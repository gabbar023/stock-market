from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
urlpatterns = [
    path('', views.home,name="home"),
    path('about/', views.about, name="about"),
    path('login/', auth_views.LoginView.as_view(template_name='aa/login.html'),name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name='aa/logout.html'),name="logout"),
    path('register/', views.register, name="register"),
    path('profile/', views.profile, name="profile"),
    path('creg/', views.companyreg, name="creg"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('contact/', views.contact, name="contact"),
    path('db/', views.db, name="db"),
    path('sellbuy/',views.sellbuy,name='sellbuy'),
    url(r'^(?P<stockQuotes_id>[0-9]+)/$', views.something, name='something'),
    ]