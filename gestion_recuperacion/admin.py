from django.contrib import admin

from gestion_recuperacion.models import ModelVacio


# Register your models here.
@admin.register(ModelVacio)
class ModelVacioAdmin(admin.ModelAdmin):
    pass