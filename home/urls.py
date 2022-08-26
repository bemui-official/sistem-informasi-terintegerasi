from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('team', views.team, name='team'),
    path('keuangan', views.keuangan, name='keuangan'),
    path('surat', views.surat, name='surat'),
    path('publikasi', views.publikasi, name='publikasi'),
    path('survei', views.survei, name='survei'),
]