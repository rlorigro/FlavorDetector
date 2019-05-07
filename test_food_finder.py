from modules.find_good_food import find_good_food


if __name__ == "__main__":
    good_foods_detected, urls = find_good_food()

    result_strings = list()

    for food_type in good_foods_detected:
        result_strings.append("ALERT! %s detected at %s:" % (food_type, good_foods_detected[food_type]["location"]))
        for item in good_foods_detected[food_type]["items"]:
            result_strings.append("\t- %s" % item)

    print("\n".join(result_strings))
