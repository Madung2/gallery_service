from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns =[
    path("art/", views.ArtListView.as_view(), name="art"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)