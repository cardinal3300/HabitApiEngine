from django.urls import reverse
from rest_framework import status

from habits.models import Habit
from habits.tests.test_habits_api import HabitBaseTestCase


class HabitPaginatorTestCase(HabitBaseTestCase):

    def setUp(self):
        super().setUp()

    def test_pagination_five_per_page(self):
        """Проверка на странице больше 5ти записей."""

        for i in range(6):
            Habit.objects.create(
                user=self.user,
                place="Дом",
                time="08:00",
                action=f"Привычка {i}",
                execution_time=60,
                is_public=True,
            )

        response = self.client.get(reverse("habits-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 5)
        self.assertEqual(response.data["count"], 6)
