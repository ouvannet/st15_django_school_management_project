# project_1/serializers/customer_serializer.py
from rest_framework import serializers
from project_1.models.customer import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'age', 'phone_number']
