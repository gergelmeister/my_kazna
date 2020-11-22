import requests
import datetime

class User:
    """ Stores all information about users finances """

    def __init__(self, chat_id):
        """  Constructor without arguments  """
        self.budget = 0
        self.daily_wasting = 0
        self.chat_id = chat_id

    def adding(self, number):
        """  User make some money  """
        self.budget += number

    def spent(self, number):
        """User spent some money """
        self.budget -= number
        self.daily_wasting -= number

    def display_budget(self):
        """ Display budget  """
        print(self.budget)

    def get_budget(self):
        return self.budget


class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=30):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
        else:
            last_update = None

        return last_update


bot = BotHandler("1293488251:AAHrPPm2c8ysDF6rrJBavNyCyMtyvgXQI_0")
commands = ("бюджет", "трата", "доход")
now = datetime.datetime.now()


def main():
    new_offset = None
    today = now.day
    hour = now.hour
    customers = dict()
    message_id = str()
    chat_id = str()

    while True:
        bot.get_updates(new_offset)

        last_update = bot.get_last_update()

        if last_update is not None:

            last_chat_text = last_update['message']['text'].split(" ")
            last_chat_id = last_update['message']['chat']['id']
            last_message_id = last_update['message']['message_id']

            if customers.get(last_chat_id) is None:
                customer = User(last_chat_id)
                customers[last_chat_id] = customer
            else:
                customer = customers.get(last_chat_id)

            if last_message_id != message_id:
                message_id = last_message_id
                if last_chat_text[0].lower() in commands:
                    if last_chat_text[0].lower() == "бюджет":
                        bot.send_message(last_chat_id, "На вашем счету осталось {}₽".format(customer.get_budget()))
                    elif last_chat_text[0].lower() == "трата":
                        customer.spent(float(last_chat_text[1].replace(",", ".")))
                        bot.send_message(last_chat_id, "На вашем счету осталось {}₽".format(customer.get_budget()))
                    elif last_chat_text[0].lower() == "доход":
                        customer.adding(float(last_chat_text[1].replace(",", ".")))
                        bot.send_message(last_chat_id, "Теперь на вашем счету {}₽".format(customer.get_budget()))
                else:
                    bot.send_message(last_chat_id, "Я пока не знаю такой команды :(")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        exit()




