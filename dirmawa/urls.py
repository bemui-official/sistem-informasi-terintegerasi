from . import views
from django.urls import path

urlpatterns = [
    path('form', views.formSd, name='formsd'),
    path('postformsd', views.postFormSd, name='postformsd'),
]