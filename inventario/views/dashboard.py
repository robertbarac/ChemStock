from django.shortcuts import render
from django.utils import timezone
from inventario.models import Reactivo, Equipo, Material, Movimiento
from sedes.models import Sede, Espacio

def dashboard_view(request):
    total_reactivos = Reactivo.objects.count()
    reactivos_en_uso = Reactivo.objects.filter(estado_uso__in=["Usado", "En uso"]).count()
    reactivos_sin_uso = Reactivo.objects.filter(estado_uso="Sin uso").count()

    total_equipos = Equipo.objects.count()
    equipos_operativos = Equipo.objects.filter(estado__in=["Operativo", "Usado", "Sin uso"]).count()

    total_materiales = Material.objects.count()
    materiales_agotados = Material.objects.filter(estado__icontains="No hay").count()

    ultimos_movimientos = Movimiento.objects.select_related("usuario", "espacio_origen", "espacio_destino").order_by("-fecha_hora")[:6]
    sedes = Sede.objects.prefetch_related("espacios").all()

    # Muestras recientes de cada categoría
    ultimos_reactivos = Reactivo.objects.select_related("espacio__sede").order_by("-id")[:5]
    ultimos_equipos = Equipo.objects.select_related("espacio__sede").order_by("-id")[:5]

    context = {
        "total_reactivos": total_reactivos,
        "reactivos_en_uso": reactivos_en_uso,
        "reactivos_sin_uso": reactivos_sin_uso,
        "total_equipos": total_equipos,
        "equipos_operativos": equipos_operativos,
        "total_materiales": total_materiales,
        "materiales_agotados": materiales_agotados,
        "ultimos_movimientos": ultimos_movimientos,
        "sedes": sedes,
        "ultimos_reactivos": ultimos_reactivos,
        "ultimos_equipos": ultimos_equipos,
    }
    return render(request, "inventario/dashboard.html", context)
