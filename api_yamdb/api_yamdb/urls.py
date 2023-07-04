from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

from api.views import signup, token, UserViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)

auth_patterns = [
    path('signup/', signup, name='signup'),
    path('token/', token, name='token')
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include(auth_patterns)),
    path('api/v1/', include(router.urls)),
    path('redoc/',
         TemplateView.as_view(template_name='redoc.html'),
         name='redoc'),
]
