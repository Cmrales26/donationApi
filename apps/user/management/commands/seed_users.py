from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from faker import Faker

fake = Faker()
User = get_user_model()


class Command(BaseCommand):
    help = "🌱 Seed de roles y usuarios iniciales"

    def handle(self, *args, **kwargs):
        # Crear grupos
        admin_group, _ = Group.objects.get_or_create(name="Administrador")
        beneficiary_group, _ = Group.objects.get_or_create(name="Beneficiario")

        # (Opcional) asignar todos los permisos al grupo Administrador
        all_permissions = Permission.objects.all()
        admin_group.permissions.set(all_permissions)

        self.stdout.write(
            self.style.SUCCESS("✅ Grupos creados o existentes actualizados.")
        )

        # Crear usuario administrador
        if not User.objects.filter(username="admin").exists():
            admin_user = User.objects.create_user(
                username="admin",
                email="admin@demo.com",
                password="admin123",
                first_name="Admin",
                last_name="Demo",
                is_staff=True,
                is_superuser=True,
            )
            admin_user.groups.add(admin_group)
            self.stdout.write(
                self.style.SUCCESS("✅ Usuario administrador creado: admin/admin123")
            )
        else:
            self.stdout.write("ℹ️ Usuario administrador ya existe (admin)")

        # Crear usuarios beneficiarios
        for _ in range(20):
            username = fake.user_name()
            email = fake.email()
            phone = fake.phone_number()

            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    phone=phone,
                    password="12345678",
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                )
                user.groups.add(beneficiary_group)

        self.stdout.write(
            self.style.SUCCESS("✅ 20 usuarios Beneficiario creados con éxito.")
        )
