from django.contrib import admin
from .models import Sede, Espacio

class EspacioInline(admin.TabularInline):
    model = Espacio
    extra = 1

@admin.register(Sede)
class SedeAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ciudad", "total_espacios")
    search_fields = ("nombre", "ciudad")
    inlines = [EspacioInline]

    def total_espacios(self, obj):
        return obj.espacios.count()
    total_espacios.short_description = "Espacios / Labs"

@admin.register(Espacio)
class EspacioAdmin(admin.ModelAdmin):
    list_display = ("nombre", "sede", "tipo", "responsable")
    list_filter = ("tipo", "sede")
    search_fields = ("nombre", "sede__nombre")
