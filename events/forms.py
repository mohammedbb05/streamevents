from django import forms
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Event
from datetime import timedelta

class EventCreationForm(forms.ModelForm):
    scheduled_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        input_formats=['%Y-%m-%dT%H:%M'],
    )
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'scheduled_date', 
                 'thumbnail', 'max_viewers', 'tags', 'stream_url']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Títol de l\'esdeveniment'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Descriu el teu esdeveniment...'
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'max_viewers': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
                'max': 1000
            }),
            'tags': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'etiqueta1, etiqueta2, etiqueta3'
            }),
            'stream_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://www.youtube.com/watch?v=... o https://www.twitch.tv/...'
            }),
        }
        labels = {
            'title': 'Títol',
            'description': 'Descripció',
            'category': 'Categoria',
            'scheduled_date': 'Data i hora programada',
            'thumbnail': 'Imatge de portada',
            'max_viewers': 'Màxim espectadors',
            'tags': 'Etiquetes',
            'stream_url': 'URL del streaming',
        }
        help_texts = {
            'tags': 'Separa les etiquetes amb comes',
            'stream_url': 'Introdueix una URL de YouTube o Twitch',
            'max_viewers': 'Màxim espectadors (1-1000)',
        }

    def clean_scheduled_date(self):
        scheduled_date = self.cleaned_data.get('scheduled_date')
        if scheduled_date and scheduled_date < timezone.now():
            raise ValidationError('La data programada no pot ser en el passat')
        return scheduled_date

    def clean_max_viewers(self):
        max_viewers = self.cleaned_data.get('max_viewers')
        if max_viewers and (max_viewers < 1 or max_viewers > 1000):
            raise ValidationError('El màxim d\'espectadors ha d\'estar entre 1 i 1000')
        return max_viewers

    def clean_title(self):
        title = self.cleaned_data.get('title')
        # Si l'usuari està disponible (en el cas de creació, ho comprovarem a la vista)
        return title


class EventUpdateForm(forms.ModelForm):
    scheduled_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control',
        }),
        input_formats=['%Y-%m-%dT%H:%M'],
    )
    
    class Meta:
        model = Event
        fields = ['title', 'description', 'category', 'scheduled_date', 
                 'thumbnail', 'max_viewers', 'tags', 'status', 'stream_url']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'thumbnail': forms.FileInput(attrs={'class': 'form-control'}),
            'max_viewers': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 1000}),
            'tags': forms.TextInput(attrs={'class': 'form-control'}),
            'stream_url': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'status': 'Estat',
        }

    def __init__(self, *args, **kwargs):
        self.event = kwargs.pop('event', None)
        super().__init__(*args, **kwargs)
        
        # Si l'esdeveniment està en directe, no es pot canviar la data
        if self.event and self.event.status == 'live':
            self.fields['scheduled_date'].disabled = True
            self.fields['scheduled_date'].help_text = 'No es pot canviar la data quan l\'esdeveniment està en directe'

    def clean(self):
        cleaned_data = super().clean()
        
        if self.event:
            # No es pot canviar l'estat a programat si l'esdeveniment ja ha començat
            new_status = cleaned_data.get('status')
            new_date = cleaned_data.get('scheduled_date')
            
            if new_status == 'scheduled' and new_date and new_date < timezone.now():
                raise ValidationError('No es pot programar un esdeveniment en el passat')
                
        return cleaned_data


class EventSearchForm(forms.Form):
    CATEGORY_CHOICES = [
        ('', 'Totes les categories'),
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
        ('', 'Tots els estats'),
        ('scheduled', 'Programat'),
        ('live', 'En Directe'),
        ('finished', 'Finalitzat'),
        ('cancelled', 'Cancel·lat'),
    ]

    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Cercar esdeveniments...'
        })
    )
    
    category = forms.ChoiceField(
        required=False,
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    status = forms.ChoiceField(
        required=False,
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'type': 'date',
            'class': 'form-control'
        })
    )