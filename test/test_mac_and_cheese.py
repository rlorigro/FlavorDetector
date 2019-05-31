import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from handlers.MenuParser import MenuParser
from modules.find_good_food import find_good_food


def main():
    script_directory = os.path.dirname(os.path.realpath(__file__))

    html_directory = os.path.join(script_directory, "pages")
    html_path = os.path.join(html_directory, "mac_and_cheese_pos_neg.html")

    print("Testing %s" % html_path)

    menus = dict()
    urls = dict()

    with open(html_path, "r") as page:
        menus, urls = MenuParser.parse_menu_page(name="test_mac_and_cheese",
                                                 page=page,
                                                 url="www.test_mac_and_cheese.com",
                                                 menus=menus,
                                                 urls=urls)

    good_food = {"mac and cheese": {"mac"}}

    food_found, urls = find_good_food(good_food=good_food, menus=menus, urls=urls)

    items_detected = set()
    for food_type in food_found:
        for item in food_found[food_type]["items"]:
            items_detected.add(item)

    print()
    assert "Macaroni & Cheese" in items_detected, "FAIL: Macaroni & Cheese"
    print("PASS: Macaroni & Cheese")
    assert "Potato Mac Salad" not in items_detected, "FAIL: Potato Mac Salad"
    print("PASS: Potato Mac Salad")


if __name__ == "__main__":
    main()
