from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultancy/', views.consultancy, name='consultancy'),
    path('wine_variety_stats/', views.wine_variety_stats, name='wine_variety_stats'),
]
