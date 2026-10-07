import re
from pathlib import Path
from datetime import datetime, date
from django.core.management.base import BaseCommand
import openpyxl

from sedes.models import Sede, Espacio
from inventario.models import Marca, Reactivo, Equipo, Material

class Command(BaseCommand):
    help = "Importa y normaliza el Excel GIQYMA hacia los modelos directos y limpios con Marca"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file",
            type=str,
            default="../6. Inventario Laboratorio 109 CREAD.xlsx",
            help="Ruta al archivo Excel de inventario"
        )

    def handle(self, *args, **options):
        excel_path = Path(options["file"])
        if not excel_path.exists():
            alt = Path("/home/robertbarac/giqyma/inventario/6. Inventario Laboratorio 109 CREAD.xlsx")
            if alt.exists():
                excel_path = alt
            else:
                self.stderr.write(f"Archivo no encontrado en {excel_path} ni en {alt}")
                return

        self.stdout.write(f"Cargando archivo: {excel_path}")
        wb = openpyxl.load_workbook(excel_path, data_only=True)

        # 1. Sedes y Espacios
        self.stdout.write("1. Creando Sedes y Espacios...")
        sede_cread, _ = Sede.objects.get_or_create(
            nombre="CREAD",
            defaults={"descripcion": "Sede CREAD (Centro de Recursos para la Educación Abierta y a Distancia)"}
        )
        sede_zarago, _ = Sede.objects.get_or_create(
            nombre="Zaragocilla",
            defaults={"descripcion": "Campus Zaragocilla - Facultad de Medicina / Ciencias de la Salud"}
        )

        lab_109, _ = Espacio.objects.get_or_create(
            sede=sede_cread,
            nombre="Laboratorio 109",
            defaults={"tipo": "laboratorio"}
        )
        lab_toxi, _ = Espacio.objects.get_or_create(
            sede=sede_zarago,
            nombre="Laboratorio de Toxicología",
            defaults={"tipo": "laboratorio"}
        )
        ofic_estud, _ = Espacio.objects.get_or_create(
            sede=sede_zarago,
            nombre="Oficina de Estudiantes",
            defaults={"tipo": "oficina"}
        )

        def parse_date(val):
            if isinstance(val, (datetime, date)):
                return val.date() if isinstance(val, datetime) else val
            if isinstance(val, str) and val.strip():
                try:
                    return datetime.strptime(val.strip()[:10], "%Y-%m-%d").date()
                except Exception:
                    pass
            return None

        def get_marca(marca_name):
            if not marca_name or not str(marca_name).strip():
                return None
            clean_name = str(marca_name).strip()
            # Normalizar pequeñas variaciones de mayúsculas/espacios
            marca_obj, _ = Marca.objects.get_or_create(nombre=clean_name)
            return marca_obj

        # 2. Hoja "Estandar"
        self.stdout.write("2. Importando Estándares Analíticos...")
        ws_est = wb["Estandar"]
        for row in list(ws_est.iter_rows(values_only=True))[1:]:
            if not row or not row[0]:
                continue
            Reactivo.objects.create(
                espacio=lab_109,
                tipo="ESTANDAR",
                nombre=str(row[0]).strip(),
                marca=get_marca(row[1]),
                presentacion=str(row[2]).strip() if row[2] else "",
                lote=str(row[3]).strip() if row[3] else "",
                referencia=str(row[4]).strip() if row[4] else "",
                fecha_expedicion=parse_date(row[5]),
                cantidad=str(row[6]).strip() if row[6] else "",
                estado_uso=str(row[7]).strip() if row[7] else "Sin uso",
                unidades=str(row[8]).strip() if row[8] else "1",
            )

        # 3. Hoja "Buffer" (sin lote)
        self.stdout.write("3. Importando Soluciones Buffer (sin campo lote)...")
        ws_buf = wb["Buffer"]
        for row in list(ws_buf.iter_rows(values_only=True))[1:]:
            if not row or not row[0]:
                continue
            Reactivo.objects.create(
                espacio=lab_109,
                tipo="BUFFER",
                nombre=str(row[0]).strip(),
                marca=get_marca(row[1]),
                presentacion=str(row[2]).strip() if row[2] else "",
                lote="",
                referencia=str(row[3]).strip() if row[3] else "",
                fecha_expedicion=parse_date(row[4]),
                cantidad=str(row[5]).strip() if row[5] else "",
                estado_uso=str(row[6]).strip() if row[6] else "Usado",
                unidades=str(row[7]).strip() if len(row) > 7 and row[7] else "1",
            )

        # 4. Hoja "Reactivos"
        self.stdout.write("4. Importando Reactivos y Solventes...")
        ws_rea = wb["Reactivos"]
        for row in list(ws_rea.iter_rows(values_only=True))[1:]:
            if not row or not row[0]:
                continue
            Reactivo.objects.create(
                espacio=lab_109,
                tipo="REACTIVO",
                nombre=str(row[0]).strip(),
                marca=get_marca(row[1]),
                presentacion=str(row[2]).strip() if row[2] else "",
                lote=str(row[3]).strip() if row[3] else "",
                referencia=str(row[4]).strip() if row[4] else "",
                fecha_expedicion=parse_date(row[5]),
                cantidad=str(row[6]).strip() if row[6] else "",
                estado_uso=str(row[7]).strip() if row[7] else "Usado",
                unidades=str(row[8]).strip() if row[8] else "1",
                clasificacion=str(row[9]).strip() if len(row) > 9 and row[9] else "",
            )

        # 5. Hoja "Equipos" (con Marca FK y Fotografía)
        self.stdout.write("5. Importando Equipos de Laboratorio...")
        ws_eq = wb["Equipos"]
        for row in list(ws_eq.iter_rows(values_only=True))[1:]:
            if not row or not row[0]:
                continue
            cant_val = int(str(row[2]).strip()) if row[2] and str(row[2]).strip().isdigit() else 1
            Equipo.objects.create(
                espacio=lab_109,
                nombre=str(row[0]).strip(),
                marca=get_marca(row[1]),
                cantidad=cant_val,
                estado=str(row[3]).strip() if row[3] else "Usado",
            )

        # 6. Hoja "Material de muestreo"
        self.stdout.write("6. Importando Material de Muestreo (Sedimentos y Peces)...")
        ws_mue = wb["Material de muestreo"]
        for row in list(ws_mue.iter_rows(values_only=True))[2:]:
            if row[0]:
                Material.objects.create(
                    espacio=lab_109,
                    categoria="MUESTREO_SEDIMENTOS",
                    nombre=str(row[0]).strip(),
                    cantidad=str(row[1]).strip() if row[1] else "1",
                    estado=str(row[2]).strip() if row[2] else "Sin uso",
                )
            if len(row) > 5 and row[5]:
                Material.objects.create(
                    espacio=lab_109,
                    categoria="MUESTREO_PECES",
                    nombre=str(row[5]).strip(),
                    cantidad=str(row[6]).strip() if row[6] else "1",
                    estado=str(row[7]).strip() if len(row) > 7 and row[7] else "Usado",
                )

        # 7. Hoja "Materiales varios"
        self.stdout.write("7. Importando Material de Vidrio, Limpieza y Varios...")
        ws_var = wb["Materiales varios"]
        for row in list(ws_var.iter_rows(values_only=True))[2:]:
            if row[0]:
                Material.objects.create(
                    espacio=lab_109,
                    categoria="VIDRIO",
                    nombre=str(row[0]).strip(),
                    cantidad=str(row[1]).strip() if row[1] else "1",
                    estado=str(row[2]).strip() if row[2] else "Usado",
                )
            if len(row) > 5 and row[5]:
                Material.objects.create(
                    espacio=lab_109,
                    categoria="LIMPIEZA",
                    nombre=str(row[5]).strip(),
                    cantidad=str(row[6]).strip() if row[6] else "1",
                    estado=str(row[7]).strip() if len(row) > 7 and row[7] else "Sin uso",
                )
            if len(row) > 10 and row[10]:
                Material.objects.create(
                    espacio=lab_109,
                    categoria="VARIOS",
                    nombre=str(row[10]).strip(),
                    cantidad=str(row[11]).strip() if row[11] else "1",
                    estado=str(row[12]).strip() if len(row) > 12 and row[12] else "Sin uso",
                )

        # 8. Hoja "Material M.humano"
        self.stdout.write("8. Importando Material de Muestreo Humano / Biomédico...")
        ws_hum = wb["Material M.humano"]
        for row in list(ws_hum.iter_rows(values_only=True))[2:]:
            if not row or not row[0]:
                continue
            Material.objects.create(
                espacio=lab_109,
                categoria="BIOMEDICO",
                nombre=str(row[0]).strip(),
                cantidad=str(row[1]).strip() if row[1] else "0",
                estado=str(row[2]).strip() if row[2] else "Sin uso",
            )

        self.stdout.write(self.style.SUCCESS("¡IMPORTACIÓN COMPLETADA CON ÉXITO!"))
        self.stdout.write(f"- Sedes: {Sede.objects.count()}")
        self.stdout.write(f"- Espacios: {Espacio.objects.count()}")
        self.stdout.write(f"- Marcas registradas: {Marca.objects.count()}")
        self.stdout.write(f"- Reactivos, Estándares y Buffers: {Reactivo.objects.count()}")
        self.stdout.write(f"- Equipos de Laboratorio: {Equipo.objects.count()}")
        self.stdout.write(f"- Materiales e Insumos: {Material.objects.count()}")
