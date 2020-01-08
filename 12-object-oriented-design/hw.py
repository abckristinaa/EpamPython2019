from __future__ import annotations

import threading
import time
from abc import ABC, abstractmethod


def endpoint(f: list):
    """ Picks endpoints available for direct delivery (as "B", "Port")."""
    def wrapper(cls: [Port, Warehouse]):
        def __init__(self, name: str, endpoints=None):
            super(cls, self).__init__(name)
            if endpoints:
                self.transit = True
                self.endpoints.append(endpoints)
            f.append(self)
        cls.__init__ = __init__
        return cls
    return wrapper


class Time_Policy:
    """ Defines methods for processing delivery data and counting time. """
    def __init__(self, database: dict=None):
        if database is None:
            database = {"B": 5, "A": 4, "Port1": 1}
        self.database = database

    @staticmethod
    def time_report(truck_data: dict, ship_data: dict) -> int:
        """ Returns number of total time of delivery. """
        if not ship_data.values():
            return max(list(truck_data.values()))
        else:
            max_truck = max(list(truck_data.values()))
            max_ship = max(list(ship_data.values()))
            if max_ship > max_truck:
                return max_ship + 1
            else:
                return max_truck

    @staticmethod
    def load(garage: list, port: list) -> tuple:
        """ Returns tuple of two dict with trucks and ships data. """
        truck_data = {}
        ship_data = {}
        print("\nЗаказ выполнен. Отчет транспортной компании: ")
        print("==" * 22)
        for car in garage:
            if len(car.route) - 1 != len(car.time_in_work):
                car.time_in_work.pop()
            truck_data[car.name] = sum(car.time_in_work)
            print(f"{car.name}: {car.route}")
        for ship in port:
            if ship.time_in_work:
                ship_data[ship.name] = (len(ship.route) - 1) * ship.to_go
                print(f"{ship.name}: {ship.route}")

        return truck_data, ship_data


class Storage:
    """Base class for buildings. """
    def __init__(self, name, policy: Time_Policy=None):
        self.name = name
        self.storage = []
        self.transit = False

        if policy is None:
            self.policy = Time_Policy()
        else:
            self.policy = policy


class Delivery:
    """ Defines the transportation methods."""
    storage: [Warehouse, Port, WarehouseND]
    truck: Transport
    order: list

    @staticmethod
    def loading(storage, truck) -> None:
        """ Loading a container on a Transport. """
        truck.cargo = storage.work.pop(0)
        storage.storage.pop(0)
        truck.route.append(storage.name)
        print(f"{truck.name} c контейнером {truck.cargo} "
              f"отправлен.")

    @staticmethod
    def transportation(storage, truck) -> [Warehouse, Port, WarehouseND]:
        """ Returns point to unloading and defines time to reach it. """
        node = None
        for point in storage.endpoints:
            if point.name == truck.cargo:
                node = point
            else:
                if point.transit:
                    for ware in point.endpoints:
                        if ware.name == truck.cargo:
                            node = point
            if node:
                truck.to_go = storage.policy.database[node.name]
                truck.time_in_work.append(truck.to_go)
                print("Время в пути: ", truck.to_go)
                time.sleep(truck.to_go * 0.4)
                return node

    @staticmethod
    def unloading(storage, truck) -> None:
        """ Unloading a container from a Transport to a point. """
        storage.storage.append(truck.cargo)
        print(f"{truck.name} доставил контейнер {truck.cargo} "
              f"на склад {storage.name}.")
        truck.cargo = None
        truck.route.append(storage.name)
        if storage.transit:
            storage.run()

    @staticmethod
    def way_back(storage, truck) -> None:
        """ Defines time for way back. """
        if storage.work:
            print(f"{truck.name} возвращается.")
            print("Время в пути: ", truck.to_go)
            truck.time_in_work.append(truck.to_go)
            time.sleep(truck.to_go)
            truck.to_go = 0

    def start(self, storage, truck) -> None:
        """ Defines chain of execution delivery. """
        while storage.work:
            self.loading(storage, truck)
            point = self.transportation(storage, truck)
            self.unloading(point, truck)
            self.way_back(storage, truck)

    @staticmethod
    def delivery_check(order: str) -> bool:
        """ Cheks if the delivery is done. """
        a = len([i.storage for i in Factory.endpoints if not i.transit][0])
        b = len([i.storage for i in Port.endpoints if not i.transit][0])
        return len(order) == a + b


class Factory(Storage, Delivery):
    car_port = []
    endpoints = []
    work = []

    def __init__(self, name: str):
        super().__init__(name)

    def accept_order(self, order: str) -> None:
        """ Puts an order in work."""
        self.work = list(order)
        self.storage = list(order)
        print(f"Заказ {order} принят в работу. Приступаем к выполнению:")
        print("=="*30, '\n')

    def run(self, order: str) -> None:
        """ Main function which runs direct delivery. """
        self.accept_order(order)
        cars_need = len(order)
        transport = Truck.hire(Factory.car_port, cars_need)
        for truck in transport:
            t = threading.Thread(target=self.start, args=(self, truck))
            t.start()
            time.sleep(0.1)
            self.car_port.append(truck)

        while not self.delivery_check(order):
            time.sleep(1)

        data1, data2 = self.policy.load(self.car_port, Port.ship_port)
        time_report = self.policy.time_report(data1, data2)
        print(f'Суммарное время для доставки контейнеров: {time_report}')


@endpoint(f=Factory.endpoints)
class Warehouse(Storage):
    """ Warehouse with direct delivery. """
    def __init__(self, name: str):
        super().__init__(name)


class WarehouseND(Storage):
    """ Warehouse with non-direct delivery. """
    def __init__(self, name: str):
        super().__init__(name)


@endpoint(f=Factory.endpoints)
class Port(Storage, Delivery):
    """Transitional point for delivery."""
    ship_port = []
    endpoints = []
    work = []

    def __init__(self, name: str, endpoints):
        super().__init__(name)
        self.transit = True

    def run(self) -> None:
        """ Runs non-direct delivery. """
        self.work = [i for i in self.storage]
        ship_needs = len(self.work)
        transport = Ship.hire(self.ship_port, ship_needs)
        if transport:
            for ship in transport:
                if not ship.cargo:
                    sh = threading.Thread(target=self.start,
                                          args=(self, ship))
                    sh.start()
                    time.sleep(1)
            self.ship_port.extend(transport)


def garage(f=Factory):
    """ Moves new trucks to the Factory garage."""
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
    """Abstract class for all kind of transport. """
    def __init__(self, name: str, cargo=None):
        self.name = name
        self.cargo = cargo
        self.route = []
        self.to_go = 0
        self.time_in_work = []

    @abstractmethod
    def report(self) -> list:
        pass

    @staticmethod
    def hire(garage: list, to_rent: int) -> list:
        pass


@garage()
class Truck(Transport):
    """A truck."""
    def __init__(self, name):
        super().__init__(name)

    def report(self) -> list:
        return self.route

    @staticmethod
    def hire(garage: list, need_to_rent: int) -> list:
        """ Issues cars from the garage on request. """
        cars_in_garage = len(garage)
        if cars_in_garage:
            if cars_in_garage <= need_to_rent:
                hired = [i for i in garage]
                garage.clear()
            else:
                hired = [garage.pop(i) for i in range(need_to_rent)]
            return hired


@port()
class Ship(Transport):
    """ A ship. """
    def __init__(self, name: str):
        super().__init__(name)

    def report(self) -> list:
        return self.route

    @staticmethod
    def hire(port: list, need_to_rent: int) -> list:
        """ Issues ships from the port on request. """
        ships_in_port = len(port)
        if ships_in_port:
            if ships_in_port <= need_to_rent:
                hired = [i for i in port]
                port.clear()
            else:
                hired = [port.pop(i) for i in range(need_to_rent)]
            return hired


if __name__ == "__main__":
    f = Factory('Factory')
    car1, car2 = Truck('Truck1'), Truck('Truck2')
    ware1, ware2 = WarehouseND('A'), Warehouse('B')
    boat = Ship('Ship1')
    port1 = Port('Port1', ware1)

    print('Автотранспорт в гараже:', *[i.name for i in Factory.car_port])
    print('Кораблей в порту:', *[i.name for i in Port.ship_port], '\n')

    f.run("AABABBAB")
