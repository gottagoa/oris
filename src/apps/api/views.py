from django.shortcuts import render
from src.apps.account.models import Category, Doctor, Appointment, User, DoctorAvailability
from .serializer import DoctorSerializer, AppointmentSerializer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework import status
import json
# def get_doctors(request, slug):
#     category = Category.objects.get(slug=slug)
#     doctors = Doctor.objects.filter(category=category)
#     serializer = DoctorSerializer(doctors, many=True)
#     print(serializer.data)  # Обратите внимание на `many=True` для queryset
#     return Response(data=serializer.data)


class DoctorsListAPIView(ListAPIView):
    serializer_class = DoctorSerializer


    def get_queryset(self):
        slug = self.kwargs.get("slug")
        category = Category.objects.get(slug=slug)
        doctors = Doctor.objects.filter(category=category)
        return doctors
    

# def create_appointment(request):
#     data = json.loads(request.body.decode('utf-8'))
#     AppointmentSerializer(instance=data)
#     print(request.POST)
#     return Response(data={"message": "Success"}, status=200, safe=False)

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse


def create_appointment(request, *args, **kwargs):

    data = json.loads(request.body.decode('utf-8'))

    serializer = AppointmentSerializer(data=data)

    if serializer.is_valid():
        print(serializer)

        doctor_id = serializer.validated_data['doctor_id']
        date = serializer.validated_data['date']
        time = serializer.validated_data['time']
        user_id = serializer.validated_data["user_id"]

        doctor = Doctor.objects.get(user__id=doctor_id)
        user = User.objects.get(id=user_id)
        if doctor.user == user:
            return JsonResponse({"message":"Нельзя записаться к себе на прием!"},status=status.HTTP_403_FORBIDDEN)


        Appointment.objects.create(
            doctor=doctor,
            day=date,
            time=time,
            patient=user
        )
        return JsonResponse({"message": "Запись успешно создана"}, status=status.HTTP_201_CREATED)
  
    else:
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def get_doctor_availibity(request, pk):
    doctor = Doctor.objects.get(user__id=pk)
    availibity = DoctorAvailability.objects.get(doctor=doctor)
    print(availibity)
    
    data = {
        "day":[day.get_name_display() for day in availibity.days.all()],
        "start_time": availibity.start_time,
        "end_time": availibity.end_time
    }
    return JsonResponse(data=data, status=status.HTTP_200_OK)
