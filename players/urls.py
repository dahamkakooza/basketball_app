from django.urls import path
from .views import PlayerListCreateView, OpportunityListCreateView, home

urlpatterns = [
    path('', home, name='home'),  # Home page rendering the HTML template
    path('players/', PlayerListCreateView.as_view(), name='player-list'),
    path('opportunities/', OpportunityListCreateView.as_view(), name='opportunity-list'),
]
