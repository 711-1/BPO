from django.contrib import admin
from .models import Sport, League, Event, Odd

@admin.register(Sport)
class SportAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(League)
class LeagueAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'country', 'is_active')
    list_filter = ('sport', 'country', 'is_active')
    search_fields = ('name', 'country')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'league', 'team_a', 'team_b', 'start_time', 'status', 'is_active')
    list_filter = ('status', 'league', 'league__sport', 'is_active')
    search_fields = ('name', 'team_a', 'team_b', 'league__name')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'start_time'
    ordering = ('-start_time',)

@admin.register(Odd)
class OddAdmin(admin.ModelAdmin):
    list_display = ('event', 'odd_type', 'value', 'is_active', 'last_updated')
    list_filter = ('odd_type', 'is_active', 'event__status')
    search_fields = ('event__name', 'odd_type')
    readonly_fields = ('last_updated', 'created_at')
    list_editable = ('value', 'is_active')