from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, Group, Permission

# Custom User Model
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Player', 'Player'),
        ('Scout', 'Scout'),
        ('Admin', 'Admin'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='Player')

    # Avoid conflicts with auth.User model
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_groups",  # Unique related name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions",  # Unique related name
        blank=True
    )

    def __str__(self):
        return f"{self.username} ({self.role})"


# Player Model
class Player(models.Model):
    POSITION_CHOICES = [
        ('PG', 'Point Guard'),
        ('SG', 'Shooting Guard'),
        ('SF', 'Small Forward'),
        ('PF', 'Power Forward'),
        ('C', 'Center'),
    ]

    SKILL_LEVEL_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Professional', 'Professional'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='player_profile')
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    height = models.FloatField(help_text="Height in cm")
    location = models.CharField(max_length=100)
    skill_level = models.CharField(max_length=50, choices=SKILL_LEVEL_CHOICES)
    scholarship_interest = models.BooleanField(default=True, help_text="Is the player interested in scholarships?")
    achievements = models.TextField(blank=True, help_text="Basketball achievements and awards")
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    contact_email = models.EmailField(null=True, blank=True)
    availability = models.BooleanField(default=True, help_text="Available for new opportunities?")
    created_at = models.DateTimeField(auto_now_add=True)
    preferred_opportunities = models.ManyToManyField('Opportunity', blank=True, related_name="interested_players")
    mentor_assigned = models.CharField(max_length=100, null=True, blank=True, help_text="Assigned mentor, if any")

    def __str__(self):
        return f"{self.name} ({self.position})"


# Opportunity Model
class Opportunity(models.Model):
    SCHOLARSHIP_CHOICES = [
        ('Full', 'Full Scholarship'),
        ('Partial', 'Partial Scholarship'),
    ]

    SKILL_REQUIREMENTS_CHOICES = [
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
        ('Professional', 'Professional'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(help_text="Detailed description of the opportunity")
    location = models.CharField(max_length=100)
    scholarship_type = models.CharField(max_length=50, choices=SCHOLARSHIP_CHOICES)
    skill_requirements = models.CharField(
        max_length=50,
        choices=SKILL_REQUIREMENTS_CHOICES,
        default='Beginner'
    )
    basketball_program = models.CharField(max_length=200, null=True, blank=True, help_text="Associated basketball program, if any")
    application_deadline = models.DateField()
    contact_email = models.EmailField(null=True, blank=True, help_text="Contact email for applications")
    link = models.URLField(max_length=200, help_text="Link to the application or more information")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.scholarship_type})"


# Application Model
class Application(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='applications')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.player.name} applied for {self.opportunity.title} ({self.status})"
