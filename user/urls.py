from . import views
from django.urls import path

urlpatterns = [
    path('signup', views.signUp, name='signup'),
    path('postsignup', views.postSignUp, name='postsignup'),
    path('signin', views.signIn, name='signin'),
    path('postsignin', views.postSignIn, name='postsignin'),
    path('logout', views.logout, name='logout'),
    path('give_permission', views.give_permission, name='give_permission'),
    path('post_give_permission', views.post_give_permission, name='post_give_permission'),
    path('dashboard/<str:category>/<str:sort>', views.dashboard, name='dashboard'),
    path('dashboard_pengurus/<str:category>/<str:sort>', views.dashboard_pengurus, name='dashboard_pengurus'),
]