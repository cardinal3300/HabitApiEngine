from datetime import time
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.utils import timezone

from habits.models import Habit
from habits.tasks import send_habit_reminders
from habits.tests.test_habits_api import HabitBaseTestCase

User = get_user_model()


class SendHabitRemindersTaskTestCase(HabitBaseTestCase):

    def setUp(self):
        super().setUp()

    @patch("habits.tasks.bot.send_message")
    def test_reminder_sent_when_conditions_match(self, mock_send):
        """Напоминание отправляется при выполнении условий."""
        now = timezone.localtime()

        Habit.objects.create(
            user=self.user,
            action="Выпить воды",
            place="Дом",
            time=time(now.hour, now.minute),
            execution_time=30,
            periodicity=1,
        )

        send_habit_reminders()

        self.assertEqual(mock_send.call_count, 1)

    @patch("habits.tasks.bot.send_message")
    def test_reminder_not_sent_if_wrong_time(self, mock_send):
        """Напоминание не отправляется, если время указано не верно."""

        Habit.objects.create(
            user=self.user,
            action="Пробежка",
            place="Улица",
            time="23:59",
            execution_time=60,
            periodicity=1,
        )

        send_habit_reminders()

        mock_send.assert_not_called()

    @patch("habits.tasks.bot.send_message")
    @patch("habits.tasks.check_habits_is_periodicity", return_value=False)
    def test_reminder_not_sent_if_periodicity_false(self, mock_periodicity, mock_send):
        """Если периодичность не задана, напоминание не отправляется."""
        now = timezone.localtime()

        Habit.objects.create(
            user=self.user,
            place="Дом",
            time=time(now.hour, now.minute),
            action="Йога",
            is_pleasant=False,
            execution_time=60,
            periodicity=1,
            is_public=False,
        )

        send_habit_reminders()

        mock_send.assert_not_called()
