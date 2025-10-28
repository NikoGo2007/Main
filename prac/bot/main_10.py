# # -*- coding: utf-8 -*-
# import telebot
# from telebot import types
# import random
# from baza import *
#
#
# BOT_TOKEN = "8061663619:AAEsLjXPTiq59wQaLHazJyKKwPc-TXCIWpc"
# bot = telebot.TeleBot(BOT_TOKEN)
#
#
#
# @bot.message_handler(commands=['start'])
# def start(message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.row("Идеи для контента")
#     keyboard.row("Промпты для AI")
#     keyboard.row("Шаблоны")
#     keyboard.row("Мемы")
#     keyboard.row("Случайная идея")
#
#     bot.send_message(
#         message.chat.id,
#         "Креативный генератор идей. Выбери категорию:",
#         reply_markup=keyboard
#     )
#
#
# @bot.message_handler(func=lambda message: message.text == "Идеи для контента")
# def content(message):
#     idea = random.choice(content_ideas)
#     bot.send_message(message.chat.id, idea)
#
#
# @bot.message_handler(func=lambda message: message.text == "Промпты для AI")
# def ai(message):
#     prompt = random.choice(ai_prompts)
#     bot.send_message(message.chat.id, prompt)
#
#
# @bot.message_handler(func=lambda message: message.text == "Шаблоны")
# def template(message):
#     template = random.choice(templates)
#     bot.send_message(message.chat.id, template)
#
#
# @bot.message_handler(func=lambda message: message.text == "Мемы")
# def meme(message):
#     meme = random.choice(meme_ideas)
#     bot.send_message(message.chat.id, meme)
#
#
# @bot.message_handler(func=lambda message: message.text == "Случайная идея")
# def random_idea(message):
#     all_ideas = content_ideas + ai_prompts + templates + meme_ideas
#     idea = random.choice(all_ideas)
#     bot.send_message(message.chat.id, idea)
#
#
# @bot.message_handler(func=lambda message: True)
# def other(message):
#     bot.send_message(message.chat.id, "Используй кнопки меню или /start")
#
#
# if __name__ == "__main__":
#     bot.infinity_polling()

import telebot
from telebot import types

bot = telebot.TeleBot("8061663619:AAEsLjXPTiq59wQaLHazJyKKwPc-TXCIWpc")
USER_DATA = {}

DAILY_QUESTS = [
    "Убить 5 обычных врагов",
    "Блокировать 10 атак",
    "Совершить 5 критических атак",
    "Разжечь костер",
    "Восстановить эстус после смерти",
    "Использовать 3 предмета",
    "Пробежать 1000 шагов"
]

ACHIEVEMENTS = {
    10: "Первый рыцарь",
    20: "Искатель приключений",
    30: "Ветеран битв",
    40: "Хранитель огня",
    50: "Повелитель пепла"
}


def get_user_data(uid):
    if uid not in USER_DATA:
        USER_DATA[uid] = {
            'soul_level': 1,
            'quests_completed': 0,
            'daily_state': [False] * len(DAILY_QUESTS),
            'achievements': []
        }
    return USER_DATA[uid]


def check_achievements(user_data):
    new_achievements = []
    for level, achievement in ACHIEVEMENTS.items():
        if user_data['soul_level'] >= level and achievement not in user_data['achievements']:
            user_data['achievements'].append(achievement)
            new_achievements.append(achievement)
    return new_achievements


def create_daily_quests_buttons(state):
    keyboard = types.InlineKeyboardMarkup()
    for idx, (completed, quest) in enumerate(zip(state, DAILY_QUESTS)):
        status = "[X]" if completed else "[ ]"
        keyboard.row(types.InlineKeyboardButton(
            f"{status} {quest}",
            callback_data=f"quest:{idx}"
        ))
    return keyboard


def create_main_menu():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Ежедневные квесты", "Статистика")
    return keyboard


def create_share_stats_button():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.row(types.InlineKeyboardButton("Поделиться статистикой", callback_data="share_stats"))
    return keyboard


def format_stats_for_share(user_data, username):
    share_text = f"🔥 Статистика Негорящего {username}:\n\n"
    share_text += f"Уровень душ: {user_data['soul_level']}\n"
    share_text += f"Выполнено квестов: {user_data['quests_completed']}\n"

    if user_data['achievements']:
        share_text += f"Достижений: {len(user_data['achievements'])}\n"
        share_text += "Полученные звания:\n"
        for achievement in user_data['achievements']:
            share_text += f"• {achievement}\n"

    share_text += "\nПрисоединяйся к путешествию в Лотрике!"
    return share_text


@bot.message_handler(commands=['start'])
def start_journey(message):
    user_data = get_user_data(message.from_user.id)
    bot.send_message(
        message.chat.id,
        f"Добро пожаловать в Лотрик, Негорящий!\n\n"
        f"Уровень душ: {user_data['soul_level']}\n\n"
        f"Используй меню для путешествия...",
        reply_markup=create_main_menu()
    )


@bot.message_handler(func=lambda message: message.text == "Ежедневные квесты")
def show_daily_quests(message):
    user_data = get_user_data(message.from_user.id)
    bot.send_message(
        message.chat.id,
        "Ежедневные квесты Негорящего:\nВыполни все чтобы повысить уровень душ\n",
        reply_markup=create_daily_quests_buttons(user_data['daily_state'])
    )


@bot.message_handler(func=lambda message: message.text == "Статистика")
def show_stats(message):
    user_data = get_user_data(message.from_user.id)

    # Проверяем достижения при открытии статистики
    check_achievements(user_data)

    stats_text = f"Статистика Негорящего:\n\n"
    stats_text += f"Уровень душ: {user_data['soul_level']}\n"
    stats_text += f"Выполнено квестов: {user_data['quests_completed']}\n\n"

    if user_data['achievements']:
        stats_text += "Достижения:\n"
        for achievement in user_data['achievements']:
            stats_text += f"• {achievement}\n"
    else:
        stats_text += "Достижения: пока нет"

    bot.send_message(
        message.chat.id,
        stats_text,
        reply_markup=create_share_stats_button()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("quest:"))
def complete_quest(call):
    idx = int(call.data.split(":")[1])
    user_data = get_user_data(call.from_user.id)

    if not user_data['daily_state'][idx]:
        user_data['daily_state'][idx] = True
        user_data['quests_completed'] += 1

        if all(user_data['daily_state']):
            user_data['soul_level'] += 1
            user_data['daily_state'] = [False] * len(DAILY_QUESTS)

            message_text = f"Все квесты выполнены!\n\nУровень душ повышен: {user_data['soul_level']}\nКвесты сброшены для нового дня..."

            bot.send_message(call.message.chat.id, message_text)

    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        reply_markup=create_daily_quests_buttons(user_data['daily_state'])
    )


@bot.callback_query_handler(func=lambda call: call.data == "share_stats")
def share_stats(call):
    user_data = get_user_data(call.from_user.id)
    username = call.from_user.first_name or "Негорящий"

    share_text = format_stats_for_share(user_data, username)

    bot.send_message(
        call.message.chat.id,
        "Вот твоя статистика для分享:\n\n" + share_text
    )


bot.polling(none_stop=True)