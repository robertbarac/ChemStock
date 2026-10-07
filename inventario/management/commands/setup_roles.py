from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from inventario.models import Reactivo, Equipo, ImagenEquipo, Material, Marca, Movimiento
from sedes.models import Sede, Espacio

class Command(BaseCommand):
    help = "Configura el grupo de permisos limitados (add y view en inventario y sedes, sin acceso a usuarios ni borrado)"

    def handle(self, *args, **options):
        group_name = "Investigadores y Asistentes de Laboratorio"
        group, created = Group.objects.get_or_create(name=group_name)
        if created:
            self.stdout.write(self.style.SUCCESS(f"Grupo creado: '{group_name}'"))
        else:
            self.stdout.write(f"Grupo existente encontrado: '{group_name}'")

        models_allowed = [Reactivo, Equipo, ImagenEquipo, Material, Marca, Movimiento, Sede, Espacio]
        
        group.permissions.clear()
        
        added_perms = []
        for model in models_allowed:
            ct = ContentType.objects.get_for_model(model)
            perms = Permission.objects.filter(
                content_type=ct
            ).filter(
                Q(codename__startswith="add_") | Q(codename__startswith="view_")
            )
            for perm in perms:
                group.permissions.add(perm)
                added_perms.append(f"{perm.content_type.model}.{perm.codename}")

        self.stdout.write(self.style.SUCCESS(
            f"Se asignaron {len(added_perms)} permisos al grupo '{group_name}':\n" + ", ".join(added_perms)
        ))

        # Configurar usuario de prueba
        test_username = "investigador"
        test_user, u_created = User.objects.get_or_create(
            username=test_username,
            defaults={
                "first_name": "Investigador",
                "last_name": "GIQYMA",
                "email": "investigador@unicartagena.edu.co",
                "is_staff": True,
                "is_superuser": False,
            }
        )
        test_user.set_password("investigador123")
        test_user.is_staff = True
        test_user.is_superuser = False
        test_user.save()
        test_user.groups.add(group)

        self.stdout.write(self.style.SUCCESS(
            f"Usuario '{test_username}' configurado y actualizado con los permisos del grupo."
        ))
