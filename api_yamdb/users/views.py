# всё пойдет в api/views.py
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


from users.models import User
from users.permissions import IsAdmin
from users.serializers import CustomUserSerializer, ProfileEditSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = (IsAdmin, )
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter)
    search_fields = ('username', )

    @action(methods=['GET', 'PATCH'], detail=False,
            permission_classes=(IsAuthenticated, ))
    def me(self, request):
        user = get_object_or_404(User, username=self.request.user.username)
        if request.method == 'PATCH':
            serializer = ProfileEditSerializer(request.user, data=request.data,
                                               partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
