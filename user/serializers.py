from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import ArtistModel, UserModel, ArtistModel
from art.models import ArtModel


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        post=UserModel(**validated_data)
        post.save()
        return validated_data

    class Meta:
        model = UserModel
        fields = ['username', 'password', 'is_staff', 'is_artist','date_joined']

        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserArtistSerializer(serializers.ModelSerializer):
    art_num = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    def get_art_num(self, obj):
        return ArtModel.objects.filter(artist=obj.id).count()   

    def get_image(self,obj):
        a=ArtModel.objects.filter(artist=obj.id)
        if a:
            return '2.png'
        return '1.png'

    class Meta:
        model = ArtistModel
        fields=['user_id','name','gender','birthday','phone_number','email', 'art_num' , 'image']

class StaffArtistSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()

    def get_date(self, obj):
        return str(obj.created_at)[:10]

    class Meta:
        model = ArtistModel
        fields=['user_id','name','gender','birthday','phone_number','email','is_waiting','is_confirmed','created_at', 'date']

class ArtistStaticSerializer(serializers.ModelSerializer):
    price = serializers.SerializerMethodField()
    over_under_100 = serializers.SerializerMethodField()

    def get_price(self, obj):
        """_summary_

        Args:
            obj (_type_): _description_

        Returns:
            _type_: _description_
        """
        arts = ArtModel.objects.filter(artist=obj.id).all()
        price = [art.price for art in arts]

        try:
            avg = int(sum(price)/len(price))
        except ZeroDivisionError:
            avg = 0
        
        try:
            max_n = max(price)
        except ValueError:
            max_n = 0 

        try:
            min_n = min(price)
        except ValueError:
            min_n = 0 

        return {'avg': avg, 'max_n':max_n, 'min_n':min_n}
        

    def get_over_under_100(self, obj):
        arts = ArtModel.objects.filter(artist=obj.id).all()
        under_count=0
        over_count=0
        for art in arts:
            if art.number<100:
                under_count+=1
            if art.number>=100:
                over_count+=1
        return {'over_100':over_count, 'under_100':under_count}

    class Meta:
        model = ArtistModel
        fields= ['user_id','name','gender','birthday','phone_number','email', 'price', 'over_under_100']


