from django.db import models
from utils_project.choices import *
# Create your models here.

class Nacionalidade(models.Model):
    id_nacionalidad = models.AutoField(primary_key=True)
    nombre_nacionalidad = models.CharField(max_length=100)

    class Meta:
        db_table = 'nacionalidade'
        verbose_name = 'Nacionalidade'
        verbose_name_plural = 'Nacionalidades'

    def __str__(self):
        return self.nombre_nacionalidad

class AreaProfesion(models.Model):
    id_area_profesion = models.AutoField(primary_key=True)
    nombre_area_profesion = models.CharField(max_length=100)

    class Meta:
        db_table = 'area_profesion'
        verbose_name = 'Area de Profesion'
        verbose_name_plural = 'Areas de Profesion'
        # unique_together = ('id_area_profesion', 'nombre_area_profesion')
    def __str__(self):
        return self.nombre_area_profesion



class Profesione(models.Model):
    id_profesione = models.AutoField(primary_key=True)
    id_area_profesion = models.ForeignKey(AreaProfesion, on_delete=models.CASCADE)
    nombre_profesione = models.CharField(max_length=100)

    class Meta:
        db_table = 'profesione'
        verbose_name = 'Profesione'
        verbose_name_plural = 'Profesiones'

    def __str__(self):
        return self.nombre_profesione


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    tipo_cliente = models.CharField(choices=CLIENTES_CHOICES, max_length=50, default=CLIENTES_CHOICES[0][0])
    rut_cliente = models.CharField(verbose_name="Rut Cliente", max_length=50)
    id_nacionalidad = models.ForeignKey(Nacionalidade, verbose_name="Nacionalidad",
                                        on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField(verbose_name="Fecha nacimiento")
    genero = models.CharField(verbose_name="Género", max_length=30, choices=SEXO_CHOICES, default=sin_definir)
    region = models.CharField(verbose_name="Región", max_length=31, choices=REGIONES_CHOICES, default=iv_reg_coquimbo)
    nombres_cliente = models.CharField(verbose_name="Nombres", max_length=50)
    apellidos_cliente = models.CharField(verbose_name="Apellidos", max_length=50)
    correo = models.EmailField(verbose_name="Correo")
    telefono = models.CharField(verbose_name="Teléfono", max_length=9)
    renta = models.IntegerField(verbose_name="Renta")
    id_profesion = models.ForeignKey(Profesione, verbose_name="Profesión", on_delete=models.CASCADE)  # PENDIENTE



    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_cliente']
    def __str__(self):
        return str(self.rut_cliente)+ " - " +str(self.nombres_cliente)+ " - " +str(self.apellidos_cliente)