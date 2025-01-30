from rest_framework import serializers
from .models import CarLog,Boomsig

class CarLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarLog
        fields = '__all__'  # Include all fields from the CarLog model


class BoomsigSerializer(serializers.ModelSerializer):
    class Meta:
        model = Boomsig
        fields = '__all__'
