from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class UserModel(AbstractUser):
    class Meta:
        db_table = "user"
    def __str__(self):
        return self.username

    is_artist=models.BooleanField("작가 여부", default=False)
    
    # user_type_choices=(
    #     ('1','general_user'),
    #     ('2', 'artist'),
    # )
    # user_type= models.CharField("유저타입", max_length=6, choices=user_type_choices, null=True, blank=True)

