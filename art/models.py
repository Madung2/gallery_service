from django.db import models
from django.core.validators import RegexValidator, MaxValueValidator, MinValueValidator

from user.models import ArtistModel

class ArtModel(models.Model):
    class Meta:
        db_table = 'art'
    def __str__(self):
        return f'{self.name}, ({self.artist.name})'

    name = models.CharField("작품명",max_length=64)
    artist = models.ForeignKey(ArtistModel, related_name ='arts', on_delete=models.CASCADE)
    size = models.CharField("사이즈", max_length=200)
    number = models.IntegerField("호수", validators=[MinValueValidator(1), MaxValueValidator(500)])
    price = models.IntegerField("가격", default=0, validators=[MinValueValidator(0)])
    image = models.FileField(upload_to='uploads/',null=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)



class ExhibitionModel(models.Model):
    class Meta:
        db_table = 'exhibition'
    def __str__(self):
        return f'{self.name}, ({self.artist.name})'
    
    name = models.CharField("전시회명", max_length=50)
    artist = models.ForeignKey(ArtistModel, on_delete= models.CASCADE)
    art_list = models.ManyToManyField(ArtModel, related_name='exhibition', verbose_name="작품리스트")
    date_regex = RegexValidator(regex = r'^([0-9]{4})-([0-9]{2})-([0-9]{2})$')
    start_date= models.CharField("시작일",validators = [date_regex], max_length = 11, unique = False, null=True, blank=True)
    end_date= models.CharField("종료일",validators = [date_regex], max_length = 11, unique = False, null=True, blank=True)
