from django.db import models

# Create your models here.


class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    razon_social = models.CharField(verbose_name="Razon Social", max_length=50)
    rut_empresa = models.CharField(verbose_name="Rut Empresa", max_length=50)
    gerente_ventas = models.CharField(verbose_name="Gerente Ventas", max_length=50)
    jefe_operaciones = models.CharField(verbose_name="Jefes Operaciones", max_length=50)
    banco_alzante = models.CharField(verbose_name="Banco Alzante", max_length=50)
    notaria = models.CharField(verbose_name="Notaria", max_length=50)
    banco_transf = models.CharField(verbose_name="Banco Transferencia", max_length=50)
    tipo_cuenta_transf = models.CharField(verbose_name="Tipo de Cuenta", max_length=50)
    num_cuenta_transf = models.CharField(verbose_name="No Cuenta", max_length=50)
    correo_transf = models.CharField(verbose_name="Correo Transferencia", max_length=50)

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        db_table = 'empresas'

    def __str__(self):
        return self.razon_social

