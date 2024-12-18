# Generated by Django 5.1.3 on 2024-11-29 05:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_service'),
    ]

    operations = [
        migrations.CreateModel(
            name='LoadTendency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('light_tendency_price', models.IntegerField(default=0)),
                ('light_tendency_minimum', models.IntegerField(default=0)),
                ('light_tendency_maximum', models.IntegerField(default=0)),
                ('medium_tendency_price', models.IntegerField(default=0)),
                ('medium_tendency_minimum', models.IntegerField(default=0)),
                ('medium_tendency_maximum', models.IntegerField(default=0)),
                ('heavy_tendency_price', models.IntegerField(default=0)),
                ('heavy_tendency_minimum', models.IntegerField(default=0)),
                ('heavy_tendency_maximum', models.IntegerField(default=0)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='business_load_tendency', to='users.service')),
            ],
        ),
    ]
