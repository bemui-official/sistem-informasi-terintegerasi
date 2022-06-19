from . import views
from django.urls import path

urlpatterns = [
    path('form', views.formKr, name='formkr'),
    path('postformkr', views.postFormKr, name='postformkr'),
    path('<str:id>', views.detail, name='detail'),
    path('1/<str:id>', views.form1, name='form1'),

]