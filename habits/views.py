from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from habits.models import Habit
from habits.permissions import IsOwner, IsPublicReadOnly
from habits.serializers import HabitSerializer
from paginators import MyPaginator


class HabitViewSet(ModelViewSet):
    queryset = Habit.objects.all()

    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = MyPaginator

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Habit.objects.none()
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsPublicReadOnly]
    pagination_class = MyPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
