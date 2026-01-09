from rest_framework.serializers import ValidationError


def validate_related_or_reward(data):
    """Нельзя одновременно указывать вознаграждение и связанную привычку."""
    if data.get("related_habit") and data.get("reward"):
        raise ValidationError(
            "Нельзя одновременно указывать вознаграждение и связанную привычку."
        )


def validate_execution_time(value):
    """Время выполнения не больше 120 секунд."""
    if value > 120:
        raise ValidationError("Время выполнения не может превышать 120 секунд.")


def validate_periodicity(value):
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней."""
    if value > 7:
        raise ValidationError("Нельзя выполнять привычку реже, чем 1 раз в 7 дней.")


def validate_related_habit_is_pleasant(related_habit):
    """Связанная привычка должна быть приятной."""
    if related_habit and not related_habit.is_pleasant:
        raise ValidationError(
            "В связанную привычку можно указывать только приятную привычку."
        )


def validate_pleasant_habit(data):
    """У приятной привычки не может быть награды или связанной привычки."""
    if data.get("is_pleasant"):
        if data.get("reward") or data.get("related_habit"):
            raise ValidationError(
                "У приятной привычки не может быть вместе и вознаграждения и связанной привычки."
            )
