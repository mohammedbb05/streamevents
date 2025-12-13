from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
import re

class Event(models.Model):
    CATEGORY_CHOICES = [
        ('gaming', 'Gaming'),
        ('music', 'Música'),
        ('talk', 'Xerrades'),
        ('education', 'Educació'),
        ('sports', 'Esports'),
        ('entertainment', 'Entreteniment'),
        ('technology', 'Tecnologia'),
        ('art', 'Art i Creativitat'),
        ('other', 'Altres'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Programat'),
        ('live', 'En Directe'),
        ('finished', 'Finalitzat'),
        ('cancelled', 'Cancel·lat'),
    ]

    title = models.CharField(max_length=200, verbose_name="Títol")
    description = models.TextField(verbose_name="Descripció")
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='events',
        verbose_name="Creador"
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        verbose_name="Categoria"
    )
    scheduled_date = models.DateTimeField(verbose_name="Data i hora programada")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled',
        verbose_name="Estat"
    )
    thumbnail = models.ImageField(
        upload_to='events/thumbnails/',
        blank=True,
        null=True,
        verbose_name="Imatge de portada"
    )
    max_viewers = models.PositiveIntegerField(
        default=100,
        verbose_name="Màxim espectadors"
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Destacat"
    )
    tags = models.CharField(
        max_length=500,
        blank=True,
        verbose_name="Etiquetes"
    )
    stream_url = models.URLField(
        max_length=500,
        blank=True,
        verbose_name="URL del streaming"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Esdeveniment'
        verbose_name_plural = 'Esdeveniments'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['category']),
            models.Index(fields=['scheduled_date']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('events:event_detail', kwargs={'pk': self.pk})

    @property
    def is_live(self):
        return self.status == 'live'

    @property
    def is_upcoming(self):
        return self.status == 'scheduled' and self.scheduled_date > timezone.now()

    def get_duration(self):
        """Calcula la durada de l'esdeveniment en minuts"""
        category_durations = {
            'gaming': 180,        # 3 hores
            'music': 90,          # 1.5 hores  
            'talk': 60,           # 1 hora
            'education': 120,     # 2 hores
            'sports': 150,        # 2.5 hores
            'entertainment': 120, # 2 hores
            'technology': 90,     # 1.5 hores
            'art': 120,           # 2 hores
            'other': 90,          # 1.5 hores
        }
        return category_durations.get(self.category, 90)

    def get_duration_display(self):
        minutes = self.get_duration()
        hours = minutes // 60
        mins = minutes % 60
        
        if hours == 0:
            return f"{mins} min"
        elif mins == 0:
            return f"{hours} h" if hours == 1 else f"{hours} hores"
        else:
            return f"{hours}h {mins}min"

    def get_tags_list(self):
        """Retorna les etiquetes com a llista"""
        if self.tags:
            return [tag.strip() for tag in self.tags.split(',')]
        return []

    def get_stream_embed_url(self):
        """Converteix URLs de YouTube/Twitch a format embed"""
        if not self.stream_url:
            return None
            
        # YouTube
        youtube_pattern = r'(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/watch\?v=|youtu\.be\/)([a-zA-Z0-9_-]+)'
        youtube_match = re.search(youtube_pattern, self.stream_url)
        if youtube_match:
            video_id = youtube_match.group(1)
            return f"https://www.youtube.com/embed/{video_id}"
        
        # Twitch
        twitch_pattern = r'(?:https?:\/\/)?(?:www\.)?twitch\.tv\/([a-zA-Z0-9_]+)'
        twitch_match = re.search(twitch_pattern, self.stream_url)
        if twitch_match:
            channel = twitch_match.group(1)
            return f"https://player.twitch.tv/?channel={channel}&parent={settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'localhost'}"
        
        return self.stream_url

    def update_status(self):
        """Actualitza l'estat automàticament segons la data programada"""
        now = timezone.now()
        
        if self.status == 'cancelled' or self.status == 'finished':
            return False
            
        if self.status == 'scheduled' and now >= self.scheduled_date:
            self.status = 'live'
            self.save()
            return True
            
        if self.status == 'live' and now >= self.scheduled_date + timedelta(minutes=self.get_duration()):
            self.status = 'finished'
            self.save()
            return True
            
        return False

    def get_status_badge_class(self):
        """Retorna la classe Bootstrap per al badge d'estat"""
        status_classes = {
            'scheduled': 'bg-primary',
            'live': 'bg-danger',
            'finished': 'bg-secondary',
            'cancelled': 'bg-dark',
        }
        return status_classes.get(self.status, 'bg-secondary')

    def get_category_icon(self):
        """Retorna una icona per a la categoria"""
        icons = {
            'gaming': '🎮',
            'music': '🎵',
            'talk': '💬',
            'education': '📚',
            'sports': '⚽',
            'entertainment': '🎭',
            'technology': '💻',
            'art': '🎨',
            'other': '📅',
        }
        return icons.get(self.category, '📅')