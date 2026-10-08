from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from inventario.models import Movimiento
from sedes.models import Espacio

@login_required
def movimientos_list_view(request):
    tipo = request.GET.get("tipo", "")
    movimientos = Movimiento.objects.select_related("usuario", "espacio_origen", "espacio_destino")

    if tipo:
        movimientos = movimientos.filter(tipo=tipo)

    context = {
        "movimientos": movimientos.order_by("-fecha_hora")[:50],
        "selected_tipo": tipo,
    }
    return render(request, "inventario/movimientos_list.html", context)

@login_required
def registrar_consumo_view(request):
    espacios = Espacio.objects.select_related("sede").all()

    if request.method == "POST":
        item_nombre = request.POST.get("item", "").strip()
        cantidad = request.POST.get("cantidad", "").strip()
        proyecto = request.POST.get("proyecto", "").strip()
        espacio_id = request.POST.get("espacio", "")
        observaciones = request.POST.get("observaciones", "").strip()

        if not item_nombre or not cantidad:
            messages.error(request, "El artículo y la cantidad son requeridos.")
        else:
            espacio_obj = Espacio.objects.filter(pk=espacio_id).first() if espacio_id else None

            Movimiento.objects.create(
                usuario=request.user,
                tipo="SALIDA_CONSUMO",
                item_descripcion=item_nombre,
                cantidad=cantidad,
                proyecto=proyecto,
                espacio_origen=espacio_obj,
                observaciones=observaciones,
            )
            messages.success(request, f"Salida/consumo de '{item_nombre}' ({cantidad}) registrada correctamente.")
            return redirect("inventario:movimientos_list")

    context = {"espacios": espacios}
    return render(request, "inventario/movimiento_form.html", context)
