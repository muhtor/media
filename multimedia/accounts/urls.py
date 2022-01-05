from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path('auth', views.AuthenticationApiView.as_view(), name="auth"),
    path('media', views.MultiMediaApiView.as_view(), name="media"),
]