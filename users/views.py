# users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import Http404
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm
from django.db import IntegrityError, DatabaseError

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES or None)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f'Registre completat. Benvingut/da, {user.get_username()}!')
                return redirect('users:profile')
            except IntegrityError:
                messages.error(request, 'Aquest correu electrònic ja està registrat.')
            except DatabaseError:
                messages.error(request, 'Error amb la base de dades. Torna-ho a provar més tard.')
        else:
            messages.error(request, 'Si us plau, corregeix els errors del formulari.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or reverse('users:profile')
    if request.method == 'POST':
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Has iniciat sessió correctament.')
            return redirect(next_url)
        else:
            messages.error(request, 'Error d\'autenticació. Revisa les credencials.')
    else:
        form = CustomAuthenticationForm(request=request)
    return render(request, 'registration/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, 'Has tancat la sessió.')
    return redirect('home')  # suposa que 'home' és la pàgina principal del projecte


@login_required
def profile_view(request):
    user = request.user
    return render(request, 'users/profile.html', {'user_obj': user})


@login_required
def edit_profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualitzat correctament.')
            return redirect('users:profile')
        else:
            messages.error(request, 'Si us plau, corregeix els errors.')
    else:
        form = CustomUserUpdateForm(instance=user)
    return render(request, 'users/edit_profile.html', {'form': form})


def public_profile_view(request, username):
    user_obj = get_object_or_404(User, username=username)
    # Si vols, filtratge per visibilitat (ex: is_active) es pot afegir aquí
    return render(request, 'users/public_profile.html', {'user_obj': user_obj})
