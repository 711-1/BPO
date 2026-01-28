from django.shortcuts import render
from rest_framework import generics, filters, permissions
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from .models import Sport, League, Event, Odd
from .serializers import (
    SportSerializer, LeagueSerializer, 
    EventSerializer, OddSerializer
)

class SportListView(generics.ListAPIView):
    queryset = Sport.objects.filter(is_active=True)
    serializer_class = SportSerializer
    permission_classes = (permissions.AllowAny,)

class LeagueListView(generics.ListAPIView):
    queryset = League.objects.filter(is_active=True)
    serializer_class = LeagueSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sport', 'country']
    search_fields = ['name']

class EventListView(generics.ListAPIView):
    serializer_class = EventSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['league', 'status', 'league__sport']
    search_fields = ['team_a', 'team_b', 'league__name']
    ordering_fields = ['start_time', 'created_at']
    ordering = ['start_time']
    
    def get_queryset(self):
        queryset = Event.objects.filter(is_active=True)
        
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(start_time__gte=date_from)
        if date_to:
            queryset = queryset.filter(start_time__lte=date_to)
        
        return queryset

class EventDetailView(generics.RetrieveAPIView):
    queryset = Event.objects.filter(is_active=True)
    serializer_class = EventSerializer
    permission_classes = (permissions.AllowAny,)

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAdminUser,)

class EventUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAdminUser,)

class EventResultUpdateView(generics.UpdateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (permissions.IsAdminUser,)
    
    def update(self, request, *args, **kwargs):
        event = self.get_object()
        result = request.data.get('result')
        
        if result:
            event.result = result
            event.status = 'finished'
            event.save()
        return super().update(request, *args, **kwargs)

class OddListView(generics.ListAPIView):
    queryset = Odd.objects.filter(is_active=True)
    serializer_class = OddSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['event', 'odd_type']