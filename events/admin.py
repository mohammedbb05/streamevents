from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'category', 'status', 'scheduled_date', 'is_featured', 'created_at')
    list_filter = ('status', 'category', 'is_featured', 'scheduled_date')
    search_fields = ('title', 'description', 'tags', 'creator__username')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Informació bàsica', {
            'fields': ('title', 'description', 'creator', 'category')
        }),
        ('Programació', {
            'fields': ('scheduled_date', 'status', 'max_viewers')
        }),
        ('Multimèdia', {
            'fields': ('thumbnail', 'stream_url')
        }),
        ('Etiquetes i destacat', {
            'fields': ('tags', 'is_featured')
        }),
        ('Metadades', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    ordering = ('-created_at',)