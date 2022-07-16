from . import views
from django.urls import path

app_name = 'sb'

urlpatterns = [
    path('form', views.formSb, name='formsb'),
    path('postformsb', views.postFormSb, name='postformsb'),
    path('detail/<str:id>', views.detail, name='detail'),
    path('diterima1', views.diterima_1, name='diterima1'),
    path('diterima2', views.diterima_2, name='diterima2'),
    path('diterima3', views.diterima_3, name='diterima3'),
    path('dibatalkan', views.dibatalkan, name='dibatalkan'),
    path('detail/4/<str:id>', views.form4, name='form4'),
    path('postform4', views.postForm4, name='postform4'),
]