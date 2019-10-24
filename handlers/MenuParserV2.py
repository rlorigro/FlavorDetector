from selenium.webdriver.firefox.options import Options
from selenium import webdriver
import os


class MenuParser:
    def __init__(self):
        self.menu_index_page = "https://nutrition.sa.ucsc.edu/"
        self.driver = self.initialize_headless_browser()

        self.dining_hall_names = {"Nine","Crown","Porter"}
        self.menu_urls = list()

    def initialize_headless_browser(self):
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Firefox(options=options, service_log_path=os.path.devnull)

        return driver

    def get_todays_menus(self):
        # Load main index
        self.driver.get(self.menu_index_page)

        # Find all the specific dining hall menu links
        candidate_elements = self.driver.find_elements_by_partial_link_text("Hall")

        # Sanity check
        if len(candidate_elements) == 0:
            exit("ERROR: no links found at " + self.menu_index_page)
        else:
            n_dining_halls = len(candidate_elements)

        # Load the main index page and then click each of the dining hall links (browsing within the same window)
        # store the links in a list for next step
        dining_hall_urls = list()
        for i in range(n_dining_halls):
            self.driver.get(self.menu_index_page)
            candidate_elements = self.driver.find_elements_by_partial_link_text("Hall")
            candidate_elements[i].click()

            candidate_elements = self.driver.find_elements_by_class_name("shortmenunutritive")
            for element in candidate_elements:
                for child in element.find_elements_by_partial_link_text(""):
                    url = child.get_attribute("href")

                    if not any([name in url for name in self.dining_hall_names]):
                        continue

                    if "Lunch" not in url:
                        continue

                    dining_hall_urls.append(url)

        # Load the menus (finally)
        menus = dict()
        for url in dining_hall_urls:
            self.parse_menu_page(url, menus)

        return menus

    def parse_menu_page(self, url, menus):
        self.driver.get(url)

        # Extract the text from the child 'a' element of every div which has the "longmenucoldispname" class name
        divs = self.driver.find_elements_by_class_name("longmenucoldispname")
        menu_items = list()
        for div in divs:
            menu_item = div.find_elements_by_css_selector("a")[0].text
            menu_items.append(menu_item)

        # Re-derive the dining hall "name" from this url
        name = None
        for candidate_name in self.dining_hall_names:
            if candidate_name in url:
                name = candidate_name

        if name is None:
            exit("ERROR: unknown dining hall page: " + url)

        menus[name] = menu_items

        return menus


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