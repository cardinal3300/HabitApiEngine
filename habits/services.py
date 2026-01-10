from django.utils import timezone


def check_habits_is_periodicity(habit):
    """Проверка, выполняться ли сегодня привычка с учётом периодичности."""
    if habit.periodicity <= 0:
        return False

    today = timezone.localtime().date()
    start_date = habit.created_at.date()

    total_day = (today - start_date).days

    if total_day < 0:
        return False

    return total_day % habit.periodicity == 0
