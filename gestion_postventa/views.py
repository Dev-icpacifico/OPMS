from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema_view, extend_schema

from .models import *
from .serializers import *


# Puedes aplicar el mismo decorador para cada ViewSet
@extend_schema_view(
    list=extend_schema(summary="Listar", tags=["Postventa"]),
    retrieve=extend_schema(summary="Detalle", tags=["Postventa"]),
    create=extend_schema(summary="Crear", tags=["Postventa"]),
    update=extend_schema(summary="Actualizar", tags=["Postventa"]),
    partial_update=extend_schema(summary="Actualizar Parcial", tags=["Postventa"]),
    destroy=extend_schema(summary="Eliminar", tags=["Postventa"]),
)
class RecintoViewSet(viewsets.ModelViewSet):
    queryset = Recinto.objects.all()
    serializer_class = RecintoSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(summary="Listar", tags=["Postventa"]),
    retrieve=extend_schema(summary="Detalle", tags=["Postventa"]),
    create=extend_schema(summary="Crear", tags=["Postventa"]),
    update=extend_schema(summary="Actualizar", tags=["Postventa"]),
    partial_update=extend_schema(summary="Actualizar Parcial", tags=["Postventa"]),
    destroy=extend_schema(summary="Eliminar", tags=["Postventa"]),
)
class LugarViewSet(viewsets.ModelViewSet):
    queryset = Lugar.objects.all()
    serializer_class = LugarSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(summary="Listar", tags=["Postventa"]),
    retrieve=extend_schema(summary="Detalle", tags=["Postventa"]),
    create=extend_schema(summary="Crear", tags=["Postventa"]),
    update=extend_schema(summary="Actualizar", tags=["Postventa"]),
    partial_update=extend_schema(summary="Actualizar Parcial", tags=["Postventa"]),
    destroy=extend_schema(summary="Eliminar", tags=["Postventa"]),
)
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(summary="Listar", tags=["Postventa"]),
    retrieve=extend_schema(summary="Detalle", tags=["Postventa"]),
    create=extend_schema(summary="Crear", tags=["Postventa"]),
    update=extend_schema(summary="Actualizar", tags=["Postventa"]),
    partial_update=extend_schema(summary="Actualizar Parcial", tags=["Postventa"]),
    destroy=extend_schema(summary="Eliminar", tags=["Postventa"]),
)
class ProblemaViewSet(viewsets.ModelViewSet):
    queryset = Problema.objects.all()
    serializer_class = ProblemaSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(summary="Listar", tags=["Postventa"]),
    retrieve=extend_schema(summary="Detalle", tags=["Postventa"]),
    create=extend_schema(summary="Crear", tags=["Postventa"]),
    update=extend_schema(summary="Actualizar", tags=["Postventa"]),
    partial_update=extend_schema(summary="Actualizar Parcial", tags=["Postventa"]),
    destroy=extend_schema(summary="Eliminar", tags=["Postventa"]),
)
class EspecialidadViewSet(viewsets.ModelViewSet):
    queryset = Especialidad.objects.all()
    serializer_class = EspecialidadSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(summary="Listar", tags=["Postventa"]),
    retrieve=extend_schema(summary="Detalle", tags=["Postventa"]),
    create=extend_schema(summary="Crear", tags=["Postventa"]),
    update=extend_schema(summary="Actualizar", tags=["Postventa"]),
    partial_update=extend_schema(summary="Actualizar Parcial", tags=["Postventa"]),
    destroy=extend_schema(summary="Eliminar", tags=["Postventa"]),
)
class CausaViewSet(viewsets.ModelViewSet):
    queryset = Causa.objects.all()
    serializer_class = CausaSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(summary="Listar", tags=["Postventa"]),
    retrieve=extend_schema(summary="Detalle", tags=["Postventa"]),
    create=extend_schema(summary="Crear", tags=["Postventa"]),
    update=extend_schema(summary="Actualizar", tags=["Postventa"]),
    partial_update=extend_schema(summary="Actualizar Parcial", tags=["Postventa"]),
    destroy=extend_schema(summary="Eliminar", tags=["Postventa"]),
)
class AlcanceResponsabilidadViewSet(viewsets.ModelViewSet):
    queryset = AlcanceResponsabilidad.objects.all()
    serializer_class = AlcanceResponsabilidadSerializer
    permission_classes = [IsAuthenticated]


@extend_schema_view(
    list=extend_schema(summary="Listar", tags=["Postventa"]),
    retrieve=extend_schema(summary="Detalle", tags=["Postventa"]),
    create=extend_schema(summary="Crear", tags=["Postventa"]),
    update=extend_schema(summary="Actualizar", tags=["Postventa"]),
    partial_update=extend_schema(summary="Actualizar Parcial", tags=["Postventa"]),
    destroy=extend_schema(summary="Eliminar", tags=["Postventa"]),
)
class RequerimientoPostVentaViewSet(viewsets.ModelViewSet):
    queryset = RequerimientoPostVenta.objects.all()
    serializer_class = RequerimientoPostVentaSerializer
    permission_classes = [IsAuthenticated]
