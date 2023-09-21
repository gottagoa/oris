from django.urls import path
from src.apps.account import views



urlpatterns = [
  
    path('login/', views.LoginView.as_view(), name='login'),
    path("logout/",views.user_logout, name="logout"),
    path("register/", views.register_user, name="register"),
    path('register/done/', views.registration_done, name='registration_done'),
    path('edit/profile/', views.UserUpdateProfile.as_view(), name="edit_profile"),
    path('profile/', views.get_user_profile, name="profile"),
    path('change_password/', views.change_password, name='change_password'),
    path('doctors/', views.doctors, name='doctors'),
    path('doctor_template/<int:pk>/', views.get_doctor, name='doctor_template'),
    path('doctor/plan/', views.add_doctor_availability, name="doctor_plan"),
    path('doctor/<int:doctor_id>/', views.view_doctor_availability, name='view_doctor_availability'),
    path('doctor/book/', views.book_appointment, name='book_appointment'),
    path('doctor/available_slots_of_doctors/', views.available_slots_of_doctors, name="available_slots_of_doctors"),
    path('doctor/available_slots/', views.get_available_time_slot, name="available_slots"),
    path('create_medical_record/<int:appointment_id>/', views.create_medical_record, name='create_medical_record'),
    path('medical_records/', views.view_records_list, name='view_records_list'),
    path('patient_records/', views.patient_records, name='patient_records'),
]
    


