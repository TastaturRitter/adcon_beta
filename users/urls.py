from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from users.views.user_viewset import UserViewSet
from users.views.auth import AdconTokenObtainPairView

# Router local — se incluirá en el URL raíz con prefijo /api/
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    # Endpoints de Autenticación JWT localizados en el app de usuarios
    path('auth/login/', AdconTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
