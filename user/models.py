from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.

class UserModel(AbstractUser):
    class Meta:
        db_table = "user"
    def __str__(self):
        return self.username

    is_artist=models.BooleanField("작가 여부", default=False)
    

class ArtistModel(models.Model):
    class Meta:
        db_table = 'artist'
    def __str__(self):
        return self.name

    user_id= models.ForeignKey(UserModel, related_name='artist_names', on_delete=models.CASCADE)
    name= models.CharField("성명",max_length=16)
    gender= models.BooleanField("성별",default=False) #0=남자 1=여자
    birthday_regex = RegexValidator(regex = r'^([0-9]{4})-?([0-9]{2})-?([0-9]{2})$')
    birthday= models.CharField("생일",validators = [birthday_regex], max_length = 11, unique = False, null=True, blank=True)
    phone_regex = RegexValidator(regex = r'^01([0|1|6|7|8|9]?)-?([0-9]{3,4})-?([0-9]{4})$')
    phone_number= models.CharField("연락처",validators = [phone_regex], max_length = 13, unique = True, null=True, blank=True)
    email=models.CharField("이메일", max_length=120, null=True, blank=True)
    is_waiting=models.BooleanField("처리대기중", default=True)
    is_confirmed= models.BooleanField("승인처리완료", default=False)

