from django.shortcuts import render
from rest_framework.generics import (CreateAPIView)
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.response import Response

from art.models import ArtModel
from art.serializers import ArtSerializer

class ArtListView(CreateAPIView):
    renderer_classes = [JSONRenderer, TemplateHTMLRenderer]
    template_name = 'main.html'

    def get(self, request):
        all_arts = ArtModel.objects.all().order_by('-created_at')
        serializer = ArtSerializer(all_arts, many=True).data
        return Response({'art':serializer}, template_name= 'art.html')
