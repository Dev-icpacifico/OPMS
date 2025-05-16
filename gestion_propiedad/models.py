from django.db import models
from utils_project.choices import *
from django.core.exceptions import ValidationError

# Create your models here.

def validar_positivo(value):
    if value < 0:
        raise ValidationError('El valor debe ser un número positivo mayor o igual a 0.')


class Condominio(models.Model):
    id_condominio = models.AutoField(primary_key=True)
    nombre_condominio = models.CharField(verbose_name="Nombre", max_length=100)
    alias_condominio = models.CharField(verbose_name="Alias Condominio", max_length=50)
    fecha_venta_condominio = models.DateField(verbose_name="Fecha Venta Condominio", null=True, blank=True)
    direccion_proyecto = models.CharField(verbose_name="Dirección", max_length=100)
    estado_condominio = models.CharField(verbose_name="Estado",max_length=30, choices=IS_DISPONIBLE_CHOICES, default=IS_DISPONIBLE_CHOICES[0][0])

    # vivienda_social = models.CharField(verbose_name="Estado",max_length=30, choices=SI_NO_CHOICES, default=no)

    def __str__(self):
        return str(self.id_condominio) + " - " + self.nombre_condominio

    class Meta:
        db_table = 'condominio'
        verbose_name = 'Condominio'
        verbose_name_plural = 'Condominios'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_condominio']


class Etapa(models.Model):
    id_etapa_condominio = models.AutoField(primary_key=True)
    id_condominio = models.ForeignKey(Condominio, verbose_name="Condominio", on_delete=models.CASCADE)
    nombre_etapa = models.CharField(verbose_name= "Nombre",max_length=50)

    def __str__(self):
        return str(self.id_etapa_condominio) + " - " + self.nombre_etapa

    class Meta:
        db_table = "etapa_proyecto"
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
        # unique_together = (('partida', 'id'),)
        ordering = ['id_etapa_condominio']

class SubEtapa(models.Model):
    id_sub_etapa = models.AutoField(primary_key=True)
    etapa = models.ForeignKey(Etapa, verbose_name="Etapa", on_delete=models.CASCADE)
    nombre_sub_etapa = models.CharField(verbose_name= "Nombre Sub Etapa",max_length=4)

    def __str__(self):
        return str(self.id_sub_etapa) + " - " + self.etapa.nombre_etapa + " - " + self.nombre_sub_etapa

    class Meta:
        db_table = "sub_etapa_proyecto"
        verbose_name = 'Sub Etapa'
        verbose_name_plural = 'Sub Etapas'
        # unique_together = (('partida', 'id'),)
        ordering = ['id_sub_etapa']

class Torre(models.Model):
    id_torre = models.AutoField(primary_key=True)
    id_etapa_condominio = models.ForeignKey(Etapa, verbose_name="Etapa", on_delete=models.CASCADE)
    estado_torre = models.CharField(verbose_name="Estado", max_length=30, choices=IS_DISPONIBLE_CHOICES, default=disponible)
    nombre_torre = models.CharField(verbose_name="Nombre", max_length=50)

    def __str__(self):
        return "(" + str(self.id_torre) + ")" + " - " + self.nombre_torre

    class Meta:
        db_table = "torre"
        verbose_name = 'Torre'
        verbose_name_plural = 'Torres'
        # unique_together = (('partida', 'id'),)
        ordering = ['id_torre']

class Modelo(models.Model):
    id_modelo = models.AutoField(primary_key=True)
    # id_condominio = models.ForeignKey(Condominio, verbose_name="Condominio", on_delete=models.CASCADE)
    nombre_modelo = models.CharField(verbose_name="Nombre", max_length=4)
    programa_modelo = models.CharField(verbose_name="Programa", max_length=10)
    estado_modelo = models.CharField(verbose_name="Estado",max_length=30, choices=IS_DISPONIBLE_CHOICES, default=disponible)



    def __str__(self):
        return "(" + str(self.id_modelo) + ")" + " - " + self.nombre_modelo

    class Meta:
        db_table = "modelo"
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'
        # unique_together = (('partida', 'id'),)
        ordering = ['id_modelo']


class Propiedade(models.Model):
    id_propiedad = models.AutoField(primary_key=True)
    estado_propiedad = models.CharField(verbose_name="Estado Propiedad", choices=PROPIEDAD_CHOICES, max_length=50, default=PROPIEDAD_CHOICES[0][0])
    condominio = models.ForeignKey(Condominio, verbose_name="Condominio", on_delete=models.CASCADE)
    etapa = models.ForeignKey(Etapa, verbose_name="Etapa", on_delete=models.CASCADE )
    rol = models.CharField(verbose_name="Rol Propiedad", max_length=50)
    numero_propiedad = models.CharField(verbose_name="Número Propiedad", max_length=3)
    modelo = models.ForeignKey(Modelo, verbose_name="Modelo", on_delete=models.CASCADE)

    ori_vivienda = models.CharField(verbose_name="Orientación", max_length=30, choices=ORIENTACION_VIVIENDA,
                                    default=norte)
    estado_vivienda = models.CharField(verbose_name="Estado vivienda", max_length=30, choices=IS_DISPONIBLE_CHOICES,
                                       default=disponible)
    piso = models.CharField(verbose_name="Piso", max_length=30, choices=PISO, default=uno)
    metros_vivienda = models.FloatField(verbose_name="Metros depto", validators=[validar_positivo])
    metros_terraza_vivienda = models.FloatField(verbose_name="Metros terraza", validators=[validar_positivo])
    metros_total_vivienda = models.FloatField(verbose_name="Metros total", validators=[validar_positivo])
    bono_vivienda = models.FloatField(verbose_name="% Descuento", null=True, blank=True)
    prorrateo_vivienda = models.FloatField(verbose_name="% Prorrateo", validators=[validar_positivo])
    estacionamiento = models.CharField(verbose_name="Estacionamiento", max_length=5)
    bodega = models.CharField(verbose_name="Bodega", max_length=5)
    m2_bodega = models.CharField(verbose_name="M2 Bodega", max_length=5)
    valor_inicial_vivienda = models.FloatField(verbose_name="Valor Inicial", validators=[validar_positivo])
    valor_inicial_final = models.FloatField(verbose_name="Valor Final", validators=[validar_positivo])
    valor_cchc = models.FloatField(verbose_name="Precio CCHC", validators=[validar_positivo])
    campagna_dscto = models.FloatField(verbose_name="Campaña dscto", validators=[validar_positivo])
    valor_dscto = models.FloatField(verbose_name="UF Dscto", validators=[validar_positivo])


    class Meta:
        db_table = 'propiedades'
        verbose_name = 'Propiedad'
        verbose_name_plural = 'Propiedades'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_propiedad']

    def __str__(self):
        return str(self.id_propiedad)+ " - " +str(self.numero_propiedad)+ " - " +str(self.condominio.alias_condominio)+ " - " +str(self.etapa.nombre_etapa)