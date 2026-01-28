from django.contrib import admin
from .models import Transaction

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'transaction_type', 'amount', 'status', 'created_at', 'reference')
    list_filter = ('transaction_type', 'status', 'created_at', 'payment_method')
    search_fields = ('user__username', 'reference', 'description')
    readonly_fields = ('created_at', 'updated_at', 'reference')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('user', 'transaction_type', 'amount', 'status')
        }),
        ('Payment Details', {
            'fields': ('payment_method', 'reference', 'description'),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('metadata',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )