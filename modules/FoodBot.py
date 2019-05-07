from find_good_food import find_good_food
from slackclient import SlackClient
import configparser


class FoodBot:
    def __init__(self, channel, config_path):
        self.channel = channel
        self.config_path = config_path
        self.key = self.get_key_from_config_file()

        self.client = SlackClient(self.key)
        self.find_good_food = find_good_food

    def get_key_from_config_file(self):
        config = configparser.ConfigParser()
        config.read(self.config_path)

        return config["Authorization"]["bot_user_access_token"]

    def generate_message(self, good_foods_detected, urls):
        lines = list()

        for food_type in good_foods_detected:
            dining_hall_name = good_foods_detected[food_type]["location"]
            lines.append(":rotating_light: ALERT %s detected at %s! :rotating_light:" % (food_type, dining_hall_name))

            for item in good_foods_detected[food_type]["items"]:
                lines.append("\t- %s" % item)

            lines.append("\n" + urls[dining_hall_name])

        message = "\n".join(lines)

        return message

    def launch(self):
        if self.client.rtm_connect(with_team_state=False):
            print("Starter Bot connected and running!")

            good_foods_detected, urls = self.find_good_food()

            if len(good_foods_detected) > 0:
                message = self.generate_message(good_foods_detected, urls)

                self.client.api_call(
                    "chat.postMessage",
                    channel=self.channel,
                    text=message)

        else:
            print("Connection failed")


if __name__ == "__main__":
    config_path = "conf/auth"
    channel_name = "bot_test"

    # starterbot's user ID in Slack: value is assigned after the bot starts up
    starterbot_id = None

    bot = FoodBot(channel=channel_name, config_path=config_path)
    bot.launch()
