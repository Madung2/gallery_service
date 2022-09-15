from rest_framework import serializers
from .models import ArtModel, ExhibitionModel
# from user.serializers import UserArtistSerializer

class ArtSerializer(serializers.ModelSerializer):
    artist_name = serializers.SerializerMethodField()

    def get_artist_name(self, obj):
        return obj.artist.name

    class Meta:
        model = ArtModel
        fields = ['id', 'name','artist','size','number','price','image','updated_at','created_at', 'artist_name']



class ExhibitionArtSerializer(serializers.ModelSerializer):

    class Meta:
        model = ArtModel
        fields = ['id', 'name','artist']


class ExhibitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExhibitionModel
        fields = '__all__'

