from django.contrib import admin
from .models import Habit


@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'action',
        'place',
        'time',
        'is_pleasant',
        'related_habit',
        'reward',
        'execution_time',
        'periodicity',
        'is_public',
        'created_at',
    )

    list_filter = (
        'is_pleasant',
        'is_public',
        'periodicity',
    )

    search_fields = (
        'action',
        'place',
        'user__email',
        'user__username',
    )

    ordering = ('-created_at',)

    readonly_fields = ('created_at',)

    fieldsets = (
        ('Основное', {
            'fields': (
                'user',
                'action',
                'place',
                'time',
                'execution_time',
                'periodicity',
            )
        }),
        ('Тип привычки', {
            'fields': (
                'is_pleasant',
                'related_habit',
                'reward',
            )
        }),
        ('Публикация', {
            'fields': (
                'is_public',
            )
        }),
        ('Служебная информация', {
            'fields': (
                'created_at',
            )
        }),
    )
