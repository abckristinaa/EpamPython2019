import json


file1 = 'winedata_1.json'
file2 = 'winedata_2.json'

variety_of_wine = ['Gewürztraminer', 'Gewurztraminer', 'Riesling',
                   'Merlot', 'Madera', 'Tempranillo', 'Red Blend']


def sort_by_price_and_merge(file1, file2):
    """ Merges two given .json files removing duplicates and
    sorting values for price and variety. Returns a list of dictionaries.
    """
    with open(file1, encoding="utf-8") as f1:
        data = json.load(f1)
    with open(file2, encoding="utf-8") as f2:
        data.extend(json.load(f2))

    keys = [i for i in data[0]]
    uniq_values = set()
    for i in data:
        uniq_values.add(tuple(i.get(key) for key in keys))

    pr = keys.index("price")
    var = keys.index("variety")
    sorted_by_variety = sorted(list(uniq_values),
                               key=lambda x: str(x[var]))
    sorted_values = sorted(sorted_by_variety,
                           key=lambda x: x[pr] if x[pr] is not None else 0,
                           reverse=True)
    return [dict(zip(keys, i)) for i in sorted_values]


def get_statistics_for_chosen(data, wines):
    """Returns a dictionary with statistics for given variety:

   * `average_price`
   * `min_price`
   * `max_price`
   * `most_common_region`
   * `most_common_country`
   * `average_score`
    """

    selected = {}
    {selected.setdefault(i["variety"], []).append(i)
     for i in data if i["variety"] in wines}

    selected_stats = {}
    for wine in selected:
        all_prices = [data['price'] for data in selected[wine]
                      if data['price'] is not None]
        all_scores = [data['points'] for data in selected[wine]]

        country, province = {}, {}
        for data in selected[wine]:
            if data['country'] is not None:
                country[data['country']] = country.get(data['country'], 0) + 1
            province[data['province']] = country.get(data['province'], 0) + 1

        average_price = sum(all_prices)//len(all_prices)
        min_price = min(all_prices)
        max_price = max(all_prices)
        most_common_region = [k for k, v in province.items()
                              if v == max(province.values())][0]
        most_common_country = [k for k, v in country.items()
                               if v == max(country.values())][0]
        average_score = sum(all_prices) // len(all_scores)

        keys = ['average_price', 'min_price', 'max_price',
                'most_common_region', 'most_common_country', 'average_score']
        values = [average_price, min_price, max_price, most_common_region,
                  most_common_country, average_score]
        selected_stats[wine] = dict(zip(keys, values))

    return selected_stats


winedata_full = sort_by_price_and_merge(file1, file2)
stats = get_statistics_for_chosen(winedata_full, variety_of_wine)

with open('winedata_full.json', 'w') as wf:
    json.dump(winedata_full, wf, ensure_ascii=False, indent=4)

with open('stats.json', 'w') as wf:
    json.dump({"statistics": {'wine': stats}}, wf,
              ensure_ascii=False, indent=4)
