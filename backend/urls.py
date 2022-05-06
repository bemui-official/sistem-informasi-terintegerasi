from django.urls import path, include
from . import uploadPhoto

urlpatterns = [
    path('upload-photo/', uploadPhoto.uploadPhoto, name='upload_photo')
]