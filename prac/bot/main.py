# -*- coding: utf-8 -*-
import telebot
from telebot import types
import random
from baza import *


BOT_TOKEN = "8061663619:AAEsLjXPTiq59wQaLHazJyKKwPc-TXCIWpc"
bot = telebot.TeleBot(BOT_TOKEN)



@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Идеи для контента")
    keyboard.row("Промпты для AI")
    keyboard.row("Шаблоны")
    keyboard.row("Мемы")
    keyboard.row("Случайная идея")

    bot.send_message(
        message.chat.id,
        "Креативный генератор идей. Выбери категорию:",
        reply_markup=keyboard
    )


@bot.message_handler(func=lambda message: message.text == "Идеи для контента")
def content(message):
    idea = random.choice(content_ideas)
    bot.send_message(message.chat.id, idea)


@bot.message_handler(func=lambda message: message.text == "Промпты для AI")
def ai(message):
    prompt = random.choice(ai_prompts)
    bot.send_message(message.chat.id, prompt)


@bot.message_handler(func=lambda message: message.text == "Шаблоны")
def template(message):
    template = random.choice(templates)
    bot.send_message(message.chat.id, template)


@bot.message_handler(func=lambda message: message.text == "Мемы")
def meme(message):
    meme = random.choice(meme_ideas)
    bot.send_message(message.chat.id, meme)


@bot.message_handler(func=lambda message: message.text == "Случайная идея")
def random_idea(message):
    all_ideas = content_ideas + ai_prompts + templates + meme_ideas
    idea = random.choice(all_ideas)
    bot.send_message(message.chat.id, idea)


@bot.message_handler(func=lambda message: True)
def other(message):
    bot.send_message(message.chat.id, "Используй кнопки меню или /start")


if __name__ == "__main__":
    bot.infinity_polling()