from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('consultancy/', views.consultancy, name='consultancy'),
    path('wine_variety_stats/', views.wine_variety_stats, name='wine_variety_stats'),
    path('variety_options/', views.variety_options, name='variety_options'),
    path('variety_reviews/<int:variety_id>', views.variety_reviews, name='variety_reviews'),
    path('review_create/', views.review_create, name='review_create'),
    path('review_delete/<int:review_id>', views.review_delete, name='review_delete'),
    path('review_like/<int:review_id>', views.review_like, name='review_like'),
]
