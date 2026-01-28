from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Sum, Count
from .models import Bet
from .serializers import BetSerializer
from events.models import Event
from payments.models import Transaction
from accounts.models import User

class BetPlaceView(generics.CreateAPIView):
    serializer_class = BetSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def perform_create(self, serializer):
        bet = serializer.save(user=self.request.user)
        
        Transaction.objects.create(
            user=self.request.user,
            transaction_type='bet',
            amount=bet.amount,
            status='completed',
            description=f"Ставка на событие {bet.event}",
            metadata={'bet_id': bet.id}
        )
        
        user = self.request.user
        user.balance -= bet.amount
        user.total_bets += 1
        user.total_wagered += bet.amount
        user.save()

class BetListView(generics.ListAPIView):
    serializer_class = BetSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'event', 'is_live']
    
    def get_queryset(self):
        return Bet.objects.filter(user=self.request.user).order_by('-placed_at')

class BetDetailView(generics.RetrieveAPIView):
    serializer_class = BetSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Bet.objects.filter(user=self.request.user)

class BetCancelView(generics.UpdateAPIView):
    serializer_class = BetSerializer
    permission_classes = (permissions.IsAuthenticated,)
    
    def get_queryset(self):
        return Bet.objects.filter(user=self.request.user, status='pending')
    
    def update(self, request, *args, **kwargs):
        bet = self.get_object()
        
        if bet.event.start_time <= timezone.now():
            return Response(
                {'error': 'Нельзя отменить ставку на начавшееся событие'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        Transaction.objects.create(
            user=request.user,
            transaction_type='refund',
            amount=bet.amount,
            status='completed',
            description=f"Возврат ставки на событие {bet.event}",
            metadata={'bet_id': bet.id}
        )
        
        user = request.user
        user.balance += bet.amount
        user.total_wagered -= bet.amount
        user.total_bets -= 1
        user.save()
        
        bet.status = 'cancelled'
        bet.save()
        
        serializer = self.get_serializer(bet)
        return Response(serializer.data)

class BetStatsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        
        stats = Bet.objects.filter(user=user).aggregate(
            total_bets=Count('id'),
            total_wagered=Sum('amount'),
            total_won=Sum('actual_win'),
            pending_bets=Count('id', filter=models.Q(status='pending')),
            won_bets=Count('id', filter=models.Q(status='won')),
            lost_bets=Count('id', filter=models.Q(status='lost'))
        )
        
        return Response(stats)