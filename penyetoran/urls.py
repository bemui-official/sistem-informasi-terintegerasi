from . import views
from django.urls import path

urlpatterns = [
    path('form', views.formKs, name='formks'),
    path('postformks', views.postFormKs, name='postformks'),
]