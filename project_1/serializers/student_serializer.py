# project_1/serializers/customer_serializer.py
from rest_framework import serializers
from project_1.models.student import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'address', 'salary', 'photo','created_at','created_by','updated_at','updated_by']
