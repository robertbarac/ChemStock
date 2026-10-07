from django.db import models
from django.contrib.auth.models import User
from sedes.models import Espacio

class Material(models.Model):
    CATEGORIA_CHOICES = [
        ("MUESTREO_SEDIMENTOS", "Material de Muestreo (Sedimentos)"),
        ("MUESTREO_PECES", "Material de Muestreo (Peces)"),
        ("VIDRIO", "Material de Vidrio"),
        ("LIMPIEZA", "Material de Limpieza"),
        ("BIOMEDICO", "Material Muestreo Humano"),
        ("VARIOS", "Materiales Varios"),
    ]
    ESTADO_CHOICES = [
        ("Sin uso", "Sin uso"),
        ("Usado", "Usado"),
        ("En uso", "En uso"),
        ("No hay", "No hay / Agotado"),
    ]
    espacio = models.ForeignKey(
        Espacio, on_delete=models.CASCADE, related_name="materiales", verbose_name="Espacio / Laboratorio"
    )
    categoria = models.CharField(
        max_length=30, choices=CATEGORIA_CHOICES, verbose_name="Categoría / Tipo de Material"
    )
    nombre = models.CharField(
        max_length=200, verbose_name="Nombre del Artículo / Insumo",
        help_text="Ej: Tubos tapa lila, Balon fondo redondo (1000mL), Algodón, Caba de icopor"
    )
    cantidad = models.CharField(
        max_length=80, verbose_name="Cantidad / Presentación",
        help_text="Ej: 910 unidades, 7 cajas x100, 1/2 Bolsa, 44, 1"
    )
    estado = models.CharField(
        max_length=30, choices=ESTADO_CHOICES, default="Sin uso", verbose_name="Estado"
    )
    ubicacion_interna = models.CharField(
        max_length=150, blank=True, verbose_name="Ubicación Interna",
        help_text="Ej: Estante de vidrio, Gaveta 3, Módulo de bioseguridad"
    )
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    creado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="materiales_registrados", verbose_name="Registrado por"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Material / Insumo"
        verbose_name_plural = "Materiales e Insumos"
        ordering = ["categoria", "nombre"]

    def __str__(self):
        return f"[{self.get_categoria_display()}] {self.nombre} - Cant: {self.cantidad}"
