from django.db.models.query_utils import Q

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from .models import ArtistModel
from art.models import ArtModel
from art.serializers import ArtSerializer, ExhibitionArtSerializer, ExhibitionSerializer
from gallery_service.permissions import IsAthenticatedAndArtistOnly




class ArtListView(APIView):
    """
    일반유저 및 anonymous유저 접근 가능 페이지
    작품 목록 조회 페이지 뷰
    
    """
    serializer_class = ArtSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'u_art.html'

    def get(self, request):
        word = self.request.query_params.get("search")
        if word:
            query = Q()
            query.add(Q(name__icontains=word), Q.OR)
            query.add(Q(number__contains=word), Q.OR)
            query.add(Q(price__contains=word), Q.OR)
            all_arts = ArtModel.objects.filter(query).order_by('-created_at')
        else:
            all_arts = ArtModel.objects.all().order_by('-created_at')
        serializer = ArtSerializer(all_arts, many=True).data
        return Response({'arts':serializer}, template_name= 'u_art.html')


class ArtistDashboardView(APIView):
    """
    작가 접근 가능 페이지
    작가 페이지: 대시보드
    
    """
    permission_classes = [IsAthenticatedAndArtistOnly]
    serializer_class = ArtSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'a_dashboard.html'

    def get(self, request):
        all_arts = ArtModel.objects.all()
        serializer = ArtSerializer(all_arts, many=True).data
        return Response({'arts':serializer},template_name= 'a_dashboard.html')

class ArtistArtView(APIView):
    """
    작가 접근 가능 페이지
    작가 페이지: 작품등록 페이지
    
    """
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
        

class ArtistExhibitionView(APIView):
    """
    작가 접근 가능 페이지
    작가 페이지: 전시 등록 페이지
    
    """
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
        artist_id= ArtistModel.objects.get(user_id_id=request.user.id).id
        data = request.data.copy()
        data['artist']=artist_id
        serializer=ExhibitionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result':"전시가 추가되었습니다"},template_name = 'a_exhibition.html')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)