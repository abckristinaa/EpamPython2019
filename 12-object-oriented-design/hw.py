from abc import ABC, abstractmethod


def endpoint(f):
    """ Collects endpoints and transitional points for delivery together."""
    def wrapper(cls):
        def __init__(self, name, endpoint=None):
            super(cls, self).__init__(name)
            if endpoint:
                self.transit = True
                self.endpoint.append(endpoint)
            f.endpoints.append(self)
        cls.__init__ = __init__
        return cls
    return wrapper


class Storage:
    """Base class for buildings. """
    def __init__(self, name):
        self.name = name
        self.storage = []


class Time_Policy:
    def __init__(self, database=None):
        if database is None:
            database = {"B": 5, "A": 4, "Port1": 1}
        self.database = database

    def calculate_time(self, report):
        total_time = sum([report[key] * self.database[key] for key in report])
        return total_time

    @staticmethod
    def load():
        truck_data = {}
        ship_data = {}
        for truck in Factory.car_port:
            truck_data[truck.name] = [[set([i])] for i in truck.route[1:]]
        for ship in Port.ship_port:
            ship_data[ship.name] = [[set([i])] for i in ship.route[1:]]
        return truck_data, ship_data

    def data_processing(self, truck_data, ship_data):
        report = {}
        keys = list(truck_data)
        lenght = len(truck_data[keys[0]])
        union_tr_data = [i for i in truck_data[keys[0]]]
        for val in truck_data.values():
            for n in range(lenght):
                try:
                    union_tr_data[n][0] = union_tr_data[n][0].union(val[n][0])
                except IndexError:
                    pass
        last = union_tr_data[lenght-1][0]
        tmp = [i[0] for i in union_tr_data]
        union_tr_data = [k for i in tmp for k in i ]
        for i in self.database:
            report[i] = union_tr_data.count(i) * 2
            if i in last:
                report[i] -= 1
        keys = list(ship_data)
        lenght = len(ship_data[keys[0]])
        if lenght:
            union_sh_data = [i for i in ship_data[keys[0]]]
            for val in ship_data.values():
                for n in range(lenght):
                    try:
                        union_sh_data[n][0] = union_sh_data[n][0].union(val[n][0])
                    except IndexError:
                        pass
            last = union_sh_data[lenght - 1][0]
            tmp = [i[0] for i in union_sh_data]
            union_sh_data = [k for i in tmp for k in i]
            for i in self.database:
                report[i] += union_sh_data.count(i) * 2
                if i in last:
                    report[i] -= 1
        a=1
        return report


class Factory(Storage):
    car_port = []
    endpoints = []
    work = []

    def __init__(self, name, policy=None):
        super().__init__(name)
        if policy is None:
            self.policy = Time_Policy()

    @staticmethod
    def delivery(point, transport):
        if point.name == transport.cargo:
            point.storage.append(transport.cargo)
            print(f"Контейнер {transport.cargo} доставлен на склад {point.name}.")
            transport.cargo = None
            return transport.route.append(point.name)
        else:
            try:
                if point.transit:
                    for ware in point.endpoint:
                        if ware.name == transport.cargo:
                            point.storage.append(transport.cargo)
                            print(f"Контейнер {transport.cargo} доставлен на "
                                  f"склад {point.name}.")
                            transport.cargo = None
                            return transport.route.append(point.name)
            except AttributeError:
                pass

    def check_transit(self):
        transit_points = []
        for i in self.endpoints:
            try:
                if i.transit:
                    if i.storage:
                        transit_points.append(i)
            except AttributeError:
                pass
        return transit_points

    def order(self, order):
        self.work = list(order)
        order = list(order)
        print("Заказ принят в работу. Приступаем к выполнению:")
        return order

    def loading(self, park, invoice):
        while self.work:
            for container in invoice:
                try:
                    transport = next(park)
                except StopIteration:
                    park = Truck.hire()
                    transport = next(park)
                transport.cargo = self.work.pop(0)
                transport.route.append(self.name)
                print(f"{transport.name} c контейнером {container} "
                      f"отправлен.")
                for point in self.endpoints:
                    self.delivery(point, transport)

        self.work = []

    def run(self, order):
        invoice = self.order(order)
        truck = Truck.hire()
        self.loading(truck, invoice)
        transit = self.check_transit()
        for i in transit:
            i.run()
        data1, data2 = self.policy.load()
        report = self.policy.data_processing(data1, data2)
        time = self.policy.calculate_time(report)
        print(f'Суммарное время для доставки контейнеров: {time}')


@endpoint(f=Factory)
class Warehouse(Storage):
    """ Endpoint for direct delivery. """
    def __init__(self, name):
        super().__init__(name)


class WarehouseND(Storage):
    """ Endpoint for non-direct delivery. """
    def __init__(self, name):
        super().__init__(name)


@endpoint(f=Factory)
class Port(Storage):
    """Transitional point for delivery."""
    ship_port = []
    endpoint = []

    def __init__(self, name, endpoint):
        super().__init__(name)
        self.transit = True

    @staticmethod
    def delivery(point, transport):
        if point.name == transport.cargo:
            point.storage.append(transport.cargo)
            print(
                f"Контейнер {transport.cargo} доставлен на склад {point.name}.")
            transport.cargo = None
            return transport.route.append(point.name)
        else:
            try:
                if point.transit:
                    if point.endpoint == transport.cargo:
                        point.storage.append(transport.cargo)
                        print(f"Контейнер {transport.cargo} доставлен на "
                              f"склад {point.name}.")
                        transport.cargo = None
                        return transport.route.append(point.name)
            except AttributeError:
                pass

    def loading(self, park, invoice):
        while self.storage:
            for container in invoice:
                try:
                    transport = next(park)
                except StopIteration:
                    park = Ship.hire()
                    transport = next(park)
                transport.cargo = self.storage.pop(0)
                transport.route.append(self.name)
                print(f"{transport.name} c контейнером {container} "
                      f"отправлен.")
                for point in self.endpoint:
                    self.delivery(point, transport)

    def run(self):
        invoice = self.storage[:]
        ship_ = Ship.hire()
        self.loading(ship_, invoice)


def garage(f=Factory):
    """ Moves new trucks to the garage."""
    def wrapper(cls):
        def __init__(self, name):
            super(cls, self).__init__(name)
            f.car_port.append(self)
        cls.__init__ = __init__
        return cls
    return wrapper


def port(p=Port):
    """ Moves new ships to the port."""
    def wrapper(cls):
        def __init__(self, name):
            super(cls, self).__init__(name)
            p.ship_port.append(self)
        cls.__init__ = __init__
        return cls
    return wrapper


class Transport(ABC):
    """Base class for all kind of transport. """
    def __init__(self, name, cargo=None):
        self.name = name
        self.cargo = cargo
        self.route = []

    @abstractmethod
    def report(self):
        pass

    @staticmethod
    def hire():
        pass


@garage()
class Truck(Transport):
    """Simply car."""
    def __init__(self, name):
        super().__init__(name)

    def report(self):
        return self.route

    @staticmethod
    def hire():
        for car in Factory.car_port:
            if not car.cargo:
                yield car


@port()
class Ship(Transport):
    """ Simply ship. """
    def __init__(self, name):
        super().__init__(name)

    def report(self):
        return self.route

    @staticmethod
    def hire():
        for ship in Port.ship_port:
            if not ship.cargo:
                yield ship


if __name__ == "__main__":
    f = Factory('Factory')
    car1, car2 = Truck('Truck1'), Truck('Truck2')
    ware1, ware2 = WarehouseND('A'), Warehouse('B')
    boat = Ship('Ship')
    port1 = Port('Port1', ware1)
    print('В гараже:', *[i.name for i in f.car_port])

    f.run("BB")
