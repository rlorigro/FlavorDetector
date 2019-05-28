import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from handlers.MenuParser import MenuParser
from collections import defaultdict


def find_good_food(good_food=None):
    """
    Check the UCSC dining hall menus to see if anything is worth eating. Return a dictionary of types of food found and
    their corresponding menu items. good_food is an optional override which specifies a dict of sets, where each set
    contains the keywords that are found exclusively in the desired food type
    :return:
    """
    parser = MenuParser()

    menus, urls = parser.get_todays_menus()

    if good_food is None:
        good_food = {"indian food": {"korma", "curry", "naan", "saag", "samosa", "paneer"},
                     "mac and cheese": {"mac+cheese"},
                     "chicken wings": {"wings"}}

    good_foods_detected = defaultdict(lambda: defaultdict(list))

    for dining_hall in menus:
        for item in menus[dining_hall]:
            for food_type in good_food:
                for keywords in good_food[food_type]:
                    all_found = True
                    for keyword in keywords.split('+'):
                        if keyword not in item.lower():
                            all_found = False
                    if all_found:
                        good_foods_detected[food_type]["location"] = dining_hall
                        good_foods_detected[food_type]["items"].append(item)

    return good_foods_detected, urls

