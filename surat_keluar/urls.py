from . import views
from django.urls import path

urlpatterns = [
    path('form', views.formSk, name='formsk'),
    path('postform', views.postFormSk, name='postformsk'),
]