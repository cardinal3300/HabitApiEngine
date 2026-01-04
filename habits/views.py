from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from habits.models import Habit
from habits.serializers import HabitSerializer
from habits.permissions import IsOwner, IsPublicReadOnly
from paginators import MyPaginator


class HabitViewSet(ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = MyPaginator

    def get_queryset(self):
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListAPIView(ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [IsPublicReadOnly]
    pagination_class = MyPaginator

    def get_queryset(self):
        return Habit.objects.filter(is_public=True)
