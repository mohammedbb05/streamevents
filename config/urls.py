# streamevents/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='home'),  # o la teva vista principal
    path('users/', include('users.urls', namespace='users')),
    path('events/', include('events.urls')),
<<<<<<< HEAD
    path('chat/', include('chat.urls')),
=======
>>>>>>> 478ab73ea527aa8a27fb9e10170ae876c46580e9
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
