import sys
import os
sys.path.append(os.path.dirname(sys.path[0]))
from handlers.MenuParserV2 import MenuParser
from modules.find_good_food import find_good_food


def main():
    script_directory = os.path.dirname(os.path.realpath(__file__))

    html_directory = os.path.join(script_directory, "pages")
    html_path = "file://" + os.path.join(html_directory, "mac_and_cheese_pos_neg_Nine.html")

    print("Testing %s" % html_path)

    menus = dict()
    parser = MenuParser()
    menus = parser.parse_menu_page(url=html_path, menus=menus)

    print(menus)

    good_food = {"mac and cheese": {"mac+cheese"}}

    food_found = find_good_food(good_food=good_food, menus=menus)

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
