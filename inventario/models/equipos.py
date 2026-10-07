from django.db import models
from django.contrib.auth.models import User
from sedes.models import Espacio
from .marcas import Marca

class Equipo(models.Model):
    ESTADO_CHOICES = [
        ("Usado", "Usado"),
        ("Sin uso", "Sin uso"),
        ("Operativo", "Operativo"),
        ("En mantenimiento", "En mantenimiento"),
        ("Fuera de servicio", "Fuera de servicio"),
    ]
    espacio = models.ForeignKey(
        Espacio, on_delete=models.CASCADE, related_name="equipos", verbose_name="Espacio / Laboratorio"
    )
    nombre = models.CharField(
        max_length=200, verbose_name="Nombre del Equipo",
        help_text="Ej: Microscopio con adaptación Axiocam, Espectofotometro UV Visible, Liofilizador"
    )
    marca = models.ForeignKey(
        Marca, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="equipos", verbose_name="Marca / Fabricante"
    )
    cantidad = models.IntegerField(
        default=1, verbose_name="Cantidad",
        help_text="Número de unidades (ej: 4 neveras, 1 espectrofotómetro)"
    )
    estado = models.CharField(
        max_length=30, choices=ESTADO_CHOICES, default="Usado", verbose_name="Estado"
    )
    fotografia = models.ImageField(
        upload_to="equipos/", blank=True, null=True, verbose_name="Fotografía Principal",
        help_text="Foto de referencia rápida (también puedes agregar múltiples fotos en la galería abajo)"
    )
    placa_udc = models.CharField(
        max_length=50, blank=True, verbose_name="Placa Activo UDC",
        help_text="Código institucional de activo si aplica"
    )
    numero_serie = models.CharField(
        max_length=100, blank=True, verbose_name="Número de Serie"
    )
    ubicacion_interna = models.CharField(
        max_length=150, blank=True, verbose_name="Ubicación en el Espacio",
        help_text="Ej: Mesón central, Zona de espectrometría"
    )
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    creado_por = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name="equipos_registrados", verbose_name="Registrado por"
    )
    fecha_registro = models.DateTimeField(
        auto_now_add=True, null=True, blank=True, verbose_name="Fecha de Registro"
    )

    class Meta:
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos de Laboratorio"
        ordering = ["nombre"]

    def __str__(self):
        marca_str = f" ({self.marca.nombre})" if self.marca else ""
        return f"{self.nombre}{marca_str} - Cant: {self.cantidad}"

    @property
    def imagen_destacada(self):
        """Retorna la imagen principal de la galería o la fotografía base si existe."""
        foto_galeria = self.imagenes.filter(es_principal=True).first() or self.imagenes.first()
        if foto_galeria and foto_galeria.imagen:
            return foto_galeria.imagen
        if self.fotografia:
            return self.fotografia
        return None

    @property
    def total_imagenes(self):
        """Total de imágenes asociadas en galería más la fotografía base."""
        total = self.imagenes.count()
        if self.fotografia and total == 0:
            return 1
        return total


class ImagenEquipo(models.Model):
    """Permite adjuntar múltiples fotografías a un mismo equipo (placa, accesorios, vistas)."""
    equipo = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name="imagenes", verbose_name="Equipo"
    )
    imagen = models.ImageField(
        upload_to="equipos/galeria/", verbose_name="Fotografía"
    )
    descripcion = models.CharField(
        max_length=150, blank=True, verbose_name="Descripción / Epígrafe",
        help_text="Ej: Vista frontal, Placa de serie, Accesorios, Conexión trasera"
    )
    es_principal = models.BooleanField(
        default=False, verbose_name="¿Es la foto principal de portada?"
    )
    fecha_subida = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha de subida"
    )

    class Meta:
        verbose_name = "Fotografía del Equipo"
        verbose_name_plural = "Galería de Fotografías del Equipo"
        ordering = ["-es_principal", "-fecha_subida"]

    def __str__(self):
        desc = f" ({self.descripcion})" if self.descripcion else ""
        return f"Foto de {self.equipo.nombre}{desc}"
