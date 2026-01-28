# events/management/commands/seed_events.py
import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from events.models import Event
from django.utils import timezone
from datetime import timedelta
from faker import Faker

User = get_user_model()

class Command(BaseCommand):
    help = "Genera esdeveniments de prova per StreamEvents"

    def add_arguments(self, parser):
        parser.add_argument(
            '--events',
            type=int,
            default=15,
            help='Nombre d\'esdeveniments a crear (default: 15)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Elimina tots els esdeveniments existents'
        )
        parser.add_argument(
            '--with-users',
            action='store_true',
            help='Crea usuaris de prova si no n\'hi ha'
        )

    def handle(self, *args, **options):
        faker = Faker('es_ES')
        num_events = options['events']
        clear = options['clear']
        with_users = options['with_users']

        self.stdout.write("🎬 Iniciant creació d'esdeveniments de prova...")

        # --- Crear usuaris si cal ---
        if with_users:
            if not User.objects.exists():
                self.stdout.write("👤 No hi ha usuaris, creant alguns de prova...")
                for i in range(5):
                    User.objects.create_user(
                        username=f'user{i+1}',
                        email=f'user{i+1}@streamevents.com',
                        password='password123',
                        first_name=faker.first_name(),
                        last_name=faker.last_name(),
                        is_active=True
                    )
                self.stdout.write(self.style.SUCCESS("✅ 5 usuaris de prova creats"))
        
        # Obtenir usuaris existents
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("❌ No hi ha usuaris a la base de dades!"))
            self.stdout.write("Executa: python manage.py seed_users --users 5")
            return

        # --- Eliminar esdeveniments existents si s'especifica --clear ---
        if clear:
            deleted_count = Event.objects.all().delete()[0]
            self.stdout.write(self.style.WARNING(f"🧹 Esdeveniments eliminats: {deleted_count}"))

        # --- Categories i estatistics ---
        categories = [
            ('gaming', '🎮'),
            ('music', '🎵'), 
            ('talk', '💬'),
            ('education', '📚'),
            ('sports', '⚽'),
            ('entertainment', '🎭'),
            ('technology', '💻'),
            ('art', '🎨'),
            ('other', '📅'),
        ]
        
        status_choices = ['scheduled', 'live', 'finished', 'cancelled']
        # Pesos per a la probabilitat de cada estat
        status_weights = [50, 15, 30, 5]  # 50% scheduled, 15% live, 30% finished, 5% cancelled

        # --- Tags per categories ---
        tags_by_category = {
            'gaming': ['fortnite', 'valorant', 'league of legends', 'minecraft', 'gaming', 'torneig', 'esports'],
            'music': ['jazz', 'rock', 'electrònica', 'acústic', 'concert', 'música', 'en viu', 'dj'],
            'talk': ['debat', 'xerrada', 'conferència', 'discussió', 'educatiu', 'tecnologia'],
            'education': ['taller', 'tutorial', 'curs', 'aprenentatge', 'programació', 'python', 'web'],
            'sports': ['futbol', 'esports', 'competició', 'marató', 'fitness', 'entrenament'],
            'entertainment': ['comèdia', 'cuina', 'creatiu', 'divertiment', 'streaming'],
            'technology': ['ia', 'blockchain', 'programació', 'tecnologia', 'innovació', 'startup'],
            'art': ['fotografia', 'dibuix', 'pintura', 'creativitat', 'disseny', 'art digital'],
            'other': ['comunitat', 'xarrada', 'q&a', 'reunió', 'networking'],
        }

        # --- Stream URLs per categories ---
        stream_urls = {
            'gaming': [
                'https://www.twitch.tv/gamingstream',
                'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
                'https://www.twitch.tv/esportstv',
            ],
            'music': [
                'https://youtu.be/6LASz6HAL7E?si=WH4iBi4sjZSDyCkp',
                'https://youtu.be/9vDL7AgLdYQ?si=3uA1VJAs-VQ_zmCv',
                'https://youtu.be/Ov5ljc44Ajs?si=x10x7CMZQf9LPIG8',
            ],
            'talk': [
                'https://www.youtube.com/watch?v=video_id_talk1',
                'https://www.youtube.com/watch?v=video_id_talk2',
            ],
            'education': [
                'https://www.youtube.com/watch?v=video_id_edu1',
                'https://www.youtube.com/watch?v=video_id_edu2',
            ],
            'other': [
                'https://www.twitch.tv/community',
                'https://www.youtube.com/watch?v=video_id_other',
            ]
        }

        # --- Crear esdeveniments ---
        created_count = 0
        for i in range(num_events):
            # Seleccionar categoria aleatòria
            category_code, category_emoji = random.choice(categories)
            
            # Seleccionar estat amb probabilitats
            status = random.choices(status_choices, weights=status_weights, k=1)[0]
            
            # Crear data programada (dels darrers 30 dies als pròxims 60 dies)
            days_offset = random.randint(-30, 60)
            hours_offset = random.randint(0, 23)
            minutes_offset = random.randint(0, 59)
            
            scheduled_date = timezone.now() + timedelta(
                days=days_offset,
                hours=hours_offset,
                minutes=minutes_offset
            )
            
            # Ajustar estat segons la data
            if scheduled_date < timezone.now() and status == 'scheduled':
                status = random.choice(['finished', 'live'])
            elif scheduled_date > timezone.now() + timedelta(days=1) and status == 'live':
                status = 'scheduled'
            
            # Títol i descripció segons categoria
            if category_code == 'gaming':
                games = ['Fortnite', 'Valorant', 'League of Legends', 'Minecraft', 'Call of Duty']
                game = random.choice(games)
                title = f"{category_emoji} {random.choice(['Torneig', 'Marató', 'Streaming', 'Competició'])} de {game}"
                description = faker.paragraph(nb_sentences=3) + f" {game} amb jugadors de diferents nivells."
                
            elif category_code == 'music':
                genres = ['Jazz', 'Rock', 'Electrònica', 'Acústic', 'Hip Hop']
                genre = random.choice(genres)
                title = f"{category_emoji} {random.choice(['Concert', 'Jam Session', 'Live Set', 'Sessió'])} de {genre}"
                description = faker.paragraph(nb_sentences=3) + f" Gènere {genre.lower()} amb artistes {random.choice(['locals', 'internacionals', 'emergents'])}."
                
            elif category_code == 'talk':
                topics = ['Intel·ligència Artificial', 'Canvi Climàtic', 'Salut Mental', 'Blockchain', 'Emprenedoria']
                topic = random.choice(topics)
                title = f"{category_emoji} {random.choice(['Xerrada', 'Debat', 'Conferència', 'Ponent'])}: {topic}"
                description = faker.paragraph(nb_sentences=3) + f" Sobre {topic.lower()} amb experts del sector."
                
            elif category_code == 'education':
                subjects = ['Python', 'Desenvolupament Web', 'Fotografia', 'Dibuix Digital', 'Cuina']
                subject = random.choice(subjects)
                title = f"{category_emoji} {random.choice(['Taller', 'Curs', 'Tutorial', 'Masterclass'])}: {subject}"
                description = faker.paragraph(nb_sentences=3) + f" Aprengues {subject.lower()} des de zero amb professionals."
                
            else:
                title = f"{category_emoji} {faker.sentence(nb_words=4)}"
                description = faker.paragraph(nb_sentences=3)
            
            # Tags aleatoris
            tags_list = random.sample(tags_by_category.get(category_code, ['esdeveniment', 'streaming']), 
                                     min(3, len(tags_by_category.get(category_code, ['esdeveniment']))))
            tags = ', '.join(tags_list)
            
            # Stream URL segons categoria
            stream_url = random.choice(stream_urls.get(category_code, stream_urls['other']))
            
            # Seleccionar creador aleatori
            creator = random.choice(users)
            
            # Determinar si és destacat (20% de probabilitat)
            is_featured = random.random() < 0.2
            
            # Màxim d'espectadors
            max_viewers = random.choice([50, 100, 150, 200, 300, 500])
            
            # Crear l'esdeveniment
            try:
                event = Event.objects.create(
                    title=title,
                    description=description,
                    creator=creator,
                    category=category_code,
                    scheduled_date=scheduled_date,
                    status=status,
                    max_viewers=max_viewers,
                    is_featured=is_featured,
                    tags=tags,
                    stream_url=stream_url,
                )
                
                created_count += 1
                featured_str = " ⭐" if is_featured else ""
                self.stdout.write(f"{category_emoji} '{title}'{featured_str} creat per {creator.username}")
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error creant esdeveniment: {e}"))

        self.stdout.write(self.style.SUCCESS(f"🎉 {created_count} esdeveniments creats correctament!"))
        self.stdout.write("\n📊 Resum:")
        self.stdout.write(f"   • Total esdeveniments: {Event.objects.count()}")
        
        # Safer way to count featured and live events without complex WHERE clauses
        all_events = list(Event.objects.all())  # Get all events as a list
        featured_count = sum(1 for event in all_events if event.is_featured)
        live_count = sum(1 for event in all_events if event.status == 'live')
        scheduled_count = sum(1 for event in all_events if event.status == 'scheduled')
        
        self.stdout.write(f"   • Esdeveniments destacats: {featured_count}")
        self.stdout.write(f"   • En directe ara: {live_count}")
        self.stdout.write(f"   • Programats: {scheduled_count}")
        
        # Mostrar consells
        self.stdout.write("\n💡 Consells:")
        self.stdout.write("   • Per crear més esdeveniments: python manage.py seed_events --events 20")
        self.stdout.write("   • Per reiniciar: python manage.py seed_events --clear --events 15")