from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from inventario.models import Equipo, ImagenEquipo, Marca
from sedes.models import Sede, Espacio

@login_required
def equipos_list_view(request):
    query = request.GET.get("q", "").strip()
    marca_id = request.GET.get("marca", "")
    sede_id = request.GET.get("sede", "")
    espacio_id = request.GET.get("espacio", "")
    estado = request.GET.get("estado", "")

    equipos = Equipo.objects.select_related("espacio__sede", "marca", "creado_por").prefetch_related("imagenes")

    if query:
        equipos = equipos.filter(
            Q(nombre__icontains=query) |
            Q(marca__nombre__icontains=query) |
            Q(placa_udc__icontains=query) |
            Q(numero_serie__icontains=query)
        )

    if marca_id:
        equipos = equipos.filter(marca_id=marca_id)

    if sede_id:
        equipos = equipos.filter(espacio__sede_id=sede_id)

    if espacio_id:
        equipos = equipos.filter(espacio_id=espacio_id)

    if estado:
        equipos = equipos.filter(estado=estado)

    sedes = Sede.objects.all()
    espacios = Espacio.objects.all()
    marcas = Marca.objects.filter(equipos__isnull=False).distinct()

    context = {
        "equipos": equipos.order_by("nombre"),
        "sedes": sedes,
        "espacios": espacios,
        "marcas": marcas,
        "query": query,
        "selected_marca": marca_id,
        "selected_sede": sede_id,
        "selected_espacio": espacio_id,
        "selected_estado": estado,
    }
    return render(request, "inventario/equipos_list.html", context)

@login_required
def equipo_detail_view(request, pk):
    equipo = get_object_or_404(
        Equipo.objects.select_related("espacio__sede", "marca", "creado_por").prefetch_related("imagenes"),
        pk=pk
    )
    return render(request, "inventario/equipo_detail.html", {"equipo": equipo})

@login_required
def subir_fotos_equipo_view(request, pk):
    """Permite subir múltiples imágenes a un equipo directamente desde el sitio web."""
    equipo = get_object_or_404(Equipo, pk=pk)

    if request.method == "POST":
        archivos = request.FILES.getlist("imagenes")
        descripcion = request.POST.get("descripcion", "").strip()

        if not archivos:
            messages.error(request, "Por favor seleccione al menos un archivo de imagen.")
        else:
            subidas = 0
            for f in archivos:
                es_primera = not equipo.imagenes.filter(es_principal=True).exists() and not equipo.fotografia and subidas == 0
                ImagenEquipo.objects.create(
                    equipo=equipo,
                    imagen=f,
                    descripcion=descripcion or f.name,
                    es_principal=es_primera
                )
                subidas += 1

            messages.success(request, f"Se han subido exitosamente {subidas} fotografía(s) a '{equipo.nombre}'.")

    return redirect("inventario:equipo_detail", pk=pk)

@login_required
def eliminar_foto_equipo_view(request, pk):
    """Permite eliminar una fotografía de la galería del equipo desde el sitio web."""
    imagen_obj = get_object_or_404(ImagenEquipo, pk=pk)
    equipo_id = imagen_obj.equipo_id

    if request.method == "POST":
        nombre_foto = imagen_obj.descripcion or "Fotografía"
        imagen_obj.imagen.delete(save=False)
        imagen_obj.delete()
        messages.success(request, f"Se eliminó la foto '{nombre_foto}' del equipo.")

    return redirect("inventario:equipo_detail", pk=equipo_id)

@login_required
def marcar_foto_principal_view(request, pk):
    """Marca una imagen como foto principal / portada del equipo."""
    imagen_obj = get_object_or_404(ImagenEquipo, pk=pk)
    equipo = imagen_obj.equipo

    if request.method == "POST":
        equipo.imagenes.all().update(es_principal=False)
        imagen_obj.es_principal = True
        imagen_obj.save()
        messages.success(request, "Se actualizó la foto principal de portada del equipo.")

    return redirect("inventario:equipo_detail", pk=equipo.id)
