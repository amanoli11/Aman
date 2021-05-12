from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('signup', views.signup),
    path('home', views.home),
    path('logout', views.logoutUser, name='logout')
]