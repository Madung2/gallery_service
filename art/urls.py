from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns =[
    path("user/art/", views.ArtListView.as_view(), name="art"),
    path("artist/dashboard/", views.ArtistDashboardView.as_view(), name="artist_dashboard"),
    path("artist/art/", views.ArtistArtView.as_view(), name="artist_art"),
    path("artist/exhibition/", views.ArtistExhibitionView.as_view(), name="artist_exhibition"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)