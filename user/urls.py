from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.UserCreateView.as_view(), name="signup"),
    path("login/", views.LoginPageView.as_view(), name="login"),
    path('token/', views.TokenObtainPairView.as_view(), name="gallery_token"),
    path("main/", views.MainView.as_view(), name="main"),

]