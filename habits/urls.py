from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.views import HabitViewSet, PublicHabitListAPIView

router = DefaultRouter()
router.register(r"habits", HabitViewSet, basename="habits")

urlpatterns = [
    path("public/", PublicHabitListAPIView.as_view(), name="habits-public"),
]

urlpatterns += router.urls
