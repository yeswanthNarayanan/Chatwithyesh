import telebot
import requests
import json
from telebot import types

TOKEN = 'ur telegram bot api key'
API_ENDPOINT = 'http://localhost:1234/v1/chat/completion'#your lm studio model end point


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to the yesh bot!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_input = message.text

    # Prepare the data for the API request
    api_data = {
        "messages": [
            {"role": "system", "content": "Below is an instruction that describes a task. Write a response that appropriately completes the request."},
            {"role": "user", "content": user_input}
        ],
        "temperature": 0.7,
        "max_tokens": 10000,
        "stream": False
    }

    # Make a request to the API
    response = requests.post(API_ENDPOINT, json=api_data, headers={"Content-Type": "application/json"})


    if response.status_code == 200:
        # Parse the API response
        api_response = json.loads(response.text)

        # Extract the assistant's response from the API response
        assistant_response = api_response["choices"][0]["message"]["content"]

        #bot.reply_to(message, assistant_response)
        bot.reply_to(message, assistant_response)
    else:
        bot.reply_to(message, "Sorry, something went wrong with the API request.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
