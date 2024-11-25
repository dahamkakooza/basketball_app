from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.db.models import Q, Count
from .models import Player, Opportunity, Application
from .forms import PlayerForm, OpportunityForm
from .serializers import PlayerSerializer, OpportunitySerializer
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework import viewsets, permissions

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()

class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return super().get_permissions()



# Register New Users
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Failed to create account. Please try again.")
    else:
        form = UserCreationForm()
    return render(request, 'players/register.html', {'form': form})


# Home Page
def home(request):
    return render(request, 'players/home.html')


# Add Player
@login_required
def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Player added successfully!")
            return redirect('players_list')
        else:
            messages.error(request, "Failed to add player. Please check the form for errors.")
    else:
        form = PlayerForm()
    return render(request, 'players/add_player.html', {'form': form})


# Add Opportunity
@login_required
def add_opportunity(request):
    if request.method == 'POST':
        form = OpportunityForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Opportunity added successfully!")
            return redirect('opportunities_list')
        else:
            messages.error(request, "Failed to add opportunity. Please check the form for errors.")
    else:
        form = OpportunityForm()
    return render(request, 'players/add_opportunity.html', {'form': form})


# Player List with Pagination
def players_list(request):
    query = request.GET.get('q', '')
    players = Player.objects.filter(
        Q(name__icontains=query) |
        Q(location__icontains=query) |
        Q(position__icontains=query)
    ).order_by('name')

    paginator = Paginator(players, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'players/players_list.html', {'page_obj': page_obj})


# Opportunity List with Pagination
@login_required
def opportunities_list(request):
    query = request.GET.get('q', '')
    opportunities = Opportunity.objects.filter(
        Q(title__icontains=query) |
        Q(location__icontains=query)
    ).order_by('-created_at')

    paginator = Paginator(opportunities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'players/opportunities_list.html', {'page_obj': page_obj})


# Match Opportunities Based on Filters
def match_opportunities(request):
    location = request.GET.get('location', '')
    skill_level = request.GET.get('skill_level', '')
    opportunities = Opportunity.objects.filter(
        Q(location__icontains=location) &
        Q(skill_requirements__icontains=skill_level)
    )
    if not opportunities.exists():
        messages.info(request, "No matching opportunities found.")
    return render(request, 'players/match_opportunities.html', {'opportunities': opportunities})


# Apply for an Opportunity
@login_required
def apply_for_opportunity(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    application, created = Application.objects.get_or_create(
        player=request.user.player,
        opportunity=opportunity
    )
    if created:
        messages.success(request, f"You have successfully applied for {opportunity.title}!")
    else:
        messages.warning(request, f"You have already applied for {opportunity.title}.")
    return redirect('opportunities_list')


# View Player Applications (Admin Only)
@login_required
def player_applications(request):
    applications = Application.objects.select_related('player', 'opportunity').all()
    return render(request, 'players/player_applications.html', {'applications': applications})


# Dashboard (Admin Only)
@login_required
def admin_dashboard(request):
    players_count = Player.objects.count()
    opportunities_count = Opportunity.objects.count()
    applications_status = Application.objects.values('status').annotate(count=Count('status'))

    return render(request, 'players/admin_dashboard.html', {
        'players_count': players_count,
        'opportunities_count': opportunities_count,
        'applications_status': applications_status,
    })


# API View for Player List and Creation
class PlayerListCreateView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        players = Player.objects.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(position__icontains=query)
        )
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API View for Opportunity List and Creation
class OpportunityListCreateView(APIView):
    def get(self, request):
        query = request.GET.get('q', '')
        opportunities = Opportunity.objects.filter(
            Q(title__icontains=query) |
            Q(location__icontains=query)
        )
        serializer = OpportunitySerializer(opportunities, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OpportunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
