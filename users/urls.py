"""
Router local del app de usuarios.

Registra el UserViewSet con el prefijo 'users/' y lo expone
bajo el namespace 'users' para reverse URL lookups seguros.
"""

from rest_framework.routers import DefaultRouter

from users.views.user_viewset import UserViewSet

# Router local — se incluirá en el URL raíz con prefijo /api/
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls
