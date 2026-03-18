"""
Router local del app de documentos.

Registra el DocumentViewSet con el prefijo 'documents/' y lo expone
bajo el namespace 'documents' para reverse URL lookups seguros.
"""

from rest_framework.routers import DefaultRouter
from documents.views.document import DocumentViewSet

# Router local — se incluirá en el URL raíz con prefijo /api/
router = DefaultRouter()
router.register(r'', DocumentViewSet, basename='document')

urlpatterns = router.urls
