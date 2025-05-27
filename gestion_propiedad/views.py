from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import Condominio, Etapa, SubEtapa, Torre, Modelo, Propiedade
from .serializers import (
    CondominioSerializer, EtapaSerializer, SubEtapaSerializer,
    TorreSerializer, ModeloSerializer, PropiedadeSerializer
)


# Create your views here.


# Puedes copiar este decorador para todos
def schema_decorator(name):
    return extend_schema_view(
        list=extend_schema(description=f"Lista de {name}", summary=f"Lista {name}", tags=["Propiedades"]),
        retrieve=extend_schema(description=f"Detalle de {name}", summary=f"Detalle {name}", tags=["Propiedades"]),
        create=extend_schema(description=f"Crear {name}", summary=f"Crear {name}", tags=["Propiedades"]),
        update=extend_schema(description=f"Actualizar {name}", summary=f"Actualizar {name}", tags=["Propiedades"]),
        partial_update=extend_schema(description=f"Actualizar parcialmente {name}",
                                     summary=f"Actualizar parcial {name}", tags=["Propiedades"]),
        destroy=extend_schema(description=f"Eliminar {name}", summary=f"Eliminar {name}", tags=["Propiedades"]),
    )


@schema_decorator("Condominio")
class CondominioViewSet(viewsets.ModelViewSet):
    queryset = Condominio.objects.all()
    serializer_class = CondominioSerializer
    permission_classes = [IsAuthenticated]


@schema_decorator("Etapa")
class EtapaViewSet(viewsets.ModelViewSet):
    queryset = Etapa.objects.all()
    serializer_class = EtapaSerializer
    permission_classes = [IsAuthenticated]


@schema_decorator("SubEtapa")
class SubEtapaViewSet(viewsets.ModelViewSet):
    queryset = SubEtapa.objects.all()
    serializer_class = SubEtapaSerializer
    permission_classes = [IsAuthenticated]


@schema_decorator("Torre")
class TorreViewSet(viewsets.ModelViewSet):
    queryset = Torre.objects.all()
    serializer_class = TorreSerializer
    permission_classes = [IsAuthenticated]


@schema_decorator("Modelo")
class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer
    permission_classes = [IsAuthenticated]


@schema_decorator("Propiedade")
class PropiedadeViewSet(viewsets.ModelViewSet):
    queryset = Propiedade.objects.all()
    serializer_class = PropiedadeSerializer
    permission_classes = [IsAuthenticated]
