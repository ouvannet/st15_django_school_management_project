# project_1/serializers/customer_serializer.py
from rest_framework import serializers
from project_1.models.subject import Subject

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'subject_name']
