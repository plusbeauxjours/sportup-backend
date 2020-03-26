# Generated by Django 3.0.4 on 2020-03-26 03:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('feed', '0002_auto_20200325_1315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='poster_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post', to=settings.AUTH_USER_MODEL),
        ),
    ]