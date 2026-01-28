from rest_framework import serializers
from .models import Sport, League, Event, Odd

class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = '__all__'

class LeagueSerializer(serializers.ModelSerializer):
    sport_name = serializers.CharField(source='sport.name', read_only=True)
    
    class Meta:
        model = League
        fields = '__all__'

class OddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Odd
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    league_name = serializers.CharField(source='league.name', read_only=True)
    sport_name = serializers.CharField(source='league.sport.name', read_only=True)
    odds = OddSerializer(many=True, read_only=True)
    
    class Meta:
        model = Event
        fields = '__all__'