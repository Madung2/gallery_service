from django.shortcuts import render, redirect

from rest_framework.generics import (CreateAPIView)
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer
from .models import UserModel
# Create your views here.

class UserCreateView(CreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'signup.html'

    def get(self, request):
        all_users = UserModel.objects.all().order_by('-date_joined')
        serializer = UserSerializer(all_users, many=True).data
        return Response({'user_list':serializer}, template_name= 'signup.html')

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("*****")
            return redirect('signin.html')
        return Response({'result':"회원가입 실패"})
