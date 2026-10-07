from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from inventario.models import Reactivo, Marca
from sedes.models import Sede, Espacio

def reactivos_list_view(request):
    query = request.GET.get("q", "").strip()
    tipo = request.GET.get("tipo", "")
    marca_id = request.GET.get("marca", "")
    sede_id = request.GET.get("sede", "")
    espacio_id = request.GET.get("espacio", "")
    estado = request.GET.get("estado", "")

    reactivos = Reactivo.objects.select_related("espacio__sede", "marca")

    if query:
        reactivos = reactivos.filter(
            Q(nombre__icontains=query) |
            Q(marca__nombre__icontains=query) |
            Q(lote__icontains=query) |
            Q(referencia__icontains=query) |
            Q(clasificacion__icontains=query)
        )

    if tipo:
        reactivos = reactivos.filter(tipo=tipo)

    if marca_id:
        reactivos = reactivos.filter(marca_id=marca_id)

    if sede_id:
        reactivos = reactivos.filter(espacio__sede_id=sede_id)

    if espacio_id:
        reactivos = reactivos.filter(espacio_id=espacio_id)

    if estado:
        reactivos = reactivos.filter(estado_uso=estado)

    sedes = Sede.objects.all()
    espacios = Espacio.objects.all()
    marcas = Marca.objects.filter(reactivos__isnull=False).distinct()

    context = {
        "reactivos": reactivos.order_by("tipo", "nombre"),
        "sedes": sedes,
        "espacios": espacios,
        "marcas": marcas,
        "query": query,
        "selected_tipo": tipo,
        "selected_marca": marca_id,
        "selected_sede": sede_id,
        "selected_espacio": espacio_id,
        "selected_estado": estado,
    }
    return render(request, "inventario/reactivos_list.html", context)

def reactivo_detail_view(request, pk):
    reactivo = get_object_or_404(Reactivo.objects.select_related("espacio__sede", "marca"), pk=pk)
    return render(request, "inventario/reactivo_detail.html", {"reactivo": reactivo})
