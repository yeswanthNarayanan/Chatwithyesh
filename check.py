import telebot
import requests
import json
from telebot import types
from flask import Flask
import threading

# Your Telegram Bot Token and Hugging Face Token
TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
HUGGING_FACE_TOKEN = 'xxxxxxxxxxxxxxxxxxxxxxxxxxx'

# Set Hugging Face API endpoint for the model
API_ENDPOINT = 'https://api-inference.huggingface.co/models/meta-llama/Llama-3.2-1B-Instruct'

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Welcome to the bot!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    user_input = message.text

    # Prepare data for the API request
    api_data = {
        "inputs": user_input,
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 200  # Adjust as per requirements
        }
    }

    # Hugging Face request
    headers = {
        "Authorization": f"Bearer {HUGGING_FACE_TOKEN}",
        "Content-Type": "application/json"
    }
    response = requests.post(API_ENDPOINT, headers=headers, json=api_data)

    if response.status_code == 200:
        api_response = response.json()
        assistant_response = api_response.get("generated_text", "I'm sorry, I couldn't generate a response.")
        bot.reply_to(message, assistant_response)
    else:
        bot.reply_to(message, "Sorry, something went wrong with the API request.")

@app.route('/')
def index():
    return "Bot is running!"

# Function to run Flask server
def run_flask():
    app.run(host="0.0.0.0", port=8080)

# Start bot polling and Flask server
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.polling(none_stop=True)
