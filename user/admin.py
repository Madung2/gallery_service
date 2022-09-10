from django.contrib import admin
from .models import UserModel, ArtistModel

# Register your models here.
admin.site.register(UserModel)
admin.site.register(ArtistModel)