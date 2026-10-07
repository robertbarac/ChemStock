from .dashboard import dashboard_view
from .reactivos import reactivos_list_view, reactivo_detail_view
from .equipos import (
    equipos_list_view,
    equipo_detail_view,
    subir_fotos_equipo_view,
    eliminar_foto_equipo_view,
    marcar_foto_principal_view,
)
from .materiales import materiales_list_view
from .movimientos import movimientos_list_view, registrar_consumo_view

__all__ = [
    "dashboard_view",
    "reactivos_list_view",
    "reactivo_detail_view",
    "equipos_list_view",
    "equipo_detail_view",
    "subir_fotos_equipo_view",
    "eliminar_foto_equipo_view",
    "marcar_foto_principal_view",
    "materiales_list_view",
    "movimientos_list_view",
    "registrar_consumo_view",
]
