from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Habit(models.Model):
    """Модель привычки."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        verbose_name="Пользователь",
    )
    place = models.CharField(max_length=255, verbose_name="Место")
    time = models.TimeField(verbose_name="Время")
    action = models.CharField(max_length=255, verbose_name="Действие")
    is_pleasant = models.BooleanField(
        default=False, verbose_name="Признак приятной привычки"
    )
    related_habit = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Связанная привычка",
    )
    periodicity = models.PositiveSmallIntegerField(
        default=1, verbose_name="Периодичность (в днях)"
    )
    reward = models.CharField(
        max_length=255, null=True, blank=True, verbose_name="Вознаграждение"
    )
    execution_time = models.PositiveSmallIntegerField(
        verbose_name="Время на выполнение (в секундах)"
    )
    is_public = models.BooleanField(default=False, verbose_name="Признак публичности")
    created_at = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Время создания"
    )
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name="Время обновления"
    )

    def clean(self):
        """Валидация бизнес-логики."""
        # 1. Нельзя указывать и reward и related_habit
        if self.reward and self.related_habit:
            raise ValidationError(
                "Нельзя одновременно указывать вознаграждение и связанную привычку."
            )

        # 2. Время выполнения <= 120 секунд
        if self.execution_time > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд.")

        # 3. Периодичность не реже 1 раза в 7 дней
        if self.periodicity > 7:
            raise ValidationError("Нельзя выполнить привычку реже, чем 1 раз в 7 дней.")

        # 4. В связанные привычки может попадать только приятная привычка
        if self.related_habit and not self.related_habit.is_pleasant:
            raise ValidationError("Связанная привычка должна быть приятной.")

        # 5. У приятной привычки не может быть reward и related_habit
        if self.is_pleasant and (self.reward or self.related_habit):
            raise ValidationError(
                "У приятной привычки не может быть вместе и вознаграждения или связанной привычки."
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} - {self.time} ({self.user})"

    class Meta:
        verbose_name = "Привычка"
        verbose_name_plural = "Привычки"
        ordering = ["-created_at"]
