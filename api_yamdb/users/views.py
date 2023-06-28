# всё пойдет в api/views.py
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response


from users.models import User
from users.permissions import IsAuthorOnly
from users.serializers import CustomUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdminUser, )
    pagination_class = LimitOffsetPagination

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=(IsAuthenticated, IsAuthorOnly))
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(user,
                                         data=request.data,
                                         partial=True)
        if serializer.is_valid():
            if 'role' in request.data:
                if user.role != 'user':
                    serializer.save()
                else:
                    serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
