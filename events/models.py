# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Sport(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    icon = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Вид спорта'
        verbose_name_plural = 'Виды спорта'

class League(models.Model):
    name = models.CharField(max_length=100)
    sport = models.ForeignKey(Sport, on_delete=models.CASCADE, related_name='leagues')
    country = models.CharField(max_length=100)
    logo_url = models.CharField(max_length=500, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.country})"
    
    class Meta:
        verbose_name = 'Лига/Турнир'
        verbose_name_plural = 'Лиги/Турниры'
        unique_together = ['name', 'sport', 'country']

class Event(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Запланировано'),
        ('live', 'В прямом эфире'),
        ('finished', 'Завершено'),
        ('cancelled', 'Отменено'),
        ('postponed', 'Перенесено'),
    ]
    
    name = models.CharField(max_length=200)
    league = models.ForeignKey(League, on_delete=models.CASCADE, related_name='events')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    team_a = models.CharField(max_length=100)
    team_b = models.CharField(max_length=100)
    team_a_logo_url = models.CharField(max_length=500, blank=True) 
    team_b_logo_url = models.CharField(max_length=500, blank=True) 
    result = models.JSONField(null=True, blank=True) 
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.team_a} vs {self.team_b} - {self.league}"
    
    class Meta:
        verbose_name = 'Спортивное событие'
        verbose_name_plural = 'Спортивные события'
        ordering = ['start_time']

class Odd(models.Model):
    ODD_TYPES = [
        ('win_a', 'Победа команды A'),
        ('draw', 'Ничья'),
        ('win_b', 'Победа команды B'),
        ('total_over', 'Тотал больше'),
        ('total_under', 'Тотал меньше'),
        ('handicap_a', 'Фора команды A'),
        ('handicap_b', 'Фора команды B'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='odds')
    odd_type = models.CharField(max_length=50, choices=ODD_TYPES)
    value = models.DecimalField(
        max_digits=5, 
        decimal_places=2,
        validators=[MinValueValidator(Decimal('1.01'))]
    )
    parameters = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.event} - {self.get_odd_type_display()}: {self.value}"
    
    class Meta:
        verbose_name = 'Коэффициент'
        verbose_name_plural = 'Коэффициенты'
        unique_together = ['event', 'odd_type', 'parameters']