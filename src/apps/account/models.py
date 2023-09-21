from django.db import models
from django.contrib.auth.models import AbstractUser
from src.apps.post.models import Category
from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):

    GENDER_CHOICES = [
    ('M', 'Мужской'),
    ('F', 'Женский'),
    ]
    
    username=None
    email = models.EmailField("Email", unique=True)
    avatar = models.ImageField(
        "Аватар",
          upload_to="user/images/", 
          null=True,blank=True,
        #   default=""
          )
    birthday=models.DateField("Дата рождения",null=True,blank=True)
    mobile = models.CharField("Номер телефона", max_length=30, null=True,blank=True)
    gender = models.CharField("Пол", max_length=10, choices=GENDER_CHOICES, null=True, blank=True)
    is_active = models.BooleanField("Активный аккаунт", default=True)
    is_staff = models.BooleanField("Пользователь не является специалистом", default=False)
    date_joined=models.DateTimeField("Дата регистрации", auto_now_add=True)
    
    objects = UserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
    
    def  __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    class Meta:
        verbose_name = "Пациент"
        verbose_name_plural = "Пациенты"
    
    def __str__(self):
        return self.user.full_name 



    

class Doctor(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
    qualification=models.TextField('Квалификация', null=True,blank=True)
    experience=models.TextField("Опыт работы", null=True,blank=True)
    education=models.TextField("Образование", null=True,blank=True)
    certifications=models.TextField('Сертификаты', null=True,blank=True)
    speciality=models.CharField('Специальность',max_length=200, null=True,blank=True)
    category = models.ManyToManyField(Category, related_name='doctors')

    class Meta:
        verbose_name = "Специалист"
        verbose_name_plural = "Специалисты"
        
    def __str__(self):
        return self.user.full_name 
    
    
    
class WeekDay(models.TextChoices):
    MONDAY = "monday", "Понедельник"
    TUESDAY = "tuesday", "Вторник"
    WEDNESDAY = "wednesday", "Среда"
    THURSDAY = "thursday", "Четверг"
    FRIDAY = "friday", "Пятница"
    SATURDAY = "saturday", "Суббота"
    SUNDAY = "sunday", "Воскресенье"

    @classmethod
    def days(cls):
        return (
            cls.MONDAY,
            cls.TUESDAY,
            cls.WEDNESDAY,
            cls.THURSDAY,
            cls.FRIDAY,
            cls.SATURDAY,
            cls.SUNDAY,
        )

class Day(models.Model):
    name = models.CharField(max_length=10, choices=WeekDay.choices)


    def __str__(self):
        return self.name
    
    @property
    def number(self):
        days: tuple = WeekDay.days()
        return days.index(self.name)

            
    

class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    days = models.ManyToManyField(Day)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Свободное время доктора {self.doctor}"


class Appointment(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    day = models.DateField(null=True)
    time = models.TimeField(null=True)
    is_booked = models.BooleanField(default=False)
     

class MedicalRecord(models.Model):
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    medical_history = models.TextField(blank=True, null=True)
    uploaded_file = models.FileField(upload_to='medical_records/', blank=True, null=True)

    def __str__(self):
        return f"Запись приема {self.appointment.id} - {self.appointment.patient}"

    class Meta:
        verbose_name = 'Медицинская запись'
        verbose_name_plural = 'Медицинские записи'
