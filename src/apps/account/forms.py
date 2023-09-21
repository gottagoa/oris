from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import SelectDateWidget
from src.apps.account.models import User, Day, DoctorAvailability, Appointment, Doctor
from src.apps.post.models import Category
from datetime import datetime
from django.core.exceptions import  ValidationError
import pytz
from django.forms import DateTimeInput, SelectDateWidget, TimeInput
from pytz import timezone


class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control"}),
        label="Email"
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"}),
        label="Пароль"
        )
    

class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())
    avatar = forms.ImageField(label='Аватар', required=False) 

    class Meta:
        model = User
        fields= [
                 
                 "email",
                 "first_name", 
                 "last_name",
                 "birthday",
                 "is_active",
                 "is_staff",
                 "mobile",
                 "gender",
                ]
        widgets = {
            "avatar": forms.FileInput(
                attrs={"class":"form-control"}
            ),
            
            "email": forms.EmailInput(
                attrs={"class":"form-control"}
            ), 
            "first_name": forms.TextInput(
                attrs={"class":"form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class":"form-control"}
            ),
            "birthday": forms.DateInput(
                attrs ={"class":"form-control", "type":"date"},
                format=("%Y-%m-%d")
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input",
                    "type":"checkbox"
                }
            ),

            "is_staff": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input",
                    "type":"checkbox"
                }
            ),

            "mobile": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),
            "gender":forms.Select(
                attrs={
                    "class":"form-control"
                }
            ),
        }

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            "avatar",
            "email",
            "first_name",
            "last_name",
            "birthday",
            "mobile",
            "gender",
           
            )
        widgets = {
            "avatar": forms.FileInput(
                attrs={"class":"form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class":"form-control"}
            ), 
            "first_name": forms.TextInput(
                attrs={"class":"form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class":"form-control"}
            ),
            "birthday": forms.DateInput(
                attrs ={"class":"form-control", "type":"date"},
                format=("%Y-%m-%d")
            ),

            "mobile": forms.TextInput(
                attrs={
                    "class":"form-control"
                }
            ),
            "gender":forms.Select(
                attrs={
                    "class":"form-control"
                }
            ),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['day', 'time', 'patient']

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        time = cleaned_data.get('time')

        if not self.is_valid_slot(day, time):
            self.add_error('time', 'Выбранное время недоступно.')

 

class SpecialistAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['day', 'time']
        widgets = {
            'day': forms.DateInput(attrs={'id': 'day',}),
            'time': forms.Select(attrs={'id': 'time'})
        }



class MedicalRecordForm(forms.Form):
    medical_history = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}))
    uploaded_file = forms.FileField()
