from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from .models import Event
from .forms import EventCreationForm, EventUpdateForm, EventSearchForm
from django.http import HttpResponseForbidden

def event_list_view(request):
    """Vista per llistar esdeveniments amb gestió d'errors"""
    try:
        # Obtenim tots els esdeveniments
        all_events = list(Event.objects.all())
        
        # Assegurar que tots els esdeveniments tenen created_at
        for event in all_events:
            if event.created_at is None:
                # Si no té created_at, li assignem l'hora actual
                event.created_at = timezone.now()
                # O podríem guardar-ho a la base de dades:
                # event.save()
        
        # Ordenem per data de creació amb gestió d'errors
        def get_created_at(event):
            # Retorna un valor per defecte si created_at és None
            return event.created_at or timezone.now()
        
        all_events.sort(key=get_created_at, reverse=True)
        
        # Esdeveniments destacats
        featured_events = []
        for event in all_events:
            if event.is_featured and event.status in ['scheduled', 'live']:
                featured_events.append(event)
                if len(featured_events) >= 6:  # Limit a 6
                    break
        
        # Paginació
        page_size = 12
        try:
            page = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page = 1
        
        # Assegurar que la pàgina és vàlida
        if page < 1:
            page = 1
        
        start_idx = (page - 1) * page_size
        end_idx = start_idx + page_size
        
        # Assegurar que els índexs estan dins dels límits
        if start_idx >= len(all_events):
            start_idx = 0
            page = 1
            end_idx = page_size
        
        page_events = all_events[start_idx:end_idx]
        
        # Calcular total de pàgines
        total_events = len(all_events)
        total_pages = max(1, (total_events + page_size - 1) // page_size)
        
        # Assegurar que la pàgina actual no és més gran que el total
        if page > total_pages:
            page = total_pages
            start_idx = (page - 1) * page_size
            end_idx = min(start_idx + page_size, total_events)
            page_events = all_events[start_idx:end_idx]
        
        context = {
            'events': page_events,
            'featured_events': featured_events,
            'search_form': EventSearchForm(),
            'current_page': page,
            'total_pages': total_pages,
            'total_events': total_events,
        }
        
        return render(request, 'events/includes/event_list.html', context)
        
    except Exception as e:
        # En cas d'error greu, mostrem una pàgina d'error simple
        print(f"Error a event_list_view: {e}")
        context = {
            'error': "Hi ha hagut un problema carregant els esdeveniments",
            'events': [],
            'featured_events': [],
            'search_form': EventSearchForm(),
            'current_page': 1,
            'total_pages': 1,
            'total_events': 0,
        }
        return render(request, 'events/includes/event_list.html', context)

# events/views.py
def event_detail_view(request, pk):
    try:
        event = get_object_or_404(Event, pk=pk)
        
        # Verificar si l'usuari creador encara existeix
        try:
            creator_exists = event.creator is not None
        except User.DoesNotExist:
            creator_exists = False
        
        is_creator = False
        if creator_exists and request.user.is_authenticated:
            is_creator = request.user == event.creator
        
        # Actualitzar estat si és necessari
        try:
            event.update_status()
        except:
            pass  # Si hi ha error, continuem
        
        context = {
            'event': event,
            'is_creator': is_creator,
            'creator_exists': creator_exists,
            'embed_url': event.get_stream_embed_url() if hasattr(event, 'get_stream_embed_url') else None,
            'tags_list': event.get_tags_list() if hasattr(event, 'get_tags_list') else [],
        }
        
        return render(request, 'events/event_detail.html', context)
        
    except Exception as e:
        print(f"Error in event_detail_view: {e}")
        messages.error(request, "No s'ha pogut carregar l'esdeveniment.")
        return redirect('events:event_list')
@login_required
def event_create_view(request):
    if request.method == 'POST':
        form = EventCreationForm(request.POST, request.FILES)
        
        if form.is_valid():
            event = form.save(commit=False)
            event.creator = request.user
            
            # Verificar títol únic per usuari
            if Event.objects.filter(creator=request.user, title=event.title).exists():
                messages.error(request, 'Ja tens un esdeveniment amb aquest títol')
            else:
                event.save()
                messages.success(request, 'Esdeveniment creat correctament!')
                return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventCreationForm()
    
    context = {
        'form': form,
        'title': 'Crear nou esdeveniment',
    }
    
    return render(request, 'events/event_form.html', context)

@login_required
def event_update_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Verificar que l'usuari és el creador
    if request.user != event.creator:
        return HttpResponseForbidden("No tens permís per editar aquest esdeveniment")
    
    if request.method == 'POST':
        form = EventUpdateForm(request.POST, request.FILES, instance=event, event=event)
        
        if form.is_valid():
            form.save()
            messages.success(request, 'Esdeveniment actualitzat correctament!')
            return redirect('events:event_detail', pk=event.pk)
    else:
        form = EventUpdateForm(instance=event, event=event)
    
    context = {
        'form': form,
        'event': event,
        'title': 'Editar esdeveniment',
    }
    
    return render(request, 'events/event_form.html', context)

@login_required
def event_delete_view(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    # Verificar que l'usuari és el creador
    if request.user != event.creator:
        return HttpResponseForbidden("No tens permís per eliminar aquest esdeveniment")
    
    if request.method == 'POST':
        event.delete()
        messages.success(request, 'Esdeveniment eliminat correctament!')
        return redirect('events:event_list')
    
    context = {
        'event': event,
    }
    
    return render(request, 'events/event_confirm_delete.html', context)

@login_required
def my_events_view(request):
    events = Event.objects.filter(creator=request.user).order_by('-created_at')
    
    # Estadístiques
    total_events = events.count()
    live_events = events.filter(status='live').count()
    scheduled_events = events.filter(status='scheduled').count()
    finished_events = events.filter(status='finished').count()
    
    # Filtre per estat
    status_filter = request.GET.get('status', '')
    if status_filter:
        events = events.filter(status=status_filter)
    
    context = {
        'events': events,
        'total_events': total_events,
        'live_events': live_events,
        'scheduled_events': scheduled_events,
        'finished_events': finished_events,
        'current_status_filter': status_filter,
        'status_choices': Event.STATUS_CHOICES,
    }
    
    return render(request, 'events/my_events.html', context)

def events_by_category_view(request, category):
    # Verificar que la categoria existeix
    valid_categories = [choice[0] for choice in Event.CATEGORY_CHOICES]
    
    if category not in valid_categories:
        messages.error(request, 'Categoria no vàlida')
        return redirect('events:event_list')
    
    events = Event.objects.filter(category=category).order_by('-scheduled_date')
    
    # Obtenir nom de la categoria
    category_name = dict(Event.CATEGORY_CHOICES)[category]
    
    context = {
        'events': events,
        'category': category,
        'category_name': category_name,
        'icon': Event().get_category_icon(),  # Instància buida per obtenir el mètode
    }
    
    return render(request, 'events/events_by_category.html', context)