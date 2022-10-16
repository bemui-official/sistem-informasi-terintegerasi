from . import views
from django.urls import path

app_name = 'sb'

urlpatterns = [
    path('form', views.formSb, name='formsb'),
    path('postformsb', views.postFormSb, name='postformsb'),
    path('detail/<str:id>', views.detail, name='detail'),
    path('diterima1', views.diterima_1, name='diterima1'),
    path('diterima2', views.diterima_2, name='diterima2'),
    path('diterima4', views.diterima_4, name='diterima4'),
    path('ditolak4', views.ditolak_4, name='ditolak4'),
    path('dibatalkan', views.dibatalkan, name='dibatalkan'),
    path('detail/3/<str:id>', views.form3, name='form3'),
    path('postform3', views.postForm3, name='postform3'),
    path('delete', views.delete, name='delete')
]