# Generated by Django 5.1.3 on 2024-12-03 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_business_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(max_length=30, null=True),
        ),
    ]