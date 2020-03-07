from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),
]
