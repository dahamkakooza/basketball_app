from django.contrib import admin
from .models import Player, Opportunity, Application, CustomUser

# Register models in admin
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'location', 'skill_level', 'availability')
    search_fields = ('name', 'location', 'position', 'skill_level')

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'scholarship_type', 'application_deadline')
    search_fields = ('title', 'location', 'scholarship_type')

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('player', 'opportunity', 'status', 'applied_at')
    search_fields = ('player__name', 'opportunity__title')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'email')
    search_fields = ('username', 'role', 'email')

