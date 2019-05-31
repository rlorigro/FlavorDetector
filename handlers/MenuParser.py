from urllib.parse import urlencode
from bs4 import BeautifulSoup
import requests


class MenuParser:
    def __init__(self):
        self.menu_root_url = "https://nutrition.sa.ucsc.edu/pickMenu.asp?"

        self.dining_halls = {"nine ten":
                                {"locationName":"Colleges Nine & Ten Dining Hall",
                                 "locationNum": 40,
                                 "mealName": "Lunch"},

                             "crown merril":
                                {"locationName": "Crown Merrill Dining Hall",
                                 "locationNum": 20,
                                 "mealName": "Lunch"}}

    def get_todays_menus(self):
        menus = dict()
        urls = dict()

        for name, info in self.dining_halls.items():
            url = self.menu_root_url + urlencode(info)

            page = requests.get(url).text

            menus, urls = self.parse_menu_page(name=name, page=page, url=url, menus=menus, urls=urls)

        return menus, urls

    @staticmethod
    def parse_menu_page(name, page, url, menus, urls):
        soup = BeautifulSoup(page, "html.parser")

        divs = soup.find_all("div", class_="pickmenucoldispname")

        items = list()
        for div in divs:
            item_name = div.find('a').contents[0]

            if not item_name.startswith("http"):
                items.append(item_name)

        menus[name] = items
        urls[name] = url

        return menus, urls




"""
https://nutrition.sa.ucsc.edu/pickMenu.asp?locationNum=40&locationName=Colleges+Nine+%26+Ten+Dining+Hall&dtdate=05%2F07%2F2019&mealName=Lunch&sName=

https://nutrition.sa.ucsc.edu/pickMenu.asp?locationNum=40&locationName=Colleges Nine & Ten Dining Hall&dtdate=05/07/2019&mealName=Lunch&sName=

https://nutrition.sa.ucsc.edu/pickMenu.asp?

locationNum=40
locationName=Colleges Nine & Ten Dining Hall
dtdate=05/07/2019
mealName=Lunch
sName=


{"locationNum" : "40",
"locationName" : "Colleges Nine & Ten Dining Hall",
"dtdate" : "05/07/2019",
"mealName" : "Lunch",
"sName" : ""}

"""