from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from habits.models import Habit
from habits.tests.test_habits_api import HabitBaseTestCase

User = get_user_model()


class HabitValidationTestCase(HabitBaseTestCase):

    def setUp(self):
        super().setUp()

    def test_periodicity_less_once_7_days(self):
        """Нельзя выполнять привычку реже, чем 1 раз в 7 дней."""

    def test_execution_time_more_than_120(self):
        """Нельзя время на выполнение больше 120 секунд execution_time > 120."""

        data = {
            "place": "Дом",
            "time": "08:00",
            "action": "Сделать зарядку",
            "is_pleasant": False,
            "periodicity": 1,
            "execution_time": 150,
            "is_public": False,
        }

        response = self.client.post(reverse("habits-list"), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_reward_and_related_habit_together(self):
        """Нельзя вознаграждение и связанная привычка одновременно reward + related_habit."""

        pleasant = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="09:00",
            action="Выпить кофе",
            is_pleasant=True,
            periodicity=1,
            execution_time=60,
            is_public=False,
        )

        data = {
            "place": "Дом",
            "time": "08:00",
            "action": "Зарядка",
            "execution_time": 60,
            "reward": "Шоколад",
            "related_habit": pleasant.id,
        }

        response = self.client.post(reverse("habits-list"), data)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
