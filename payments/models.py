# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from accounts.models import User

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Пополнение'),
        ('withdrawal', 'Вывод'),
        ('bet', 'Ставка'),
        ('win', 'Выигрыш'),
        ('refund', 'Возврат'),
        ('bonus', 'Бонус'),
        ('penalty', 'Штраф'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'В обработке'),
        ('completed', 'Завершено'),
        ('failed', 'Ошибка'),
        ('cancelled', 'Отменено'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=12, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reference = models.CharField(max_length=100, unique=True, blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_transaction_type_display()} - {self.amount}"
    
    def generate_reference(self):
        import uuid
        if not self.reference:
            self.reference = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    
    def save(self, *args, **kwargs):
        if not self.reference:
            self.generate_reference()
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = 'Транзакция'
        verbose_name_plural = 'Транзакции'
        ordering = ['-created_at']
