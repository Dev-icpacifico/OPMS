from rest_framework import serializers
from .models import (
    Recinto, Lugar, Item, Problema, Especialidad,
    Causa, AlcanceResponsabilidad, RequerimientoPostVenta
)

class RecintoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recinto
        fields = '__all__'


class LugarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lugar
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ProblemaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problema
        fields = '__all__'


class EspecialidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Especialidad
        fields = '__all__'


class CausaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Causa
        fields = '__all__'


class AlcanceResponsabilidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlcanceResponsabilidad
        fields = '__all__'


class RequerimientoPostVentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequerimientoPostVenta
        fields = '__all__'
