from . import views
from django.urls import path

urlpatterns = [
    path('signup', views.signUp, name='signup'),
    path('postsignup', views.postSignUp, name='postsignup'),
    path('signin', views.signIn, name='signin'),
    path('postsignin', views.postSignIn, name='postsignin'),
    path('logout', views.logout, name='logout'),
    path('dashboard/<str:category>/<str:sort>', views.dashboard, name='dashboard')

]