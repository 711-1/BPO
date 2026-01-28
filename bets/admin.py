from django.contrib import admin
from .models import Bet

@admin.register(Bet)
class BetAdmin(admin.ModelAdmin):
    list_display = ('user', 'event', 'amount', 'status', 'placed_at', 'settled_at')
    list_filter = ('status', 'is_live', 'placed_at', 'user__user_type')
    search_fields = ('user__username', 'event__name', 'notes')
    readonly_fields = ('placed_at', 'potential_win', 'actual_win')
    date_hierarchy = 'placed_at'
    ordering = ('-placed_at',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'event', 'odd', 'amount')
        }),
        ('Results', {
            'fields': ('potential_win', 'actual_win', 'status', 'settled_at')
        }),
        ('Additional', {
            'fields': ('is_live', 'notes'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('placed_at',),
            'classes': ('collapse',)
        }),
    )