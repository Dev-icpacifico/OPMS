from django.db import models

# Create your models here.


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    rut_cliente = models.CharField(verbose_name="Rut Cliente", max_length=50)
    nombres_cliente = models.CharField(verbose_name="Nombres", max_length=50)
    apellidos_cliente = models.CharField(verbose_name="Apellidos", max_length=50)
    correo = models.EmailField(verbose_name="Correo")
    telefono = models.CharField(verbose_name="Teléfono", max_length=9)
    renta = models.IntegerField(verbose_name="Renta")


    class Meta:
        db_table = 'clientes'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_cliente']
    def __str__(self):
        return str(self.rut_cliente)+ " - " +str(self.nombres_cliente)+ " - " +str(self.apellidos_cliente)