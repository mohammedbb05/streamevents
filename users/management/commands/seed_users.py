import random
import unicodedata
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import transaction
from faker import Faker
from django.apps import apps

User = get_user_model()


class Command(BaseCommand):
    help = "Genera usuaris de prova per StreamEvents amb Faker i assigna rols/grups."

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=10,
            help='Nombre d\'usuaris a crear (default: 10)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina tots els usuaris existents (excepte superusers)'
        )
        parser.add_argument(
            '--with-follows',
            action='store_true',
            help='Crea relacions de seguiment aleatòries si el model Follow existeix'
        )

    def handle(self, *args, **options):
        faker = Faker('es_ES')
        num_users = options['users']
        clear = options['clear']
        with_follows = options['with_follows']

        self.stdout.write("🚀 Iniciant creació d'usuaris de prova...")

        # --- Crear grups si no existeixen ---
        groups = {
            "Organitzadors": Group.objects.get_or_create(name="Organitzadors")[0],
            "Participants": Group.objects.get_or_create(name="Participants")[0],
            "Moderadors": Group.objects.get_or_create(name="Moderadors")[0],
        }
        self.stdout.write(self.style.SUCCESS("✅ Grups creats o existents: Organitzadors, Participants, Moderadors"))

        # --- Eliminar usuaris existents si s'especifica --clear ---
        if clear:
            deleted_count = User.objects.filter(is_superuser=False).delete()[0]
            self.stdout.write(self.style.WARNING(f"🧹 Usuaris eliminats: {deleted_count}"))

        # --- Crear superusuari admin ---
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@streamevents.com',
                password='admin123',
                first_name='Admin',
                last_name='StreamEvents',
                display_name='🔧 Administrador',
                bio='Administrador del sistema StreamEvents.'
            )
            self.stdout.write(self.style.SUCCESS("🔧 Superusuari 'admin' creat amb èxit."))
        else:
            self.stdout.write(self.style.NOTICE("ℹ️ El superusuari 'admin' ja existeix."))

        # --- Crear usuaris de prova ---
        with transaction.atomic():
            for i in range(num_users):
                first = faker.first_name()
                last = faker.last_name()

                # Generar username sense accents
                base_username = f"{first.lower()}.{last.lower()}"
                username_clean = unicodedata.normalize('NFKD', base_username).encode('ascii', 'ignore').decode('utf-8')
                username = f"{username_clean}{i+1}"
                email = f"{username}@streamevents.com"

                # Determinar rol segons la posició
                if (i + 1) % 5 == 0:
                    role = "Organitzadors"
                    emoji = "🎯"
                    bio = faker.sentence(nb_words=8) + " Organitzador d'esdeveniments en streaming."
                elif (i + 1) % 3 == 0:
                    role = "Moderadors"
                    emoji = "🛡️"
                    bio = faker.sentence(nb_words=8) + " Moderador d'esdeveniments i xats."
                else:
                    role = "Participants"
                    emoji = ""
                    bio = faker.sentence(nb_words=8) + " Participant habitual."

                display_name = f"{emoji} {first} {last}".strip()

                # Crear usuari o obtenir-lo si ja existeix
                user, created = User.objects.get_or_create(
                    username=username,
                    defaults={
                        "email": email,
                        "first_name": first,
                        "last_name": last,
                        "display_name": display_name,
                        "bio": bio,
                        "avatar": None,
                        "is_active": True
                    }
                )

                if created:
                    user.set_password('password123')
                    user.save()
                    user.groups.add(groups[role])
                    self.stdout.write(self.style.SUCCESS(f"👤 {display_name} ({role}) creat."))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ Usuari existent: {username}"))

        self.stdout.write(self.style.SUCCESS(f"🎉 {num_users} usuaris de prova creats correctament!"))

        # --- Crear relacions de seguiment si s'indica ---
        if with_follows:
            self.create_follow_relations()

    def create_follow_relations(self):
        """Crea relacions aleatòries de seguiment si el model Follow existeix."""
        if not apps.is_installed('follows'):
            self.stdout.write(self.style.WARNING("⚠️ App 'follows' no instal·lada. No es poden crear relacions de seguiment."))
            return

        Follow = apps.get_model('follows', 'Follow')
        users = list(User.objects.filter(is_superuser=False))
        count = 0

        for user in users:
            following = random.sample(users, random.randint(0, min(3, len(users))))
            for f in following:
                if f != user:
                    Follow.objects.get_or_create(follower=user, followed=f)
                    count += 1

        self.stdout.write(self.style.SUCCESS(f"🔗 Relacions de seguiment creades: {count}"))