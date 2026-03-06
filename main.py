import telebot
import random
from logic import DB_Manager
from config import TOKEN

bot = telebot.TeleBot(TOKEN)
db = DB_Manager(DATABASE)

bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-казино
К сожалению выиграть пока что тут нечего не получиться(Как и проиграть:), но можно испытать свою удачу!) 
""")

@bot.message_handler(commands=['spin'])
def spin_handler(message):
    user_id = message.from_user.id
    username = message.from_user.username or "unknown"

    # 1. Получаем список комбинаций из БД
    combinations = db.__select_data("SELECT combination, payout FROM win_combinations")

    if not combinations:
        bot.reply_to(message, "Комбинации ещё не добавлены в базу данных.")
        return

    # 2. Выбираем случайную комбинацию
    import random
    combo, payout = random.choice(combinations)

    # 3. Обновляем выигрыш пользователя
    existing = db.__select_data(
        "SELECT total_win FROM winners WHERE user_id = ?",
        (user_id,)
    )

    if existing:
        new_total = existing[0][0] + payout
        db._DB_Manager__executemany(
            "UPDATE winners SET total_win = ?, username = ? WHERE user_id = ?",
            [(new_total, username, user_id)]
        )
    else:
        db._DB_Manager__executemany(
            "INSERT INTO winners (user_id, username, total_win) VALUES (?, ?, ?)",
            [(user_id, username, payout)]
        )

    bot.reply_to(
        message,
        f"🎰 Комбинация: {combo}\n💰 Вы выиграли: {payout} денег\n"
        f"Играй ещё!"
    )


if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()