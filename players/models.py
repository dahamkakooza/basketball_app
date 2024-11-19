from django.db import models

class Player(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    position = models.CharField(max_length=50, choices=[
        ('PG', 'Point Guard'),
        ('SG', 'Shooting Guard'),
        ('SF', 'Small Forward'),
        ('PF', 'Power Forward'),
        ('C', 'Center')
    ])
    height = models.FloatField(help_text="Height in cm")
    location = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    highlight_video = models.URLField(max_length=200, null=True, blank=True)
    achievements = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Opportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=100)
    application_deadline = models.DateField()
    link = models.URLField(max_length=200)

    def __str__(self):
        return self.title


