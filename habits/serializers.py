from rest_framework import serializers

from habits.models import Habit
from habits.validators import (validate_execution_time, validate_periodicity,
                               validate_pleasant_habit,
                               validate_related_habit_is_pleasant,
                               validate_related_or_reward)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate_execution_time(self, value):
        validate_execution_time(value)
        return value

    def validate_periodicity(self, value):
        validate_periodicity(value)
        return value

    def validate_related_habit(self, value):
        validate_related_habit_is_pleasant(value)
        return value

    def validate(self, data):
        validate_related_or_reward(data)
        validate_pleasant_habit(data)
        return data
