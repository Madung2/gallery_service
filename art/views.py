from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from art.models import ArtModel
from .models import ArtistModel
from art.serializers import ArtSerializer, ExhibitionArtSerializer
from gallery_service.permissions import IsAthenticatedAndArtistOnly

class ArtListView(CreateAPIView):
    serializer_class = ArtSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'u_art.html'

    def get(self, request):
        all_arts = ArtModel.objects.all().order_by('-created_at')
        serializer = ArtSerializer(all_arts, many=True).data
        return Response({'arts':serializer}, template_name= 'u_art.html')

class ArtistDashboardView(CreateAPIView):
    permission_classes = [IsAthenticatedAndArtistOnly]
    serializer_class = ArtSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'a_dashboard.html'
    def get(self, request):
        all_arts = ArtModel.objects.all()
        serializer = ArtSerializer(all_arts, many=True).data
        return Response({'arts':serializer},template_name= 'a_dashboard.html')

class ArtistArtView(CreateAPIView):
    permission_classes = [IsAthenticatedAndArtistOnly]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'a_artupload.html'
    def get(self, request):        
        return Response(template_name= 'a_artupload.html')
    def post(self, request):
        new_price = int(request.data['price'].replace(',',''))
        artist_id= ArtistModel.objects.get(user_id_id=request.user.id).id
        request.data['artist']=artist_id
        request.data['price']=new_price
        serializer=ArtSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result':"작품이 추가되었습니다"},template_name = 'a_artupload.html')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ArtistExhibitionView(CreateAPIView):
    permission_classes = [IsAthenticatedAndArtistOnly]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'a_exhibition.html'
    def get(self, request):
        artist_id= ArtistModel.objects.get(user_id_id=request.user.id).id
        try: #art model에서 artist_id가 같은 작품의 id와 이름
            arts_data = ArtModel.objects.filter(artist_id=artist_id).all()
            arts = ExhibitionArtSerializer(arts_data, many=True).data
        except:
            arts = "작품을 등록해주세요"
        return Response({"arts":arts}, template_name= 'a_exhibition.html')

    def post(self, request):

        return Response(template_name= 'a_exhibition.html')