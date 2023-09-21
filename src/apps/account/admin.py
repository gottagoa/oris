from django.contrib import admin
from django import forms
from django.utils.formats import date_format
from django.forms import SelectDateWidget
from src.apps.account.models import User, Doctor, Patient, Day, DoctorAvailability, Appointment, MedicalRecord
from .forms import  AppointmentForm
from django.utils.timezone import activate
from django.utils import timezone


class UserAdminUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        exclude = ["password", "date_joined", "groups", "user_permissions", "last_login"]

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    form = UserAdminUpdateForm
    list_display = ["first_name", "last_name", "email"]

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    def __str__(self):
        return self.user.full_name


@admin.register(Day)
class  DayAdmin(admin.ModelAdmin):
    list_display = ["get_name_display"]


@admin.register(Doctor)
class DoctorProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ["category"]
    def __str__(self):
        return self.user.full_name



@admin.register(DoctorAvailability)
class DoctorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'display_days', 'start_time', 'end_time']
    filter_horizontal = ["days"]
    
    def display_days(self, obj):
        return ", ".join([day.get_name_display() for day in obj.days.all()])
    
    display_days.short_description = 'Дни доступности'



@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'patient', 'day', 'time', 'is_booked']
    list_filter = ['doctor', 'is_booked']
    actions = ['mark_as_booked']
    form = AppointmentForm

    def changelist_view(self, request, extra_context=None):
        activate('Asia/Bishkek')  
        return super().changelist_view(request, extra_context=extra_context)

    def mark_as_booked(self, request, queryset):
        queryset.update(is_booked=True)
    mark_as_booked.short_description = 'Отметить как забронированные'



admin.site.register(MedicalRecord)


