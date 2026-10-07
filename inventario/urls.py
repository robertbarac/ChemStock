from django.urls import path
from . import views

app_name = "inventario"

urlpatterns = [
    path("", views.dashboard_view, name="dashboard"),
    path("reactivos/", views.reactivos_list_view, name="reactivos_list"),
    path("reactivos/<int:pk>/", views.reactivo_detail_view, name="reactivo_detail"),
    path("equipos/", views.equipos_list_view, name="equipos_list"),
    path("equipos/<int:pk>/", views.equipo_detail_view, name="equipo_detail"),
    path("equipos/<int:pk>/subir-fotos/", views.subir_fotos_equipo_view, name="subir_fotos_equipo"),
    path("equipos/fotos/<int:pk>/eliminar/", views.eliminar_foto_equipo_view, name="eliminar_foto_equipo"),
    path("equipos/fotos/<int:pk>/principal/", views.marcar_foto_principal_view, name="marcar_foto_principal"),
    path("materiales/", views.materiales_list_view, name="materiales_list"),
    path("movimientos/", views.movimientos_list_view, name="movimientos_list"),
    path("movimientos/registrar-consumo/", views.registrar_consumo_view, name="registrar_consumo"),
]
