from django.shortcuts import render
from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import (Nacionalidade,AreaProfesion,Profesione,Cliente)
from .serializers import (NacionalidadSerializer,AreaProfesionSerializer,ProfesioneSerializer,ClienteSerializer)

# Create your views here.

@extend_schema_view(
    list=extend_schema(
        description="Obtiene una lista de todos los proyectos registrados.",
        summary="Lista de Nacionalidades",
        tags=["Nacionalidades"],
    ),
    retrieve=extend_schema(
        description="Obtiene los detalles de un proyecto específico por su ID.",
        summary="Detalle de Nacionalidades",
        tags=["Nacionalidades"]
    ),
    create=extend_schema(
        description="Crea un nuevo proyecto con los datos proporcionados.",
        summary="Crear Nacionalidades",
        tags=["Nacionalidades"]
    ),
    update=extend_schema(
        description="Actualiza todos los campos de un proyecto existente.",
        summary="Actualizar Nacionalidades",
        tags=["Nacionalidades"]
    ),
    partial_update=extend_schema(
        description="Actualiza parcialmente los campos de un proyecto.",
        summary="Actualizar Parcialmente Nacionalidades",
        tags=["Nacionalidades"]
    ),
    destroy=extend_schema(
        description="Elimina un proyecto existente por su ID.",
        summary="Eliminar Nacionalidades",
        tags=["Nacionalidades"]
    ),
)
class NacionalidadeViewSet(viewsets.ModelViewSet):
    queryset = Nacionalidade.objects.all()
    serializer_class = NacionalidadSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        description="Obtiene una lista de todos los proyectos registrados.",
        summary="Lista de Areas",
        tags=["Areas"]
    ),
    retrieve=extend_schema(
        description="Obtiene los detalles de un proyecto específico por su ID.",
        summary="Detalle de Areas",
        tags=["Areas"]
    ),
    create=extend_schema(
        description="Crea un nuevo proyecto con los datos proporcionados.",
        summary="Crear Areas",
        tags=["Areas"]
    ),
    update=extend_schema(
        description="Actualiza todos los campos de un proyecto existente.",
        summary="Actualizar Areas",
        tags=["Areas"]
    ),
    partial_update=extend_schema(
        description="Actualiza parcialmente los campos de un proyecto.",
        summary="Actualizar Parcialmente Areas",
        tags=["Areas"]
    ),
    destroy=extend_schema(
        description="Elimina un proyecto existente por su ID.",
        summary="Eliminar Areas",
        tags=["Areas"]
    ),
)

class AreaProfesionViewSet(viewsets.ModelViewSet):
    queryset = AreaProfesion.objects.all()
    serializer_class = AreaProfesionSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        description="Obtiene una lista de todos los proyectos registrados.",
        summary="Lista de Profesiones",
        tags=["Profesiones"]
    ),
    retrieve=extend_schema(
        description="Obtiene los detalles de un proyecto específico por su ID.",
        summary="Detalle de Profesiones",
        tags=["Profesiones"]
    ),
    create=extend_schema(
        description="Crea un nuevo proyecto con los datos proporcionados.",
        summary="Crear Profesiones",
        tags=["Profesiones"]
    ),
    update=extend_schema(
        description="Actualiza todos los campos de un proyecto existente.",
        summary="Actualizar Profesiones",
        tags=["Profesiones"]
    ),
    partial_update=extend_schema(
        description="Actualiza parcialmente los campos de un proyecto.",
        summary="Actualizar Parcialmente Profesiones",
        tags=["Profesiones"]
    ),
    destroy=extend_schema(
        description="Elimina un proyecto existente por su ID.",
        summary="Eliminar Profesiones",
        tags=["Profesiones"]
    ),
)

class ProfesioneViewSet(viewsets.ModelViewSet):
    queryset = Profesione.objects.all()
    serializer_class = ProfesioneSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(
        description="Obtiene una lista de todos los proyectos registrados.",
        summary="Lista de Clientes",
        tags=["Clientes"]
    ),
    retrieve=extend_schema(
        description="Obtiene los detalles de un proyecto específico por su ID.",
        summary="Detalle de Clientes",
        tags=["Clientes"]
    ),
    create=extend_schema(
        description="Crea un nuevo proyecto con los datos proporcionados.",
        summary="Crear Clientes",
        tags=["Clientes"]
    ),
    update=extend_schema(
        description="Actualiza todos los campos de un proyecto existente.",
        summary="Actualizar Clientes",
        tags=["Clientes"]
    ),
    partial_update=extend_schema(
        description="Actualiza parcialmente los campos de un proyecto.",
        summary="Actualizar Parcialmente Clientes",
        tags=["Clientes"]
    ),
    destroy=extend_schema(
        description="Elimina un proyecto existente por su ID.",
        summary="Eliminar Clientes",
        tags=["Clientes"]
    ),
)

class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated]