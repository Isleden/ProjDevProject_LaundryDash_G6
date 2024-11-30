# Generated by Django 5.1.3 on 2024-11-29 05:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_order_ordered_from_business_alter_order_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=200)),
                ('business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_business', to='users.business')),
            ],
        ),
    ]