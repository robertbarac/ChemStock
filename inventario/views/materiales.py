from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from inventario.models import Material
from sedes.models import Sede, Espacio

def materiales_list_view(request):
    query = request.GET.get("q", "").strip()
    categoria = request.GET.get("categoria", "")
    sede_id = request.GET.get("sede", "")
    espacio_id = request.GET.get("espacio", "")
    estado = request.GET.get("estado", "")

    materiales = Material.objects.select_related("espacio__sede")

    if query:
        materiales = materiales.filter(
            Q(nombre__icontains=query) |
            Q(ubicacion_interna__icontains=query) |
            Q(observaciones__icontains=query)
        )

    if categoria:
        materiales = materiales.filter(categoria=categoria)

    if sede_id:
        materiales = materiales.filter(espacio__sede_id=sede_id)

    if espacio_id:
        materiales = materiales.filter(espacio_id=espacio_id)

    if estado:
        materiales = materiales.filter(estado=estado)

    sedes = Sede.objects.all()
    espacios = Espacio.objects.all()

    context = {
        "materiales": materiales.order_by("categoria", "nombre"),
        "sedes": sedes,
        "espacios": espacios,
        "query": query,
        "selected_categoria": categoria,
        "selected_sede": sede_id,
        "selected_espacio": espacio_id,
        "selected_estado": estado,
    }
    return render(request, "inventario/materiales_list.html", context)
