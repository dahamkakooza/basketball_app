# Generated by Django 5.1.3 on 2024-11-18 23:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Opportunity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('application_deadline', models.DateField()),
                ('link', models.URLField()),
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
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('highlight_video', models.URLField(blank=True, null=True)),
                ('achievements', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
