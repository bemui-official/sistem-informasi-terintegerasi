from django.urls import path
from .misc import uploadPhoto

urlpatterns = [
    path('upload-photo/', uploadPhoto.uploadPhoto, name='upload_photo')
]