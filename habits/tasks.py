from celery import shared_task
from django.utils import timezone
from habits.models import Habit
import telebot
from django.conf import settings


bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


@shared_task
def send_habit_reminders():
    now = timezone.localtime()
    current_time = now.time()

    habits = Habit.objects.filter(
        time__hour=current_time.hour,
        time__minute=current_time.minute
    )

    for habit in habits:
        chat_id = habit.user.telegram_chat_id
        if not chat_id:
            continue

        bot.send_message(
            chat_id,
            f'⏰ Напоминание!\n'
            f'Привычка: {habit.action}\n'
            f'Место: {habit.place}'
        )
