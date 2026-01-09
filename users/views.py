from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User
from users.serializers import UserListApiViewSerializer, UserRegisterSerializer


class UserRegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]


class UserListApiView(ListAPIView):
    serializer_class = UserListApiViewSerializer
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
