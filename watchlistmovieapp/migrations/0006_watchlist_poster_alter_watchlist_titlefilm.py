# Generated by Django 4.0.4 on 2022-05-19 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlistmovieapp', '0005_watchlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='poster',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='titleFilm',
            field=models.CharField(default='', max_length=50),
        ),
    ]
