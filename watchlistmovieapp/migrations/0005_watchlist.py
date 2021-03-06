# Generated by Django 4.0.4 on 2022-05-19 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlistmovieapp', '0004_alter_credentialsessiontmdb_api_key'),
    ]

    operations = [
        migrations.CreateModel(
            name='watchList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idFilm', models.IntegerField(null=True)),
                ('popularity', models.CharField(default='', max_length=50)),
                ('titleFilm', models.CharField(max_length=50)),
                ('rating', models.CharField(default='', max_length=5)),
                ('addUser', models.CharField(default='', max_length=50)),
                ('last_updated', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
