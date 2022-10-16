from . import views
from django.urls import path

urlpatterns = [
    path('form', views.formKs, name='formks'),
    path('postformks', views.postFormKs, name='postformks'),
    path('detail/<str:id>', views.detail, name='detail'),
    path('diterima', views.diterima, name='diterima'),
    path('diterima2', views.diterima2, name='diterima2'),
    path('dibatalkan', views.dibatalkan, name='dibatalkan'),
    path('detail/1/<str:id>', views.form1, name='form1'),
    path('postform1', views.postForm1, name='postform1'),
    path('detail/2/<str:id>', views.form2, name='form2'),
    path('postform2', views.postForm2, name='postform2'),
    path('delete', views.delete, name='delete')

]