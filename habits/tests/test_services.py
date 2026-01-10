from datetime import timedelta

from django.contrib.auth import get_user_model
from django.utils import timezone

from habits.models import Habit
from habits.services import check_habits_is_periodicity
from habits.tests.test_habits_api import HabitBaseTestCase

User = get_user_model()


class CheckHabitPeriodicityTestCase(HabitBaseTestCase):

    def setUp(self):
        super().setUp()

    def test_periodicity_zero_returns_false(self):
        """Если проверка периодичности равна '0', возвращает False."""

        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Test",
            is_pleasant=False,
            periodicity=0,
            execution_time=60,
            is_public=False,
        )

        self.assertFalse(check_habits_is_periodicity(habit))

    def test_first_day_returns_true(self):
        """Тест первого дня, возвращает True."""

        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Test",
            is_pleasant=False,
            periodicity=2,
            execution_time=60,
            is_public=False,
        )

        self.assertTrue(check_habits_is_periodicity(habit))

    def test_periodicity_match_returns_true(self):
        """Проверка периодичности соответствия, возвращает True."""

        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Test",
            is_pleasant=False,
            periodicity=2,
            execution_time=60,
            is_public=False,
        )

        habit.created_at = timezone.now() - timedelta(days=2)
        habit.save(update_fields=["created_at"])

        self.assertTrue(check_habits_is_periodicity(habit))

    def test_periodicity_not_match_returns_false(self):
        """Проверка периодичности на совпадение, возвращает False."""

        habit = Habit.objects.create(
            user=self.user,
            place="Дом",
            time="08:00",
            action="Test",
            is_pleasant=False,
            periodicity=3,
            execution_time=60,
            is_public=False,
        )

        habit.created_at = timezone.now() - timedelta(days=1)
        habit.save(update_fields=["created_at"])

        self.assertFalse(check_habits_is_periodicity(habit))
