from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.mixins import LoginRequiredMixin
# from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from django.views.generic import FormView, CreateView, UpdateView, ListView,TemplateView, DetailView
from .models import Patient, User, Doctor, DoctorAvailability, Appointment, MedicalRecord
from src.apps.account.forms import LoginForm, UserRegisterForm, UserUpdateForm, SpecialistAppointmentForm
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from src.apps.post.models import About, Category
from .forms import AppointmentForm, MedicalRecordForm
from datetime import datetime, date
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.utils.timezone import now
from django.http import JsonResponse
from datetime import datetime, timedelta
import json 


def register_user(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data["password1"]
            user = User.objects.create(
                # username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                birthday=form.cleaned_data["birthday"],
                is_active=form.cleaned_data["is_active"],
                is_staff=form.cleaned_data["is_staff"],
                mobile=form.cleaned_data["mobile"],
                gender=form.cleaned_data["gender"],
            )
            user.set_password(password)
            user.save()
            login(request, user)
            return render(request, "register_done.html")
    
    context = {'form':form}
    return render(request, 'register.html', context)



def registration_done(request):
    return render(request, 'registration_done.html')


class LoginView(FormView):
    template_name="login.html"
    form_class = LoginForm

    def form_valid(self, form):
        data = form.cleaned_data 
        email = data["email"]
        password = data["password"]
        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect("index")
            else:
                return HttpResponse("Ваш аккаунт не активен")
        return HttpResponse("Такого пользователя не существует или данные неверны")
    

      
@login_required(login_url='login')
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")



@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            messages.success(request, 'Ваш пароль успешно изменен!')
            return redirect('profile')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})



class UserUpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "edit_profile.html"
    queryset = User.objects.all()
    form_class=UserUpdateForm
    success_url = reverse_lazy("profile")


    def get_object(self):
        return self.request.user


def get_user_profile(request):
    context = {
        "user": request.user
      
    }
    return render(request, "profile_data.html", context)



def doctors(request):
    doctors=Doctor.objects.all()
    quantity=doctors.count()
    about=About.objects.get(page="doctors")

    context = {
        'doctors': doctors,
        'quantity': quantity,
        'about': about,
    }

    return render(request, 'doctors.html', context)



def get_doctor(request, pk):
    user = User.objects.get(id=pk)
    doctor = user.doctor
 
    if request.method == 'POST':
        form = SpecialistAppointmentForm(request.POST)
        
        if form.is_valid():
            chosen_day = form.cleaned_data['day']
            chosen_time = form.cleaned_data["time"]
            day_of_week = chosen_day.weekday()

            ave = DoctorAvailability.objects.get(
                doctor=doctor
            )

            days = [day.number for day in ave.days.all()]
            if chosen_day <= datetime.today().date():
                form.add_error('day', 'Выберите будущую дату и время.')
            elif day_of_week not in days:
                form.add_error('day', 'Врач не работает в выбранный день.')
            elif doctor.user == request.user:
                form.add_error(None, 'Вы не можете записаться на прием к себе.')
            else:
                start_time = datetime.combine(chosen_day, ave.start_time)
                end_time = datetime.combine(chosen_day, ave.end_time)
                appointments = Appointment.objects.filter(doctor=doctor, day=chosen_day, time=chosen_time)
                if not start_time.time() <= chosen_time  or chosen_time >= end_time.time():
                    form.add_error('time', 'Время не входит в доступные часы врача.')
                elif len(appointments):
                    form.add_error('time', 'Это время уже занято.')
                else:
                    appointment = form.save(commit=False)
                    appointment.doctor = doctor
                    patient, created = Patient.objects.get_or_create(user=request.user)
                    appointment.patient = patient.user
                    appointment.save()
                    messages.success(request, 'Ваша запись успешно проведена.')
                    return redirect(reverse_lazy("doctor_template", kwargs={"pk": doctor.user.id}))
        else:
            form.errors
    else:
        form = SpecialistAppointmentForm()

    user = get_object_or_404(User, pk=pk)
    try:
        doctor = Doctor.objects.get(user=user)
    except Doctor.DoesNotExist:
        return HttpResponse("Пользователь не является врачом")
    doctor_availability = doctor.doctoravailability_set.all()
    available_times = []

    for availability in doctor_availability:
        for day in availability.days.all():
            available_times.append({
                'day': day.get_name_display(),
                'start_time': availability.start_time,
                'end_time': availability.end_time,
            })

    else:
        context = {
            "user": user,
            "doctor": doctor,
            "available_times":available_times,
            'form':form,
        }
        
        return render(request, 'doctor_template.html', context)



@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            chosen_day = form.cleaned_data['day']
            chosen_time = form.cleaned_data["time"]
            selected_doctor = form.cleaned_data['doctor']
            day_of_week = chosen_day.weekday()

           
            ave = DoctorAvailability.objects.get(doctor=selected_doctor)
            days = [day.number for day in ave.days.all()]

            if chosen_day <= datetime.today().date():
                form.add_error('day', 'Выберите будущую дату и время.')
            elif day_of_week not in days:
                form.add_error('day', 'Врач не работает в выбранный день.')
            elif selected_doctor.user == request.user:
                form.add_error(None, 'Вы не можете записаться на прием к себе.')
            else:
                start_time = datetime.combine(chosen_day, ave.start_time)
                end_time = datetime.combine(chosen_day, ave.end_time)

                appointments = Appointment.objects.filter(doctor=selected_doctor, day=chosen_day, time=chosen_time)
                if not start_time.time() <= chosen_time <= end_time.time():
                    form.add_error('time', 'Время не входит в доступные часы врача.')
                elif len(appointments):
                    form.add_error('time', 'Это время уже занято.')
                else:
                    appointment = form.save(commit=False)
                    appointment.doctor = selected_doctor
                    patient = Patient.objects.get_or_create(user=request.user)
                    appointment.patient = patient.user
                    appointment.save()
                    return redirect('book_appointment')
        else:
            form.errors
    else:
        form = AppointmentForm()
    
    doctors=Doctor.objects.all()

    return render(request, 'book_appointment.html', {'form': form, 'doctors':doctors})




@login_required(login_url='login')
def add_doctor_availability(request):
    try:
        doctor = request.user.doctor 
    except ObjectDoesNotExist:
        return HttpResponse("Вы не являетесь врачом.")

    appointments = []
    if doctor:
        # Получение записи пациентов для врача
        appointments = Appointment.objects.filter(doctor=doctor)

    return render(request, 'doctor_plan.html', {"appointments": appointments})




@login_required(login_url='login')
def view_doctor_availability(request, doctor_id):
    doctor = Doctor.objects.get(pk=doctor_id)
    available_times = []
    doctor_availability = doctor.doctoravailability_set.all()
    
    for availability in doctor_availability:
        for day in availability.days.all():
            available_times.append({
                'day': day.get_name_display(),
                'start_time': availability.start_time,
                'end_time': availability.end_time,
            })
    
    return render(request, 'view_doctor_availability.html', {'available_slots': available_times})



def create_hourly_slots(start_time, end_time):
    current_time = datetime.combine(datetime.today(), start_time)
    end_datetime = datetime.combine(datetime.today(), end_time)
    hourly_slots = []

    while current_time < end_datetime:
        hourly_slots.append(current_time.strftime('%H:%M'))
        current_time += timedelta(hours=1)

    return hourly_slots



@login_required(login_url='login')
def get_available_time_slot(request):
    data = json.loads(request.body.decode('utf-8'))
    date = data["date"]
    user_id = data["user_id"]

    user = User.objects.get(pk=user_id)
    doctor = user.doctor

    day =  datetime.strptime(date, "%Y-%m-%d").date()
    week_day = day.weekday()
    da = DoctorAvailability.objects.get(doctor=doctor)
    days = [day.number for day in da.days.all()]
    if week_day not in days:
        return JsonResponse(data={"slots":[]})
    

    booked_appointments = Appointment.objects.filter(doctor=doctor, day=day) 
    hourly_slots = create_hourly_slots(da.start_time,da.end_time) 
    available_slots = [slot for slot in hourly_slots if slot not in [appointment.time.strftime('%H:%M') for appointment in booked_appointments]]
    return JsonResponse(data={"slots": available_slots})



@login_required(login_url='login')
def available_slots_of_doctors(request):
    data = json.loads(request.body.decode('utf-8'))
    date = data["date"]
    user_id = data["user_id"]
    user = User.objects.get(pk=user_id)
    doctor = user.doctor

    day =  datetime.strptime(date, "%Y-%m-%d").date()
    week_day = day.weekday()
    da = DoctorAvailability.objects.get(doctor=doctor)
    days = [day.number for day in da.days.all()]
    if week_day not in days:
        return JsonResponse(data={"slots":[]})
    

    booked_appointments = Appointment.objects.filter(doctor=doctor, day=day) 
    hourly_slots = create_hourly_slots(da.start_time,da.end_time) 
    available_slots = [slot for slot in hourly_slots if slot not in [appointment.time.strftime('%H:%M') for appointment in booked_appointments]]
    return JsonResponse(data={"slots": available_slots})


@login_required(login_url='login')
def create_medical_record(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id)
    existing_record = MedicalRecord.objects.filter(appointment=appointment).first()

    if existing_record:
        messages.error(request, 'Запись уже существует для этого приема.')
        return redirect('doctor_plan')

    if request.method == 'POST':
        form = MedicalRecordForm(request.POST, request.FILES)
        if form.is_valid():
            medical_record = MedicalRecord(appointment=appointment)
            medical_record.medical_history = form.cleaned_data['medical_history']
            medical_record.uploaded_file = form.cleaned_data['uploaded_file']
            medical_record.save()
            messages.success(request, 'Запись истории болезни успешно создана.')
            return redirect('doctor_plan') 
    else:  
        form = MedicalRecordForm() 

    return render(request, 'create_medical_record.html', {'form': form, 'appointment': appointment})


@login_required(login_url='login')
def view_records_list(request):
    medical_records = MedicalRecord.objects.select_related('appointment__patient', 'appointment__doctor').filter(appointment__doctor=request.user.doctor)
    return render(request, 'view_records_list.html', {'medical_records': medical_records})



@login_required(login_url='login')
def patient_records(request):
    user = request.user  
    appointments = Appointment.objects.filter(patient=user)  
    medical_records = MedicalRecord.objects.filter(appointment__in=appointments) 

    context = {
        'appointments': appointments,
        'medical_records': medical_records,
    }

    return render(request, 'patient_records.html', context)