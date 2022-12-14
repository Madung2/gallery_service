# Generated by Django 4.1.1 on 2022-09-11 05:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0008_artistmodel_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="artistmodel",
            name="created_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="artistmodel",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
