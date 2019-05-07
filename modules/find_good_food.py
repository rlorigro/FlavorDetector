import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from handlers.MenuParser import MenuParser
from collections import defaultdict


def find_good_food():
    """
    Check the UCSC dining hall menus to see if anything is worth eating. Return a list containing
    :return:
    """
    parser = MenuParser()

    menus, urls = parser.get_todays_menus()

    good_food = {"indian food": {"korma", "curry", "naan", "saag", "samosa", "paneer"},
                 "mac and cheese": {"mac"},
                 "pizza": {"pizza"},
                 "chicken wings": {"wings"}}

    good_foods_detected = defaultdict(lambda: defaultdict(list))

    for dining_hall in menus:
        for item in menus[dining_hall]:
            for food_type in good_food:
                for keyword in good_food[food_type]:
                    if keyword in item.lower():
                        good_foods_detected[food_type]["location"] = dining_hall
                        good_foods_detected[food_type]["items"].append(item)

    return good_foods_detected, urls

