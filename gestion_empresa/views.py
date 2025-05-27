from django.shortcuts import render
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Empresa
from .serializers import EmpresaSerializer

@extend_schema_view(
    list=extend_schema(
        description="Obtiene una lista de todas las empresas registradas.",
        summary="Lista de Empresa",
        tags=["Empresa"],
    ),
    retrieve=extend_schema(
        description="Obtiene los detalles de una empresa específica por su ID.",
        summary="Detalle de Empresa",
        tags=["Empresa"]
    ),
    create=extend_schema(
        description="Crea una nueva empresa con los datos proporcionados.",
        summary="Crear Empresa",
        tags=["Empresa"]
    ),
    update=extend_schema(
        description="Actualiza todos los campos de una empresa existente.",
        summary="Actualizar Empresa",
        tags=["Empresa"]
    ),
    partial_update=extend_schema(
        description="Actualiza parcialmente los campos de una empresa existente.",
        summary="Actualizar Parcialmente Empresa",
        tags=["Empresa"]
    ),
    destroy=extend_schema(
        description="Elimina una empresa existente por su ID.",
        summary="Eliminar Empresa",
        tags=["Empresa"]
    ),
)
class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAuthenticated]
