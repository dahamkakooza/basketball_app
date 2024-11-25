from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from rest_framework.routers import DefaultRouter
from . import views
from .views import PlayerViewSet, OpportunityViewSet

# Create a router and register ViewSets
router = DefaultRouter()
router.register('players', PlayerViewSet, basename='players')
router.register('opportunities', OpportunityViewSet, basename='opportunities')

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),

    # Player-related URLs
    path('add_player/', views.add_player, name='add_player'),
    path('players/', views.players_list, name='players_list'),

    # Opportunity-related URLs
    path('add_opportunity/', views.add_opportunity, name='add_opportunity'),
    path('opportunities/', views.opportunities_list, name='opportunities_list'),

    # Match Opportunities
    path('match_opportunities/', views.match_opportunities, name='match_opportunities'),

    # Application-related URLs
    path('apply/<int:opportunity_id>/', views.apply_for_opportunity, name='apply_for_opportunity'),

    # User Authentication
    path('login/', LoginView.as_view(template_name='players/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),

    # Include API endpoints
    path('api/', include(router.urls)),
]
