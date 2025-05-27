from rest_framework import serializers
from .models import *

class NacionalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model =Nacionalidade
        fields = '__all__'
        # read_only_fields = ('id',)
        # write_only_fields = ('id',)

class AreaProfesionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaProfesion
        fields = '__all__'

class ProfesioneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profesione
        fields = '__all__'


class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

