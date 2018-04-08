from django.urls import path
from django.conf.urls import url, include
from winereviews.views import ReviewList, ReviewCreate, ReviewUpdate, ReviewDelete
from winereviews.views import WineList, WineCreate, WineUpdate, WineDelete
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultancy/', views.consultancy, name='consultancy'),
    path('wine_variety_stats/', views.wine_variety_stats, name='wine_variety_stats'),
    path('variety_options/', views.variety_options, name='variety_options'),
    path('variety_reviews/<int:variety_id>', views.variety_reviews, name='variety_reviews'),

    # Reviews CRUD
    path('reviews/', ReviewList.as_view()),
    path('review/add/', ReviewCreate.as_view(), name='review_add'),
    path('review/<int:pk>/', ReviewUpdate.as_view(), name='review_update'),
    path('review/<int:pk>/delete/', ReviewDelete.as_view(), name='review_delete'),
    path('review/<int:pk>/detail', views.review_detail, name='review_detail'),

    # Wines CRUD
    path('wines/', WineList.as_view(), name='wine_list'),
    path('wine/add/', WineCreate.as_view(), name='wine_add'),
    path('wine/<int:pk>/', WineUpdate.as_view(), name='wine_update'),
    path('wine/<int:pk>/delete/', WineDelete.as_view(), name='wine_delete'),
    path('wine/<int:pk>/detail', views.wine_detail, name='wine_detail'),
    path('wine/<int:pk>/review/', views.wine_review_create, name='wine_review_create'),

]
