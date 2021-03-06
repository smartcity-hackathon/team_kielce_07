# Generated by Django 2.0.6 on 2018-06-16 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dodawarka', '0003_auto_20180616_1430'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='centre_distance',
            field=models.IntegerField(verbose_name='Odległość od centrum (m)'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Cena (zł)'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='surface',
            field=models.DecimalField(decimal_places=2, max_digits=20, verbose_name='Powierzchnia (m2)'),
        ),
    ]
