from . import views
from django.urls import path

app_name = 'sb'

urlpatterns = [
    path('create/', views.formPublikasi, name='publikasiCreate'),
    path('spo/', views.spo_publikasi, name='spoPublikasi'),
    path('detail/<str:id>', views.detail, name='detail'),
    path("delete/", views.delete_publikasi, name = 'delete')
]