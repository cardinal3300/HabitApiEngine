from rest_framework.routers import DefaultRouter
from django.urls import path
from habits.views import HabitViewSet, PublicHabitListAPIView


router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')

urlpatterns = [
    path('habits/public/', PublicHabitListAPIView.as_view()),
]

urlpatterns += router.urls
