from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('keuangan', views.keuangan, name='keuangan'),
    path('surat', views.surat, name='surat'),
    path('publikasi', views.publikasi, name='publikasi'),

]