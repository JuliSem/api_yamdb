from django.urls import include, path
from rest_framework import routers

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    UserViewSet,
    signup,
    token
)

auth_patterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token')
]

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='categories')
router.register('genres', GenreViewSet, basename='genres')
router.register('titles', TitleViewSet, basename='titles')
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(router.urls))
]
