from django.db import models
from django.contrib.auth.models import User
from .sede import Sede

class Espacio(models.Model):
    TIPO_CHOICES = [
        ("laboratorio", "Laboratorio"),
        ("oficina", "Oficina"),
        ("otro", "Otro"),
    ]
    sede = models.ForeignKey(Sede, on_delete=models.CASCADE, related_name="espacios", verbose_name="Sede")
    nombre = models.CharField(
        max_length=150, verbose_name="Nombre del Espacio",
        help_text="Ej: Laboratorio 109, Laboratorio de Toxicología, Oficina de Estudiantes"
    )
    tipo = models.CharField(
        max_length=20, choices=TIPO_CHOICES, default="laboratorio", verbose_name="Tipo de Espacio"
    )
    responsable = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="espacios", verbose_name="Responsable / Custodio"
    )
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")

    class Meta:
        verbose_name = "Espacio"
        verbose_name_plural = "Espacios"
        unique_together = ("sede", "nombre")
        ordering = ["sede", "nombre"]

    def __str__(self):
        return f"{self.nombre} ({self.sede.nombre}) - {self.get_tipo_display()}"
