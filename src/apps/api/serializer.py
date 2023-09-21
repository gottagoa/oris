

from src.apps.account.models import User, Doctor

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta: 
        model = Doctor
        fields = "__all__"


class AppointmentSerializer(serializers.Serializer):
    date = serializers.DateField(format="%Y-%m-%d")
    time = serializers.CharField()
    doctor_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    
