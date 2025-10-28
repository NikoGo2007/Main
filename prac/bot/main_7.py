import telebot
from telebot import types
from baza import *

bot = telebot.TeleBot("8061663619:AAEsLjXPTiq59wQaLHazJyKKwPc-TXCIWpc")
USER_DATA = {}

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
    keyboard.row("Ежедневные квесты", "Статистика", "Поделиться статистикой с друзьями")
    return keyboard

@bot.message_handler(func=lambda message: message.text == "Поделиться статистикой с друзьями")
def friend(message):
    bot.send_message(
        message.chat.id,
        "у тебя нет друзей)))")

@bot.message_handler(commands=['start'])
def start_journey(message):
    user_data = get_user_data(message.from_user.id)
    bot.send_photo(message.from_user.id, "https://images.unsplash.com/photo-1511512578047-dfb367046420?w=800&h=600&fit=crop")
    bot.send_message(
        message.chat.id,
        f"Добро пожаловать в Лотрик, Негорящий!\n\n"
        f"Уровень душ: {user_data['soul_level']}\n\n"
        f"Используй меню для путешествия...",
        reply_markup=create_main_menu()
    )


@bot.message_handler(func=lambda message: message.text == "Ежедневные квесты")
def show_daily_quests(message):
    bot.send_photo(message.from_user.id, "https://images.unsplash.com/photo-1534423861386-85a16f5d13fd?w=800&h=600&fit=crop")
    user_data = get_user_data(message.from_user.id)
    bot.send_message(
        message.chat.id,
        "Ежедневные квесты Негорящего:\nВыполни все чтобы повысить уровень душ\n",
        reply_markup=create_daily_quests_buttons(user_data['daily_state'])
    )


@bot.message_handler(func=lambda message: message.text == "Статистика")
def show_stats(message):
    bot.send_photo(message.from_user.id, "https://images.unsplash.com/photo-1542751110-97427bbecf20?w=800&h=600&fit=crop")
    user_data = get_user_data(message.from_user.id)

    stats_text = f"Статистика Негорящего:\n\n"
    stats_text += f"Уровень душ: {user_data['soul_level']}\n"
    stats_text += f"Выполнено квестов: {user_data['quests_completed']}\n\n"

    if user_data['achievements']:
        stats_text += "Достижения:\n"
        for achievement in user_data['achievements']:
            stats_text += f"• {achievement}\n"
    else:
        stats_text += "Достижения: пока нет"

    bot.send_message(message.chat.id, stats_text)


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

if __name__ == "__main__":
    bot.polling(none_stop=True)