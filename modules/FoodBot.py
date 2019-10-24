from find_good_food import find_good_food
from slackclient import SlackClient
import configparser
import datetime
import time


class FoodBot:
    def __init__(self, channel, config_path, target_time):
        """
        :param channel: name of the slack channel to post to
        :param config_path: where the authorization data lives
        :param target_time: a datetime.time object with hour and minute fields that specifies the target time to check menu
        """
        self.channel = channel
        self.config_path = config_path
        self.key = self.get_key_from_config_file()

        self.client = SlackClient(self.key)
        self.find_good_food = find_good_food

        self.date_prev = datetime.date(year=1, month=1, day=1)
        self.target_time = target_time

        self.good_food = {"Indian food": {"korma", "tikka", "curry", "naan", "saag", "samosa", "paneer", "madras"},
                          "Mac and cheese": {"mac+cheese"},
                          "Chicken wings": {"wings"}}

        self.emojis = {"Indian food": ":flag-in:",
                       "Mac and cheese": ":cheese_wedge:",
                       "Chicken wings": ":poultry_leg:"}

    def get_key_from_config_file(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)

        return config["Authorization"]["bot_user_access_token"]

    def generate_message(self, good_foods_detected):
        lines = list()

        for food_type in good_foods_detected:
            dining_hall_name = good_foods_detected[food_type]["location"]

            line = "%s detected at %s!" % (food_type, dining_hall_name)
            line = ":rotating_light:" + self.emojis[food_type] + " " + line + " " + self.emojis[food_type] + ":rotating_light:"
            lines.append(line)

            for item in good_foods_detected[food_type]["items"]:
                lines.append("\t- %s" % item)

        message = "\n".join(lines)

        return message

    def launch(self):
        while True:
            now = datetime.datetime.now()
            date_now = datetime.date(year=now.year, month=now.month, day=now.day)
            time_now = datetime.time(hour=now.hour, minute=now.minute)

            if date_now > self.date_prev and time_now > self.target_time:
                success = self.update()

                if success:
                    self.date_prev = date_now

            time.sleep(30)

    def update(self):
        if self.client.rtm_connect(with_team_state=False):
            print("Bot connected!")

            good_foods_detected = self.find_good_food(self.good_food)

            if len(good_foods_detected) == 0:
                print("No good food detected :(")

            if len(good_foods_detected) > 0:
                message = self.generate_message(good_foods_detected)

                print(message)

                self.client.api_call(
                    "chat.postMessage",
                    channel=self.channel,
                    text=message)

            return True

        else:
            print("Connection failed")

            return False


if __name__ == "__main__":
    config_path = "conf/auth"
    channel_name = "lunch"

    target_hour = 11
    target_minute = 0
    target_time = datetime.time(hour=target_hour, minute=target_minute)

    bot = FoodBot(channel=channel_name, config_path=config_path, target_time=target_time)
    bot.launch()
