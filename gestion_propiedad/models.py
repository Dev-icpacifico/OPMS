from django.db import models
from utils_project.choices import PROPIEDAD_CHOICES
# Create your models here.


class Propiedade(models.Model):
    id_propiedad = models.AutoField(primary_key=True)
    estado_propiedad = models.CharField(verbose_name="Estado Propiedad", choices=PROPIEDAD_CHOICES, max_length=50, default=PROPIEDAD_CHOICES[0][0])
    condominio = models.CharField(verbose_name="Condominio", max_length=50)
    alias_condominio = models.CharField(verbose_name="Alias Condominio", max_length=50)
    etapa = models.CharField(verbose_name="Etapa", max_length=50)
    rol = models.CharField(verbose_name="Rol Propiedad", max_length=50)
    numero_propiedad = models.CharField(verbose_name="Número Propiedad", max_length=3)
    modelo = models.CharField(verbose_name="Modelo Propiedad", max_length=50)


    class Meta:
        db_table = 'propiedades'
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_propiedad']
    def __str__(self):
        return str(self.alias_condominio)+ " - " +str(self.etapa)+ " - " +str(self.numero_propiedad)