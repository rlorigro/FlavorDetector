from handlers.MenuParserV2 import MenuParser


def main():
    parser = MenuParser()

    menus = parser.get_todays_menus()

    for dining_hall in menus:
        print(menus[dining_hall])


if __name__ == "__main__":
    main()
