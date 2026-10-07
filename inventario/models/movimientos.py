from django.db import models
from django.contrib.auth.models import User
from sedes.models import Espacio

class Movimiento(models.Model):
    TIPO_CHOICES = [
        ("SALIDA_CONSUMO", "Salida / Consumo"),
        ("INGRESO_COMPRA", "Ingreso / Compra"),
        ("TRASLADO", "Traslado entre Sedes / Espacios"),
        ("ROTURA_BAJA", "Baja por Rotura / Deterioro"),
    ]
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Registrado por / Responsable", related_name="movimientos_registrados"
    )
    tipo = models.CharField(
        max_length=30, choices=TIPO_CHOICES, default="SALIDA_CONSUMO", verbose_name="Tipo de Movimiento"
    )
    item_descripcion = models.CharField(
        max_length=255, verbose_name="Artículo / Reactivo / Material",
        help_text="Nombre del ítem movido"
    )
    cantidad = models.CharField(
        max_length=50, verbose_name="Cantidad Movida", help_text="Ej: 50 mL, 2 cajas, 1 unidad"
    )
    proyecto = models.CharField(
        max_length=150, blank=True, verbose_name="Proyecto / Tesis / Semillero",
        help_text="Proyecto MinCiencias o tesis para el cual se utilizó"
    )
    espacio_origen = models.ForeignKey(
        Espacio, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="movimientos_origen", verbose_name="Espacio Origen"
    )
    espacio_destino = models.ForeignKey(
        Espacio, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="movimientos_destino", verbose_name="Espacio Destino"
    )
    fecha_hora = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora de Registro")
    observaciones = models.TextField(blank=True, verbose_name="Notas / Justificación")

    class Meta:
        verbose_name = "Movimiento de Inventario"
        verbose_name_plural = "Movimientos de Inventario (Kardex)"
        ordering = ["-fecha_hora"]

    def __str__(self):
        return f"[{self.get_tipo_display()}] {self.item_descripcion} ({self.cantidad}) - {self.fecha_hora.strftime('%d/%m/%Y')}"
