from django.db import models
from gestion_propiedad.models import Propiedade
from utils_project.choices import POSTVENTA_CHOICES


class Recinto(models.Model):
    id_recinto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    class Meta:
        ordering = ['nombre']


class Lugar(models.Model):
    id_lugar = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    class Meta:
        ordering = ['nombre']


class Item(models.Model):
    id_item = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    class Meta:
        ordering = ['nombre']


class Problema(models.Model):
    id_problema = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=255)

    def __str__(self):
        return self.descripcion
    class Meta:
        ordering = ['descripcion']


class Especialidad(models.Model):
    id_especialidad = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre
    class Meta:
        ordering = ['nombre']


class Causa(models.Model):
    id_causa = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion
    class Meta:
        ordering = ['descripcion']


class AlcanceResponsabilidad(models.Model):
    id_alcanceresponsabilidad = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=200)

    def __str__(self):
        return self.descripcion
    class Meta:
        ordering = ['descripcion']



class RequerimientoPostVenta(models.Model):
    fecha = models.DateField(verbose_name="Fecha ingreso")
    propiedad = models.ForeignKey(Propiedade, on_delete=models.CASCADE, limit_choices_to={'estado_propiedad': 'Entregada'})

    solicitud_cliente = models.TextField(verbose_name="Solicitud del cliente")

    recinto = models.ForeignKey(Recinto, on_delete=models.SET_NULL, null=True)
    lugar = models.ForeignKey(Lugar, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True)
    problema = models.ForeignKey(Problema, on_delete=models.SET_NULL, null=True)
    especialidad = models.ForeignKey(Especialidad, on_delete=models.SET_NULL, null=True)
    causa = models.ForeignKey(Causa, on_delete=models.SET_NULL, null=True)
    alcance_responsabilidad = models.ForeignKey(AlcanceResponsabilidad, on_delete=models.SET_NULL, null=True)

    estado = models.CharField(choices=POSTVENTA_CHOICES,max_length=30, default="Pendiente")
    mo = models.FloatField(default=0)
    materiales = models.FloatField(default=0)
    subcontrato = models.FloatField(default=0)
    total = models.FloatField(default=0)

    comentario = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.fecha} - {self.propiedad} ({self.estado})"

    def save(self, *args, **kwargs):
        self.total = (self.mo or 0) + (self.materiales or 0) + (self.subcontrato or 0)
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'requerimientos_postventa'
        verbose_name = 'Requerimiento de Postventa'
        verbose_name_plural = 'Requerimientos de Postventa'
        ordering = ['-fecha']



