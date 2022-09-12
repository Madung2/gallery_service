from django.shortcuts import render, redirect

from rest_framework import status
from rest_framework.generics import (CreateAPIView)
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import UserSerializer, UserArtistSerializer
from .serializers_jwt import TokenObtainPairSerializer
from .models import UserModel, ArtistModel

# Create your views here.


def valid_password(request):
    return bool(request['password']==request['password2'])

def valid_request(request):
    return bool(request['username'] and request['password'] and request['password2'])


class UserCreateView(CreateAPIView):
    """
    회원가입 페이지 view
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

class LoginPageView(CreateAPIView, TokenObtainPairView):
    """_
    로그인 페이지 view
    """
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'signin.html'
    serializer_class = TokenObtainPairSerializer
    def get(self, request):
        return Response(template_name= 'signin.html')        

class TokenObtainPairView(TokenObtainPairView):
    """
    Login을 구현하는 View
    내부에서 UserLog를 생성하는 함수 내장
    """
    serializer_class = TokenObtainPairSerializer



class ArtistListView(CreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'main.html'

    def get(self, request):
        all_artists = ArtistModel.objects.all().order_by('-created_at')
        serializer = UserArtistSerializer(all_artists, many=True).data
        return Response({'artists':serializer}, template_name= 'u_artist.html')




class ArtistApplyView(CreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'u_apply.html'

    def get(self, request):
        return Response(template_name= 'u_apply.html')

    def post(self,request):
        serializer = UserArtistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'result':"작가 신청이 정상적으로 이루어졌습니다."},template_name = 'u_art.html')


