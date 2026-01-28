from django.urls import path
from . import views

urlpatterns = [
    path('sports/', views.SportListView.as_view(), name='sport-list'),
    path('leagues/', views.LeagueListView.as_view(), name='league-list'),
    path('', views.EventListView.as_view(), name='event-list'),
    path('<int:pk>/', views.EventDetailView.as_view(), name='event-detail'),
    path('create/', views.EventCreateView.as_view(), name='event-create'),
    path('<int:pk>/update/', views.EventUpdateView.as_view(), name='event-update'),
    path('<int:pk>/update-result/', views.EventResultUpdateView.as_view(), name='event-update-result'),
    path('odds/', views.OddListView.as_view(), name='odd-list'),
]