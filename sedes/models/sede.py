from django.db import models

class Sede(models.Model):
    nombre = models.CharField(
        max_length=150, unique=True, verbose_name="Nombre de la Sede",
        help_text="Ej: CREAD, Zaragocilla, San Agustín, Piedra de Bolívar"
    )
    ciudad = models.CharField(max_length=100, default="Cartagena de Indias", verbose_name="Ciudad")
    descripcion = models.TextField(blank=True, verbose_name="Descripción o Ubicación")

    class Meta:
        verbose_name = "Sede"
        verbose_name_plural = "Sedes"
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre
