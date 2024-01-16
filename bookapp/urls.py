from django.urls import path, include, re_path
from django.contrib.auth import views as auth_views

from bookapp import views


urlpatterns = [
    re_path(r"^delete/(?P<pk>[0-9]+)/$", views.delete_book, name="deleteBook"),
    re_path(r'^lists/(\d+)/$', views.view_list, name='viewList'),
    re_path(r'^lists/new$', views.new_list, name='newList'),

    path('accounts/', include('django.contrib.auth.urls')),
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("", views.my_list, name="myList"),
]
