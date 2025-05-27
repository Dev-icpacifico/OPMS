from django.db import router
from django.urls import path, include
from rest_framework import routers
from .views import EmpresaViewSet

routers = routers.DefaultRouter()

routers.register(r'Empresas',EmpresaViewSet)


urlpatterns = [
    path('', include(routers.urls)),
]