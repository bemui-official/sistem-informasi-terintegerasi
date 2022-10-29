"""sit_bemui URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('home.urls', 'home'), namespace='home')),
    path('user/', include(('user.urls', 'user'), namespace='user')),
    path('surat_keluar/', include(('surat_keluar.urls', 'sk'), namespace='sk')),
    path('reimbursement/', include(('reimbursement.urls', 'kr'), namespace='kr')),
    path('penyetoran/', include(('penyetoran.urls', 'ks'), namespace='ks')),
    path('advanced/', include(('advanced.urls', 'ka'), namespace='ka')),
    path('surat_besar/', include(('surat_besar.urls', 'sb'), namespace='sb')),
    path('backend/', include('backend.urls')),
    path('linebotsit/', include('linebotsit.urls')),
]

handler404 = "sit_bemui.views.page_not_found_view"
