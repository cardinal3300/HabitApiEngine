from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "username",
        "email",
        "telegram_chat_id",
        "is_active",
        "is_staff",
        "date_joined",
    )

    list_filter = ("is_active", "is_staff", "date_joined")
    search_fields = ("username", "email", "telegram_chat_id")
    ordering = ("-date_joined",)
