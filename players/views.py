from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Player, Opportunity, Application
from .forms import PlayerForm, OpportunityForm, CustomUserCreationForm
from .serializers import PlayerSerializer, OpportunitySerializer

class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer

class OpportunityViewSet(viewsets.ModelViewSet):
    queryset = Opportunity.objects.all()
    serializer_class = OpportunitySerializer

# Role-Based Access Decorators
def role_required(role):
    """Decorator to restrict access based on user role."""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role == role:
                return view_func(request, *args, **kwargs)
            return render(request, '403.html', status=403)
        return wrapper
    return decorator


# Home Page
def home(request):
    return render(request, 'players/home.html')


# Register New Users
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
        else:
            messages.error(request, "Failed to create account. Please try again.")
    else:
        form = CustomUserCreationForm()
    return render(request, 'players/register.html', {'form': form})


# Add Player
@login_required
@role_required('Player')
def add_player(request):
    if request.method == 'POST':
        form = PlayerForm(request.POST, request.FILES)
        if form.is_valid():
            player = form.save(commit=False)
            player.user = request.user
            player.save()
            messages.success(request, "Player added successfully!")
            return redirect('players_list')
        else:
            messages.error(request, "Failed to add player. Please check the form for errors.")
    else:
        form = PlayerForm()
    return render(request, 'players/add_player.html', {'form': form})


# Add Opportunity
@login_required
@role_required('Admin')
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
@login_required
@role_required('Player')
def match_opportunities(request):
    location = request.GET.get('location', '')
    skill_level = request.GET.get('skill_level', '')
    opportunities = Opportunity.objects.filter(
        Q(location__icontains=location) & Q(skill_requirements__icontains=skill_level)
    )
    if not opportunities.exists():
        messages.info(request, "No matching opportunities found.")
    return render(request, 'players/match_opportunities.html', {'opportunities': opportunities})


# Apply for an Opportunity
@login_required
@role_required('Player')
def apply_for_opportunity(request, opportunity_id):
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    application, created = Application.objects.get_or_create(
        player=request.user.player_profile,
        opportunity=opportunity
    )
    if created:
        messages.success(request, f"You have successfully applied for {opportunity.title}!")
    else:
        messages.warning(request, f"You have already applied for {opportunity.title}.")
    return redirect('opportunities_list')


# API View for Player List and Creation
class PlayerListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get(self, request):
        query = request.GET.get('q', '')
        players = Player.objects.filter(
            Q(name__icontains=query) |
            Q(location__icontains=query) |
            Q(position__icontains=query)
        )
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(players, request)
        serializer = PlayerSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = PlayerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# API View for Opportunity List and Creation
class OpportunityListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination

    def get(self, request):
        query = request.GET.get('q', '')
        opportunities = Opportunity.objects.filter(
            Q(title__icontains=query) | Q(location__icontains=query)
        )
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(opportunities, request)
        serializer = OpportunitySerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = OpportunitySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Custom 404 and 403 Error Pages
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)


def custom_403_view(request, exception=None):
    return render(request, '403.html', status=403)
