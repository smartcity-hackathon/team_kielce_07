# Generated by Django 2.0.6 on 2018-06-16 02:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dodawarka', '0006_offer_compare_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='compare_user',
            field=models.ManyToManyField(related_name='to_compare', to=settings.AUTH_USER_MODEL),
        ),
    ]