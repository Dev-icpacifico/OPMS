from django.db import models
from gestion_clientes.models import Cliente
# from gestion_contable.models import Bancos
from gestion_propiedad.models import Propiedade
from utils_project.choices import *

# Create your models here.


class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)
    fecha_venta = models.DateField(auto_now=True)
    id_propiedad = models.ForeignKey(Propiedade, on_delete=models.CASCADE)
    tipo_venta = models.CharField(verbose_name="Tipo de venta", choices=TIPO_VENTA_CHOICES, max_length=50, default=VENTAS_CHOICES[0][0])
    estado_venta = models.CharField(verbose_name='Estado Venta', choices=VENTAS_CHOICES, max_length=50, default=VENTAS_CHOICES[0][0])
    fecha_promesa = models.DateField(verbose_name='Fecha de promesa')
    ejecutivo = models.CharField(verbose_name='Ejecutivo', max_length=50, blank=True, null=True)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    bono_pie = models.FloatField(verbose_name='Bon Pie', blank=True, null=True)
    uf_por_m2 = models.FloatField(verbose_name='UF Por M2', blank=True, null=True)
    motivo_compra = models.TextField(verbose_name='Motivo Compra', blank=True, null=True)
    atributos = models.TextField(verbose_name='Atributos', blank=True, null=True)
    ggoo = models.IntegerField(verbose_name='Gastos Operacionales', blank=True, null=True)


    class Meta:
        db_table = 'venta'
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_venta']
    def __str__(self):
        return str(self.id_venta)+ " - " +str(self.id_propiedad.numero_propiedad)


class Etapas(models.Model):
    id_etapa = models.AutoField(primary_key=True)
    nombre_etapa = models.CharField(verbose_name='Nombre Etapa', max_length=50, blank=True, null=True)
    alias_etapa = models.CharField(verbose_name='Alias Etapa', max_length=50, blank=True, null=True)
    descripcion_etapa = models.TextField(verbose_name='Descripcion Etapa', blank=True, null=True)

    class Meta:
        db_table = 'etapas'
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
        # unique_together = (('partida', 'id'),)
        ordering = ['id_etapa']

    def __str__(self):
        return str(self.id_etapa) + " - " + str(self.alias_etapa)


class VentaEtapa(models.Model):
    id_venta_etapa = models.AutoField(primary_key=True)
    id_etapa = models.ForeignKey(Etapas, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    fecha_inicio = models.DateField(verbose_name='Fecha de Inicio', blank=True, null=True)
    fecha_fin = models.DateField(verbose_name='Fecha de Fin', blank=True, null=True)



    class Meta:
        db_table = 'venta_etapas'
        verbose_name = 'Venta Etapa'
        verbose_name_plural = 'Ventas Etapas'
        # unique_together = (('partida', 'id'),)
        ordering = ['id_venta_etapa']

    def __str__(self):
        return str(self.id_venta_etapa)


class CampoEtapa(models.Model):
    id_campo_etapa = models.AutoField(primary_key=True)
    id_etapa = models.ForeignKey(Etapas, on_delete=models.CASCADE)
    nombre_campo = models.CharField(verbose_name='Nombre Campo', max_length=50, blank=True, null=True)
    tipo_dato = models.CharField(verbose_name='Tipo de Datos', max_length=50, blank=True, null=True)
    obligatorio = models.BooleanField(verbose_name='Obligatorio', default=False)
    descripcion_campo = models.TextField(verbose_name='Descripcion Campo', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'campo_etapas'
        verbose_name = 'Campo Etapa'
        verbose_name_plural = 'Campos Etapas'
        ordering = ['id_etapa']
        # unique_together = (('id_etapa', 'nombre_campo'),)

    def __str__(self):
        return str(self.id_campo_etapa) + " - " + str(self.nombre_campo)


class ValoresEtapa(models.Model):
    id_valores_etapa= models.AutoField(primary_key=True)
    id_venta_etapa = models.ForeignKey(VentaEtapa, on_delete=models.CASCADE)
    id_campo_etapa = models.ForeignKey(CampoEtapa, on_delete=models.CASCADE)
    valor_campo = models.CharField(verbose_name='Valor Campo', max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'valores_etapas'
        verbose_name = 'Valor Etapa'
        verbose_name_plural = 'Valores Etapas'
        ordering = ['id_valores_etapa']

    def __str__(self):
        return str(self.id_valores_etapa)