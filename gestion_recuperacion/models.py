from django.db import models

# Create your models here.


class ModelVacio(models.Model):
    atributo = models.CharField(max_length=100)

    class Meta:
        db_table = 'modelo_vacio'
        verbose_name = 'Modelo Vacio'
        verbose_name_plural = 'Modelos Vacios'