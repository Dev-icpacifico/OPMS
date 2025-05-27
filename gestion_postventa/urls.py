from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'recintos', RecintoViewSet)
router.register(r'lugares', LugarViewSet)
router.register(r'items', ItemViewSet)
router.register(r'problemas', ProblemaViewSet)
router.register(r'especialidades', EspecialidadViewSet)
router.register(r'causas', CausaViewSet)
router.register(r'alcance-responsabilidad', AlcanceResponsabilidadViewSet)
router.register(r'requerimientos-postventa', RequerimientoPostVentaViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
