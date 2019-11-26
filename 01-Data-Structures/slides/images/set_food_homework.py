
pizza_food = {'ground_peper', 'onion', 'tomatoes', 'salt', 'cheese',
              'sweet_basil', 'oregano', 'pepperoni', 'garlic', 'dough'}
shaverma = {'cabbage', 'onion', 'tomatoes', 'lavash',
            'souce', 'cucumber', 'fried_chicken'}


elements_pizza = len(pizza_food)
elements_shaverma = len(shaverma)

is_garlic_in_pizza = 'garlic' in pizza_food
is_carrot_not_in_shaverma = 'carrot' not in shaverma

check_for_common_food = pizza_food.isdisjoint(shaverma)
is_pizza_food_subset_of_shaverma = pizza_food.issubset(shaverma)
is_pizza_food_superset_of_shaverma = pizza_food.issuperset(shaverma)

unique_food = set()
unique_food = unique_food.union(pizza_food, shaverma)

common_food = pizza_food.intersection(shaverma)

unique_pizza_food = pizza_food - shaverma
unique_shaverma_food = shaverma.difference(pizza_food)
is_uniq_food = pizza_food.symmetric_difference(shaverma)

one_more_pizza_please = pizza_food.copy()
one_more_pizza_please.add('bacon')
one_more_pizza_please.discard('bacon')
one_more_pizza_please.remove('onion')
some_food = one_more_pizza_please.pop()

next_pizza = pizza_food.copy()
next_pizza.clear()

print(elements_pizza, elements_shaverma,
      is_garlic_in_pizza,
      is_carrot_not_in_shaverma,
      check_for_common_food,
      is_pizza_food_subset_of_shaverma,
      is_pizza_food_superset_of_shaverma,
      unique_food,
      common_food,
      unique_pizza_food,
      unique_shaverma_food,
      is_uniq_food,
      one_more_pizza_please,
      some_food,
      sep="\n")
