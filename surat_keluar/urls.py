from . import views
from django.urls import path

app_name = 'sk'

urlpatterns = [
    path('form', views.formSk, name='formsk'),
    path('postformsk', views.postFormSk, name='postformsk'),
    path('detail/<str:id>', views.detail, name='detail'),
    path('diterima1', views.diterima_1, name='diterima1'),
    path('diterima3', views.diterima_3, name='diterima2'),
    path('ditolak3', views.ditolak_3, name='ditolak3'),
    path('detail/2/<str:id>', views.form2, name='form2'),
    path('postform2', views.postForm2, name='postform2'),
    path('delete', views.delete, name='delete')

]