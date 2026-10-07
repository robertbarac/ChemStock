from django.db import models
from django.contrib.auth.models import User
from sedes.models import Espacio
from .marcas import Marca

class Reactivo(models.Model):
    TIPO_CHOICES = [
        ("ESTANDAR", "Estándar"),
        ("BUFFER", "Buffer"),
        ("REACTIVO", "Reactivo"),
    ]
    ESTADO_CHOICES = [
        ("Sin uso", "Sin uso"),
        ("Usado", "Usado"),
        ("En uso", "En uso"),
        ("Agotado", "Agotado"),
    ]
    espacio = models.ForeignKey(
        Espacio, on_delete=models.CASCADE, related_name="reactivos", verbose_name="Espacio / Laboratorio"
    )
    tipo = models.CharField(
        max_length=20, choices=TIPO_CHOICES, default="REACTIVO", verbose_name="Tipo (Estándar/Buffer/Reactivo)"
    )
    nombre = models.CharField(
        max_length=200, verbose_name="Nombre / Sustancia",
        help_text="Ej: Dichloromethane, Pyrene, Ácido sulfúrico 95-97%, Buffer pH 7.00"
    )
    marca = models.ForeignKey(
        Marca, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="reactivos", verbose_name="Marca / Fabricante"
    )
    presentacion = models.CharField(
        max_length=100, blank=True, verbose_name="Presentación",
        help_text="Ej: Líquido, Sólido"
    )
    lote = models.CharField(
        max_length=100, blank=True, verbose_name="Lote",
        help_text="Número de lote (opcional; en Buffers suele no tener)"
    )
    referencia = models.CharField(
        max_length=100, blank=True, verbose_name="Referencia / Catálogo",
        help_text="Ej: Z-014J, Orion 910110, 1007312500"
    )
    fecha_expedicion = models.DateField(
        null=True, blank=True, verbose_name="Fecha de Expedición / Vencimiento"
    )
    cantidad = models.CharField(
        max_length=50, blank=True, verbose_name="Cantidad / Contenido",
        help_text="Ej: 2 mL, 10mg, 475 mL, 2.5L, 4L"
    )
    unidades = models.CharField(
        max_length=20, default="1", verbose_name="Unidades (Frascos)",
        help_text="Número de frascos físicos (ej: 1, 2)"
    )
    estado_uso = models.CharField(
        max_length=30, choices=ESTADO_CHOICES, default="Sin uso", verbose_name="Estado de Uso"
    )
    clasificacion = models.CharField(
        max_length=100, blank=True, verbose_name="Clasificación Química",
        help_text="Ej: ACIDO, SAL, SOLVENTE ORGANICO"
    )
    ubicacion_interna = models.CharField(
        max_length=150, blank=True, verbose_name="Ubicación Interna",
        help_text="Ej: Nevera 1, Congelador -20°C, Gabinete de ácidos"
    )
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    creado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="reactivos_registrados", verbose_name="Registrado por"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Reactivo / Estándar"
        verbose_name_plural = "Reactivos, Estándares y Buffers"
        ordering = ["tipo", "nombre"]

    def __str__(self):
        marca_str = f" ({self.marca.nombre})" if self.marca else ""
        lote_str = f" [Lote: {self.lote}]" if self.lote else ""
        return f"[{self.get_tipo_display()}] {self.nombre}{marca_str}{lote_str}"
