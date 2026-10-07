from django.db import models
from django.contrib.auth.models import User

class Marca(models.Model):
    nombre = models.CharField(max_length=120, unique=True, verbose_name="Nombre de la Marca")
    pais_origen = models.CharField(max_length=80, blank=True, verbose_name="País de Origen")
    descripcion = models.TextField(blank=True, verbose_name="Descripción / Notas")
    creado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="marcas_registradas", verbose_name="Registrado por"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
