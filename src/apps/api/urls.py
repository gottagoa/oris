from django.urls import path

from src.apps.api import views

urlpatterns = [
    path("get_doctors_by_category/<str:slug>/", views.DoctorsListAPIView.as_view()), 
    path("create/appointment/", views.create_appointment),
    path('get/doctor/availibity/<int:pk>/', views.get_doctor_availibity)
]