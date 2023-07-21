from django.urls import path
from . import views

app_name = 'linebotsip'

urlpatterns = [
	path('', views.index, name='index'),
	path('callback/', views.callback, name='callback'),
]