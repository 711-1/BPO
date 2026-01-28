from django.urls import path
from . import views

urlpatterns = [
    path('place/', views.BetPlaceView.as_view(), name='bet-place'),
    path('', views.BetListView.as_view(), name='bet-list'),
    path('<int:pk>/', views.BetDetailView.as_view(), name='bet-detail'),
    path('<int:pk>/cancel/', views.BetCancelView.as_view(), name='bet-cancel'),
    path('stats/', views.BetStatsView.as_view(), name='bet-stats'),
]