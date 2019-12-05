from functools import reduce


problem9 = [a * b * (1000 - a - b) for a in range(101, 300)
            for b in range(a + 1, 400)
            if (a ** 2 + b ** 2) == (1000 - a - b) ** 2][0]

problem6 = sum(range(101)) ** 2 - sum([i ** 2 for i in range(1, 101)])

problem48 = str(sum(i ** i for i in range(1,1001)))[-10:]

seq = reduce(lambda x, y: x + y, (str(i) for i in range(1,200000)))
problem40 = reduce(lambda x, y: x * y, [int(seq[10 ** i - 1]) for i in range(7)])
