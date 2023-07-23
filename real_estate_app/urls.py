from django.urls import path     
from . import views

urlpatterns = [
    path('test',views.get),
    path('', views.index),
    path('sort_properties', views.sort_properties),
    path('register', views.register),
    path('login', views.login),
    path('login_signup', views.login_signup),
    path('properties', views.properties),
    path('properties/new', views.properties_new),
    path('properties/create', views.properties_create),
    path('properties/<int:id>', views.properties_single),
    path('properties/<int:id>/edit', views.properties_edit),
    path('properties/<int:id>/update', views.properties_update),
    path('properties/<int:id>/delete', views.properties_delete),
    path('properties/favorite', views.properties_fav),
    path('properties/<int:id>/addfavorite', views.properties_add_fav),
    path('properties/<int:id>/removefavorite', views.properties_remove_fav),
    path('logout',views.logout),
]