from . import views
from django.urls import path

app_name = 'publikasi'

urlpatterns = [
    path('create/', views.formPublikasi, name='publikasiCreate'),
    path('spo/', views.spo_publikasi, name='spoPublikasi'),
    path('detail/<str:id>', views.detail, name='detail'),
    path("delete/", views.delete_publikasi, name = 'delete'),
    path('diterima1', views.diterima_1, name='diterima1'),
    path('diterima2', views.diterima_2, name='diterima2'),    path('diterima3', views.diterima_3, name='diterima3'),
    path('diterima4', views.diterima_4, name='diterima4'),
    path('declineRequest/<str:id>/<int:tahapan>', views.declineRequest, name='declineRequest'),
    path("edit/<str:id>", views.edit_publikasi, name = "editPublikasi")
]