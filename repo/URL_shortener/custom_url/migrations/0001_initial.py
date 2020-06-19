# Generated by Django 3.0.7 on 2020-06-19 05:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='URL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin_url', models.CharField(blank=True, max_length=1024, null=True)),
                ('shorten_url', models.CharField(blank=True, max_length=100, null=True)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('converted_value', models.CharField(max_length=32)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('owner', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='urls', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
