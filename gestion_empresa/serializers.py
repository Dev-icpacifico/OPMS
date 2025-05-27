from rest_framework import serializers
from .models import *

class EmpresaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empresa
        fields = '__all__'
        depth = 1
