# Generated by Django 5.1.3 on 2024-11-29 06:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_loadtendency'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='heavy_tendency_maximum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='heavy_tendency_minimum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='heavy_tendency_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='light_tendency_maximum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='light_tendency_minimum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='light_tendency_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='medium_tendency_maximum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='medium_tendency_minimum',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='service',
            name='medium_tendency_price',
            field=models.IntegerField(default=0),
        ),
        migrations.DeleteModel(
            name='LoadTendency',
        ),
    ]