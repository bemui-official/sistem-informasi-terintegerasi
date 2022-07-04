from . import views
from django.urls import path

app_name = 'sk'

urlpatterns = [
    path('form', views.formSk, name='formsk'),
    path('postform', views.postFormSk, name='postformsk'),
    path('detail/<str:id>', views.detail, name='detail'),
    path('diterima1', views.diterima_1, name='diterima1'),
    path('diterima2', views.diterima_1, name='diterima2'),
    path('dibatalkan', views.dibatalkan, name='dibatalkan'),
    path('detail/3/<str:id>', views.form3, name='form3'),
    path('postform3', views.postForm3, name='postform3'),
]