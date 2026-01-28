from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from .models import Transaction
from .serializers import (
    TransactionSerializer, 
    DepositSerializer, 
    WithdrawalSerializer
)
from accounts.models import User

class TransactionListView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['transaction_type', 'status']
    
    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')

class BalanceView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request):
        user = request.user
        return Response({
            'balance': user.balance,
            'currency': 'USD'
        })

class DepositView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            payment_method = serializer.validated_data['payment_method']
            
            
            transaction = Transaction.objects.create(
                user=request.user,
                transaction_type='deposit',
                amount=amount,
                status='completed',
                payment_method=payment_method,
                description=f"Пополнение через {payment_method}"
            )
            
            user = request.user
            user.balance += amount
            user.save()
            
            return Response({
                'transaction_id': transaction.reference,
                'new_balance': user.balance
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WithdrawalView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request):
        serializer = WithdrawalSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            bank_account = serializer.validated_data['bank_account']
            
            if request.user.balance < amount:
                return Response(
                    {'error': 'Недостаточно средств на балансе'},
                    status=status.HTTP_400_BAD_REQUEST
            )
            
            transaction = Transaction.objects.create(
                user=request.user,
                transaction_type='withdrawal',
                amount=amount,
                status='pending', 
                description=f"Вывод на счет {bank_account}",
                metadata={'bank_account': bank_account}
            )
            
            user = request.user
            user.balance -= amount
            user.save()
            
            return Response({
                'transaction_id': transaction.reference,
                'new_balance': user.balance,
                'message': 'Запрос на вывод отправлен на обработку'
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)