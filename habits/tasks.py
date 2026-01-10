import telebot
from celery import shared_task
from django.conf import settings
from django.utils import timezone

from habits.models import Habit
from habits.services import check_habits_is_periodicity
from users.models import User

bot = telebot.TeleBot(settings.TELEGRAM_BOT_TOKEN)


@shared_task
def send_habit_reminders():
    """Отправка напоминания пользователю телеграм-боту о его привычках."""
    now = timezone.localtime()
    current_hour = now.hour
    current_minute = now.minute

    users = User.objects.filter(
        telegram_chat_id__isnull=False,
        is_active=True,
    )

    for user in users:
        habits = Habit.objects.filter(
            user=user,
            time__hour=current_hour,
            time__minute=current_minute,
        )

        for habit in habits:
            if not check_habits_is_periodicity(habit):
                continue

            bot.send_message(
                user.telegram_chat_id,
                (
                    f"⏰ Напоминание! {habit.action}\n"
                    f"📍 Место: {habit.place}\n"
                    f"🕗 Время: {habit.time.strftime('%H:%M')}\n"
                    f"Время на выполнение: {habit.execution_time} секунд\n"
                    f"🎁 Вознаграждение: {habit.reward}\n"
                    f"😊 Приятная привычка {habit.related_habit}"
                ),
            )
