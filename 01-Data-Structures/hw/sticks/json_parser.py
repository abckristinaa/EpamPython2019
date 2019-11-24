import json


file1 = open('winedata_1.json', 'r')
file2 = open('winedata_2.json', 'r')


def sort_by_price_and_merge(file1, file2):
    ''' add comment'''
    uniq_values = set()
    for file in file1, file2:
        data = json.load(file)
        file.close()
        keys = [i for i in data[0]]

        for i in data:
            uniq_values.add(tuple(i.get(key) for key in keys))


    price = keys.index("price")
    variety = keys.index("variety")
    sorted_by_variety = sorted(list(uniq_values), key=lambda x: str(x[variety]))
    sorted_values = sorted(sorted_by_variety, key=lambda x: x[price] if x[price] is not None else 0, reverse=True)

    with open('winedata_full.json', 'w') as wf:
        json.dump([dict(zip(keys, i)) for i in sorted_values], wf, ensure_ascii=False, indent=4)


sort_by_price_and_merge(file1, file2)
