from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Marca, Reactivo, Equipo, ImagenEquipo, Material, Movimiento

admin.site.site_header = "GIQYMA - Inventario de Laboratorios UDC"
admin.site.site_title = "GIQYMA Inventario"
admin.site.index_title = "Gestión de Inventario y Sedes"

class BaseAuditAdmin(admin.ModelAdmin):
    """Clase base para registrar automáticamente el usuario creador en auditoría."""
    readonly_fields = ("creado_por", "fecha_registro")

    def save_model(self, request, obj, form, change):
        if not obj.creado_por:
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)


@admin.register(Marca)
class MarcaAdmin(BaseAuditAdmin):
    list_display = ("nombre", "pais_origen", "total_reactivos", "total_equipos", "creado_por", "fecha_registro")
    search_fields = ("nombre", "pais_origen")
    list_filter = ("creado_por",)

    def total_reactivos(self, obj):
        return obj.reactivos.count()
    total_reactivos.short_description = "Reactivos / Estándares"

    def total_equipos(self, obj):
        return obj.equipos.count()
    total_equipos.short_description = "Equipos"


@admin.register(Reactivo)
class ReactivoAdmin(BaseAuditAdmin):
    list_display = (
        "nombre", "tipo_badge", "marca", "lote", "cantidad",
        "unidades", "estado_badge", "espacio", "creado_por"
    )
    list_filter = ("tipo", "marca", "estado_uso", "espacio__sede", "espacio", "creado_por")
    search_fields = ("nombre", "marca__nombre", "lote", "referencia", "clasificacion")

    def tipo_badge(self, obj):
        colors = {
            "ESTANDAR": "#6f42c1",
            "BUFFER": "#0d6efd",
            "REACTIVO": "#198754",
        }
        color = colors.get(obj.tipo, "#333")
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 7px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            color, obj.get_tipo_display()
        )
    tipo_badge.short_description = "Tipo"

    def estado_badge(self, obj):
        colors = {
            "Sin uso": "#198754",
            "Usado": "#fd7e14",
            "En uso": "#0dcaf0",
            "Agotado": "#dc3545",
        }
        color = colors.get(obj.estado_uso, "#6c757d")
        text_color = "black" if obj.estado_uso == "En uso" else "white"
        return format_html(
            '<span style="background-color: {}; color: {}; padding: 2px 7px; border-radius: 4px; font-weight: bold; font-size: 11px;">{}</span>',
            color, text_color, obj.estado_uso
        )
    estado_badge.short_description = "Estado"


class ImagenEquipoInline(admin.TabularInline):
    """Permite añadir y gestionar múltiples fotografías directamente desde la ficha del equipo."""
    model = ImagenEquipo
    extra = 3
    fields = ("foto_preview", "imagen", "descripcion", "es_principal")
    readonly_fields = ("foto_preview",)

    def foto_preview(self, obj):
        if obj.pk and obj.imagen:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px; border: 1px solid #ccc;" /></a>',
                obj.imagen.url, obj.imagen.url
            )
        return mark_safe('<span style="color: #aaa; font-size: 11px;">Nueva imagen</span>')
    foto_preview.short_description = "Vista previa"


@admin.register(Equipo)
class EquipoAdmin(BaseAuditAdmin):
    list_display = ("foto_thumbnail", "nombre", "marca", "cantidad", "estado", "espacio", "total_fotos_badge", "placa_udc", "creado_por")
    list_filter = ("estado", "marca", "espacio__sede", "espacio", "creado_por")
    search_fields = ("nombre", "marca__nombre", "placa_udc", "numero_serie")
    inlines = [ImagenEquipoInline]

    fieldsets = (
        ("Información General del Equipo", {
            "fields": ("espacio", "nombre", "marca", "cantidad", "estado", "placa_udc", "numero_serie", "ubicacion_interna", "observaciones")
        }),
        ("Foto de Portada Base (Opcional)", {
            "description": "Puedes subir una foto rápida aquí, o usar la Galería de Imágenes abajo para añadir múltiples fotos con descripciones.",
            "fields": ("fotografia",)
        }),
        ("Auditoría", {
            "fields": ("creado_por", "fecha_registro"),
            "classes": ("collapse",)
        }),
    )

    def foto_thumbnail(self, obj):
        img = obj.imagen_destacada
        if img:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px; border: 1px solid #ccc;" />',
                img.url
            )
        return mark_safe('<span style="color: #999; font-size: 12px;">Sin foto</span>')
    foto_thumbnail.short_description = "Portada"

    def total_fotos_badge(self, obj):
        count = obj.imagenes.count()
        if count == 0 and obj.fotografia:
            count = 1
        color = "#0a3d62" if count > 1 else "#6c757d"
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 7px; border-radius: 10px; font-size: 11px; font-weight: bold;"><i class="bi bi-images"></i> {} foto{}</span>',
            color, count, "s" if count != 1 else ""
        )
    total_fotos_badge.short_description = "Fotos"


@admin.register(ImagenEquipo)
class ImagenEquipoAdmin(admin.ModelAdmin):
    list_display = ("foto_preview", "equipo", "descripcion", "es_principal", "fecha_subida")
    list_filter = ("es_principal", "equipo__espacio")
    search_fields = ("equipo__nombre", "descripcion")

    def foto_preview(self, obj):
        if obj.imagen:
            return format_html(
                '<a href="{}" target="_blank"><img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 6px;" /></a>',
                obj.imagen.url, obj.imagen.url
            )
        return mark_safe('<span style="color: #999; font-size: 11px;">Sin imagen</span>')
    foto_preview.short_description = "Foto"


@admin.register(Material)
class MaterialAdmin(BaseAuditAdmin):
    list_display = ("nombre", "categoria_badge", "cantidad", "estado", "espacio", "ubicacion_interna", "creado_por")
    list_filter = ("categoria", "estado", "espacio__sede", "espacio", "creado_por")
    search_fields = ("nombre", "ubicacion_interna", "observaciones")

    def categoria_badge(self, obj):
        return format_html(
            '<span style="background-color: #f0f2f5; color: #333; border: 1px solid #ccc; padding: 2px 6px; border-radius: 4px; font-size: 11px;">{}</span>',
            obj.get_categoria_display()
        )
    categoria_badge.short_description = "Categoría"


@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ("fecha_hora", "tipo", "item_descripcion", "cantidad", "proyecto", "usuario", "espacio_origen", "espacio_destino")
    list_filter = ("tipo", "fecha_hora", "usuario")
    search_fields = ("item_descripcion", "proyecto", "usuario__username", "observaciones")
    readonly_fields = ("fecha_hora",)

    def save_model(self, request, obj, form, change):
        if not obj.usuario:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)
