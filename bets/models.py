# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from accounts.models import User
from events.models import Event, Odd
from django.conf import settings

class Bet(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('won', 'Выиграна'),
        ('lost', 'Проиграна'),
        ('cancelled', 'Отменена'),
        ('refunded', 'Возвращена'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bets')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bets')
    odd = models.ForeignKey(Odd, on_delete=models.CASCADE, related_name='bets')
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(settings.MIN_BET_AMOUNT)]
    )
    potential_win = models.DecimalField(max_digits=12, decimal_places=2)
    actual_win = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    is_live = models.BooleanField(default=False)
    placed_at = models.DateTimeField(auto_now_add=True)
    settled_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.event} - {self.amount}"
    
    def save(self, *args, **kwargs):
        if not self.pk: 
            self.potential_win = self.amount * self.odd.value
            max_bet = self.user.get_max_bet_amount()
            if self.amount > max_bet:
                raise ValueError(f"Максимальная сумма ставки: {max_bet}")
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Ставка'
        verbose_name_plural = 'Ставки'
        ordering = ['-placed_at']