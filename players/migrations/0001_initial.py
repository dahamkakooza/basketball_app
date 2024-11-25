# Generated by Django 5.1.3 on 2024-11-25 07:42

import django.contrib.auth.models
import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(help_text='Detailed description of the opportunity')),
                ('location', models.CharField(max_length=100)),
                ('scholarship_type', models.CharField(choices=[('Full', 'Full Scholarship'), ('Partial', 'Partial Scholarship')], max_length=50)),
                ('skill_requirements', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Professional', 'Professional')], default='Beginner', max_length=50)),
                ('basketball_program', models.CharField(blank=True, help_text='Associated basketball program, if any', max_length=200, null=True)),
                ('application_deadline', models.DateField()),
                ('contact_email', models.EmailField(blank=True, help_text='Contact email for applications', max_length=254, null=True)),
                ('link', models.URLField(help_text='Link to the application or more information')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('role', models.CharField(choices=[('Player', 'Player'), ('Scout', 'Scout'), ('Admin', 'Admin')], default='Player', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, related_name='customuser_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='customuser_permissions', to='auth.permission')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('age', models.IntegerField()),
                ('position', models.CharField(choices=[('PG', 'Point Guard'), ('SG', 'Shooting Guard'), ('SF', 'Small Forward'), ('PF', 'Power Forward'), ('C', 'Center')], max_length=50)),
                ('height', models.FloatField(help_text='Height in cm')),
                ('location', models.CharField(max_length=100)),
                ('skill_level', models.CharField(choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Professional', 'Professional')], max_length=50)),
                ('scholarship_interest', models.BooleanField(default=True, help_text='Is the player interested in scholarships?')),
                ('achievements', models.TextField(blank=True, help_text='Basketball achievements and awards')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('contact_email', models.EmailField(blank=True, max_length=254, null=True)),
                ('availability', models.BooleanField(default=True, help_text='Available for new opportunities?')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('mentor_assigned', models.CharField(blank=True, help_text='Assigned mentor, if any', max_length=100, null=True)),
                ('preferred_opportunities', models.ManyToManyField(blank=True, related_name='interested_players', to='players.opportunity')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='player_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Rejected', 'Rejected')], default='Pending', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('opportunity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='players.opportunity')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='players.player')),
            ],
        ),
    ]
