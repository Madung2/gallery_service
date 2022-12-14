# Generated by Django 4.1.1 on 2022-09-10 04:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("user", "0002_usermodel_is_artist"),
    ]

    operations = [
        migrations.CreateModel(
            name="ArtistModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=16, verbose_name="성명")),
                ("gender", models.BooleanField(default=False, verbose_name="성별")),
                (
                    "birthday",
                    models.CharField(
                        blank=True,
                        max_length=11,
                        null=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="^?([0-9]{4})-?([0-9]{2})-?([0-9]{2})$"
                            )
                        ],
                        verbose_name="생일",
                    ),
                ),
                (
                    "phone_number",
                    models.CharField(
                        blank=True,
                        max_length=13,
                        null=True,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                regex="^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$"
                            )
                        ],
                        verbose_name="연락처",
                    ),
                ),
                ("is_waiting", models.BooleanField(default=True, verbose_name="처리대기중")),
                (
                    "is_confirmed",
                    models.BooleanField(default=False, verbose_name="승인처리완료"),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="artist_names",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"db_table": "artist",},
        ),
    ]
