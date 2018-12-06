from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path(r'^category/(?P.*?)/*$',    views.list,             name='entry_list'),
    path(r'^author/(?P.*?)/*$',      views.list,             name='entry_list'),
    path(r'^date/(?P.*?)/*$',            views.list,             name='entry_list'),
    path(r'^$',                                views.list,             name='entry_list'),
]