import telebot
from django.conf import settings
from django.contrib.auth import get_user_model

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)
User = get_user_model()


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    username = message.from_user.username

    if not username:
        bot.send_message(chat_id, "❌ Укажи username в Telegram")
        return

    try:
        user = User.objects.get(username=username)
        user.telegram_chat_id = chat_id
        user.save(update_fields=["telegram_chat_id"])

        bot.send_message(chat_id, "✅ Telegram успешно привязан")
    except User.DoesNotExist:
        bot.send_message(chat_id, "❌ Пользователь не найден")


bot.infinity_polling()
