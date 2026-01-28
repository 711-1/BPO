from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from django.db.models import Count, Sum, Q
from events.models import Event
from bets.models import Bet
from accounts.models import User

class DashboardView(APIView):
    permission_classes = (permissions.IsAdminUser,)
    
    def get(self, request):
        events_stats = Event.objects.aggregate(
            total=Count('id'),
            scheduled=Count('id', filter=Q(status='scheduled')),
            live=Count('id', filter=Q(status='live')),
            finished=Count('id', filter=Q(status='finished'))
        )
        
        users_stats = User.objects.aggregate(
            total=Count('id'),
            regular=Count('id', filter=Q(user_type='regular')),
            vip=Count('id', filter=Q(user_type='vip')),
            admins=Count('id', filter=Q(user_type='admin'))
        )
        
        bets_stats = Bet.objects.aggregate(
            total=Count('id'),
            total_amount=Sum('amount'),
            total_won=Sum('actual_win', filter=Q(status='won')),
            pending=Count('id', filter=Q(status='pending'))
        )
        
        recent_users = User.objects.order_by('-date_joined')[:10].values('id', 'username', 'date_joined', 'user_type', 'balance')
        recent_bets = Bet.objects.select_related('user', 'event').order_by('-placed_at')[:10]
        
        return Response({
            'events': events_stats,
            'users': users_stats,
            'bets': bets_stats,
            'recent_users': list(recent_users),
            'recent_bets': [
                {
                    'id': bet.id,
                    'user': bet.user.username,
                    'event': str(bet.event),
                    'amount': float(bet.amount),
                    'status': bet.status,
                    'placed_at': bet.placed_at
                }
                for bet in recent_bets
            ]
        })