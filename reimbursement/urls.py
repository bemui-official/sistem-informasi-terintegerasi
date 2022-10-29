from . import views
from django.urls import path

urlpatterns = [
    path('form', views.formKr, name='formkr'),
    path('postformkr', views.postFormKr, name='postformkr'),
    path('detail/<str:id>', views.detail, name='detail'),
    path('diterima', views.diterima, name='diterima'),
    path('dibatalkan', views.dibatalkan, name='dibatalkan'),
    path('detail/1/<str:id>', views.form1, name='form1'),
    path('postform1', views.postForm1, name='postform1'),
    path('detail/2/<str:id>', views.form2, name='form2'),
    path('postform2', views.postForm2, name='postform2'),
]