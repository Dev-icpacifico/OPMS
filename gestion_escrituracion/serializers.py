from rest_framework import serializers
from .models import Venta, Etapas, VentaEtapa, CampoEtapa, ValoresEtapa


class EtapasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etapas
        fields = '__all__'
        depth = 1


class CampoEtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CampoEtapa
        fields = '__all__'
        depth = 1


class VentaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venta
        fields = '__all__'
        depth = 1


class VentaEtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = VentaEtapa
        fields = '__all__'
        depth = 1


class ValoresEtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValoresEtapa
        fields = '__all__'
        depth = 1
