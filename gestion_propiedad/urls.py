from django.urls import path, include
from rest_framework import routers
from .views import (
    CondominioViewSet, EtapaViewSet, SubEtapaViewSet,
    TorreViewSet, ModeloViewSet, PropiedadeViewSet
)

router = routers.DefaultRouter()
router.register(r'Condominios', CondominioViewSet)
router.register(r'Etapas', EtapaViewSet)
router.register(r'Subetapas', SubEtapaViewSet)
router.register(r'Torres', TorreViewSet)
router.register(r'Modelos', ModeloViewSet)
router.register(r'Propiedades', PropiedadeViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
