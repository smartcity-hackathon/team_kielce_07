# Generated by Django 2.0.6 on 2018-06-16 02:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dodawarka', '0005_auto_20180616_0337'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='compare_user',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]