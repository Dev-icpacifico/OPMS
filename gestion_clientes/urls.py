from django.db import router
from django.urls import path, include
from rest_framework import routers
from .views import (NacionalidadeViewSet,AreaProfesionViewSet,ProfesioneViewSet,ClienteViewSet)

routers = routers.DefaultRouter()
routers.register(r'Nacionalidades',NacionalidadeViewSet)
routers.register(r'Areas',AreaProfesionViewSet)
routers.register(r'Profesiones',ProfesioneViewSet)
routers.register(r'Clientes',ClienteViewSet)

urlpatterns = [
    path('', include(routers.urls)),
]
