# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from decimal import Decimal

class User(AbstractUser):
    USER_TYPES = [
        ('regular', 'Обычный пользователь'),
        ('vip', 'VIP пользователь'),
        ('admin', 'Администратор'),
    ]
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='regular')
    balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    total_bets = models.PositiveIntegerField(default=0)
    total_wins = models.PositiveIntegerField(default=0)
    total_losses = models.PositiveIntegerField(default=0)
    total_wagered = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_won = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    def get_max_bet_amount(self):
        from django.conf import settings
        if self.user_type == 'vip':
            return settings.MAX_BET_AMOUNT_VIP
        return settings.MAX_BET_AMOUNT_REGULAR
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'