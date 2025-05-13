from django.db import models

from gestion_escrituracion.models import Venta


# Create your models here.

class Bancos(models.Model):
    id_banco = models.AutoField(primary_key=True)
    nombre_banco = models.CharField(verbose_name="Nombre Banco", max_length=50)

    class Meta:
        db_table = 'banco'
        verbose_name = 'Banco'
        verbose_name_plural = 'Bancos'
        #unique_together = (('partida', 'id'),)
        ordering = ['nombre_banco']
    def __str__(self):
        return str(self.id_banco)+ " - " +str(self.nombre_banco)


class CategoriaPago(models.Model):
    id_categoria_pago = models.AutoField(primary_key=True)
    nombre_categoria_pago = models.CharField(verbose_name="Nombre Categoria", max_length=50)

    class Meta:
        db_table = 'categoria_pago'
        verbose_name = 'Categoria Pago'
        verbose_name_plural = 'Categorias Pagos'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_categoria_pago']
    def __str__(self):
        return str(self.id_categoria_pago)+ " - " +str(self.nombre_categoria_pago)

class FormaPago(models.Model):
    id_forma_pago = models.AutoField(primary_key=True)
    nombre_forma_pago = models.CharField(verbose_name="Nombre Forma", max_length=50)

    class Meta:
        db_table = 'forma_pago'
        verbose_name = 'Forma Pago'
        verbose_name_plural = 'Formas Pagos'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_forma_pago']
    def __str__(self):
        return str(self.id_forma_pago)+ " - " +str(self.nombre_forma_pago)



class Pagos(models.Model):
    id_pago = models.AutoField(primary_key=True)
    id_forma_pago = models.ForeignKey(FormaPago, on_delete=models.CASCADE)
    id_categoria_pago = models.ForeignKey(CategoriaPago, on_delete=models.CASCADE)
    id_banco = models.ForeignKey(Bancos, on_delete=models.CASCADE)
    id_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    estado_pago = models.CharField(verbose_name="Estado Pago", max_length=50)
    num_documento = models.CharField(verbose_name="Numero de Documento", max_length=50)
    fecha_registro_pago = models.DateField(verbose_name="Fecha de registro")
    fecha_real_pago = models.DateField(verbose_name="Fecha contable")
    monto_pago = models.IntegerField(verbose_name="Monto de pago")
    observacion_pago = models.TextField(verbose_name="Observaciones de pago")

    class Meta:
        db_table = 'pagos'
        verbose_name = 'Pago'
        verbose_name_plural = 'Pagos'
        #unique_together = (('partida', 'id'),)
        ordering = ['id_pago']
    def __str__(self):
        return str(self.id_pago)+ " - " +str(self.id_venta)