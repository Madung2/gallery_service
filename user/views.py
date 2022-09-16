from functools import partial
from django.shortcuts import  redirect
# from django.contrib import auth
from django.contrib.auth import authenticate, login
from rest_framework import status

from rest_framework.views import APIView
# from rest_framework.generics import CreateAPIView, APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, UserArtistSerializer, StaffArtistSerializer, ArtistStaticSerializer
# from .serializers_jwt import TokenObtainPairSerializer
from .models import UserModel, ArtistModel
from art.models import ArtModel
from art.serializers import ArtSerializer
from gallery_service.permissions import IsAthenticatedButNotArtist, IsAthenticatedAndStaffOnly
# Create your views here.


def valid_password(request):
    return bool(request['password']==request['password2'])

def valid_request(request):
    return bool(request['username'] and request['password'] and request['password2'])

def make_artist_apply_data(request):
    data = request.data.copy()
    data['user_id']=request.user.id
    data['email']=data['email1']+'@'+data['email2']
    data['phone_number']=data['phone1']+'-'+data['phone2']+'-'+data['phone3']
    return data

def home(request):
    return redirect('/user/art')

class UserCreateView(APIView):
    """
    모든 anonymous 접근 가능 페이지
    회원 가입 페이지 뷰
    
    """
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'signup.html'

    def get(self, request):
        all_users = UserModel.objects.all().order_by('-date_joined')
        serializer = UserSerializer(all_users, many=True).data
        return Response({'user_list':serializer}, template_name= 'signup.html')

    def post(self, request):
        if valid_request(request.data):
            if valid_password(request.data):
                serializer = UserSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(template_name = 'signin.html')#redirect('signin.html')
                return Response({'error':"회원가입 정보가 정확하지 않습니다"}, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error':'비밀번호 확인을 위해 동일한 비밀번호를 입력해주세요'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'빈칸을 채워주세요'}, status=status.HTTP_400_BAD_REQUEST)

class LoginPageView(APIView):
    """
    모든 anonymous 접근 가능 페이지
    로그인 페이지 뷰
    
    """
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'signin.html'
    def get(self, request):
        return Response(template_name= 'signin.html')
    def post(self, request):
        data = request.data.copy()
        username = data['username']
        password = data['password']
        auth_user = authenticate(request, username=username, password=password)
        if not auth_user:
            return Response({"error": "존재하지 않는 계정이거나 비밀번호가 일치하지 않습니다."},
                            status=status.HTTP_400_BAD_REQUEST)        
        login(request, auth_user)
        return redirect('/user/art')

class UserArtistView(APIView):
    """
    일반 유저 및 anonymous 접근 가능 페이지
    고객 페이지: 작가목록 조회 페이지
    
    """
    serializer_class = UserArtistSerializer
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'main.html'

    def get(self, request):
        all_artists = ArtistModel.objects.all().order_by('-created_at')
        serializer = UserArtistSerializer(all_artists, many=True).data
        return Response({'artists':serializer}, template_name= 'u_artist.html')

class UserApplyView(APIView):
    """
    일반 유저 및 anonymous 접근 가능 페이지
    고객 페이지: 작가 등록 신청 페이지
    
    """    
    serializer_class = UserArtistSerializer
    permission_classes = [IsAthenticatedButNotArtist]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'u_apply.html'

    def get(self, request):
        try:
            return Response(template_name= 'u_apply.html')
        except:
            return Response({'error':"권한이 없습니다"}, template_name='u_art.html' )

    def post(self,request):
        try:
            data= make_artist_apply_data(request)
            serializer = UserArtistSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'result':"작가 신청이 정상적으로 이루어졌습니다."},template_name = 'u_art.html')
            return Response({'error':"작가 신청이 정상적으로 이루어지지 않았습니다"}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'error':"입력된 데이터가 정확하지 않습니다"}, status=status.HTTP_400_BAD_REQUEST)

class StaffDashboardView(APIView):
    """
    관리자 계정 접근 가능 페이지
    관리자 페이지: 대시보드 페이지
    
    """  
    serializer_class = UserArtistSerializer
    permission_classes = [IsAthenticatedAndStaffOnly]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 's_dashboard.html'
    def get(self, request):
        all_artists = ArtistModel.objects.all().order_by('-created_at')
        artist_serializer = UserArtistSerializer(all_artists, many=True).data
        all_arts = ArtModel.objects.all().order_by('-created_at')
        art_serializer = ArtSerializer(all_arts, many=True).data
        return Response({'artists':artist_serializer, 'arts':art_serializer},template_name= 's_dashboard.html')



class StaffStaticView(APIView):
    """
    관리자 계정 접근 가능 페이지
    관리자 페이지: 작가 통계 페이지
    
    """  
    serializer_class = ArtistStaticSerializer
    permission_classes = [IsAthenticatedAndStaffOnly]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 's_static.html'
    def get(self, request):
        all_artists = ArtistModel.objects.all().order_by('-created_at')
        serializer = ArtistStaticSerializer(all_artists, many=True).data
        return Response({'artists':serializer},template_name= 's_static.html')



class StaffApplicationView(APIView):
    """
    관리자 계정 접근 가능 페이지
    관리자 페이지: 작가 등록 신청 내역 조회 페이지
    
    """  
    serializer_class = StaffArtistSerializer
    permission_classes = [IsAthenticatedAndStaffOnly]
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 's_application.html'
    def get(self, request):
        all_artists = ArtistModel.objects.all().order_by('-created_at')
        serializer = StaffArtistSerializer(all_artists, many=True).data
        return Response({'artists':serializer},template_name= 's_application.html')

    def post(self, request):
        id_array= request.data.getlist('is_not_waiting', False)

        for id in id_array:
            target_artist= ArtistModel.objects.get(user_id=id)
            data={"is_confirmed":1, "is_waiting":0}
            serializer = StaffArtistSerializer(target_artist, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                target_user= UserModel.objects.get(id=id)
                data2={"is_artist":1}
                serializer2 = UserSerializer(target_user, data=data2, partial=True)
                if serializer2.is_valid():
                    serializer.save()
                    all_artists = ArtistModel.objects.all().order_by('-created_at')
                    return_serializer = StaffArtistSerializer(all_artists, many=True).data
                    return Response({'artists':return_serializer},template_name= 's_application.html')
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





