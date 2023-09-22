from django.urls import path
from src.apps.account import views
from src.apps.post import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about_us', views.about_us, name='about_us'),
    path('services', views.services, name='services'),
    path('category_list', views.get_categories, name='category_list'),
    path('category_template/<int:id>/', views.category_template, name='category_template'),
    path('create_review/<int:doctor_id>/', views.create_review, name='create_review'),
    path('create_common_review/', views.create_common_review, name='create_common_review'),
    path('edit_review/<int:review_id>/', views.edit_review, name='edit_review'),
    path('delete_review/<int:review_id>/', views.delete_review, name='delete_review'),
    path('reviews/', views.review_list, name='review_list'),
    path('faq/', views.faq_list, name='faq_list'),
    path('rewards/', views.reward_list, name='reward_list'),
    path('service_template/<int:id>/', views.get_service, name='service_template'),
    path('doctor_reviews/<int:doctor_id>/', views.doctor_reviews, name='doctor_reviews'),
    path('privacy', views.view_privacy, name='view_privacy'),
  
]