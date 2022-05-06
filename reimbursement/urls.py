from . import views
from django.urls import path

urlpatterns = [
    path('form', views.formKr, name='formkr'),
    path('postformkr', views.postFormKr, name='postformkr'),
]