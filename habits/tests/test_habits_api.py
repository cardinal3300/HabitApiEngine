from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit

User = get_user_model()


class HabitBaseTestCase(APITestCase):
    """Авторизация (JWT) для тестирования."""

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="12345", telegram_chat_id="123456789"
        )

        self.client.force_authenticate(user=self.user)


class HabitCreateTestCase(HabitBaseTestCase):
    """Тест создания привычки."""

    def test_create_habit(self):
        data = {
            "place": "Дом",
            "time": "08:00",
            "action": "Сделать зарядку",
            "is_pleasant": False,
            "periodicity": 1,
            "execution_time": 60,
            "is_public": False,
        }

        response = self.client.post(reverse("habits-list"), data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 1)
