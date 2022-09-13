from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.UserCreateView.as_view(), name="signup"),
    path("login/", views.LoginPageView.as_view(), name="login"),
    path('token/', views.TokenObtainPairView.as_view(), name="gallery_token"),
    path("artist/", views.ArtistListView.as_view(), name="artist"),
    path("apply/", views.ArtistApplyView.as_view(), name="apply"),
    path("staff/dashboard/", views.StaffDashboardView.as_view(), name="staff"),
    path("staff/static/", views.StaffStaticView.as_view(), name="static"),
    path("staff/application/", views.StaffApplicationView.as_view(), name="application"),
]