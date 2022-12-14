# Generated by Django 4.1.1 on 2022-09-10 05:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("art", "0003_alter_artmodel_artist_exhibitionmodel"),
    ]

    operations = [
        migrations.AddField(
            model_name="exhibitionmodel",
            name="end_date",
            field=models.CharField(
                blank=True,
                max_length=11,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^([0-9]{4})-([0-9]{2})-([0-9]{2})$"
                    )
                ],
                verbose_name="종료일",
            ),
        ),
        migrations.AddField(
            model_name="exhibitionmodel",
            name="start_date",
            field=models.CharField(
                blank=True,
                max_length=11,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        regex="^([0-9]{4})-([0-9]{2})-([0-9]{2})$"
                    )
                ],
                verbose_name="시작일",
            ),
        ),
    ]
