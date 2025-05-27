from rest_framework import serializers
from .models import Condominio, Etapa, SubEtapa, Torre, Modelo, Propiedade

class CondominioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Condominio
        fields = '__all__'

class EtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etapa
        fields = '__all__'

class SubEtapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubEtapa
        fields = '__all__'

class TorreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Torre
        fields = '__all__'

class ModeloSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modelo
        fields = '__all__'

class PropiedadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Propiedade
        fields = '__all__'
