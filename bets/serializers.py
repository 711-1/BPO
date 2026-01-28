from rest_framework import serializers
from django.utils import timezone
from .models import Bet
from events.serializers import EventSerializer, OddSerializer

class BetSerializer(serializers.ModelSerializer):
    event_details = EventSerializer(source='event', read_only=True)
    odd_details = OddSerializer(source='odd', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Bet
        fields = '__all__'
        read_only_fields = ['user', 'potential_win', 'actual_win', 'status', 'settled_at']
    
    def validate(self, data):
        if data['event'].start_time <= timezone.now():
            raise serializers.ValidationError("Нельзя делать ставку на начавшееся событие")
        
        if data['event'].status != 'scheduled':
            raise serializers.ValidationError("Ставки принимаются только на запланированные события")
        
        if not data['odd'].is_active:
            raise serializers.ValidationError("Этот коэффициент неактивен")
        
        user = self.context['request'].user
        if user.balance < data['amount']:
            raise serializers.ValidationError("Недостаточно средств на балансе")
        
        return data