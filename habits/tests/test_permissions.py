from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status

from habits.models import Habit
from habits.tests.test_habits_api import HabitBaseTestCase

User = get_user_model()


class HabitsPermissionTestCase(HabitBaseTestCase):

    def setUp(self):
        super().setUp()

    def test_public_habits_visible(self):
        """Публичные привычки (read-only)."""

        self.public_user = User.objects.create_user(username="public", password="12345")

        Habit.objects.create(
            user=self.public_user,
            place="Home",
            time="08:00",
            action="Публичная привычка",
            is_pleasant=False,
            periodicity=1,
            execution_time=60,
            is_public=True,
        )

        response = self.client.get(reverse("habits-public"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)
