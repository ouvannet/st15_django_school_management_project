from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project_1.serializers.customer_serializer import CustomerSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.shortcuts import render,get_object_or_404
from project_1.models.customer import Customer
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'pages/customer/index.html')
class listCustomer(APIView):
    def get(self, request):
        customers = list(Customer.objects.values())
        return Response({'customers': customers}, status=status.HTTP_200_OK)
# Add customer (POST)
class CustomerAdd(APIView):
    @swagger_auto_schema(request_body=CustomerSerializer, responses={201: CustomerSerializer})
    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            customer=serializer.save()
            return Response(CustomerSerializer(customer).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Edit customer (PUT)

class EditCustomer(APIView):
    @swagger_auto_schema(request_body=CustomerSerializer, responses={200: CustomerSerializer})
    def put(self, request):
        id = request.data.get('id')
        if not id:
            return Response({"error": "ID is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)
        customer=get_object_or_404(Customer, id=id)
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            customer=serializer.save()
            return Response(CustomerSerializer(customer).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Delete customer (DELETE)
class DeleteCustomer(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER)},
            required=['id']
        ),
        responses={200: 'Customer deleted', 400: 'Invalid input', 404: 'Customer not found'}
    )
    def delete(self, request):
        id = request.data.get('id')
        if not id:
            return Response({"error": "ID is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch customer or return 404
        customer = get_object_or_404(Customer, id=id)
        
        # Delete customer
        customer.delete()
        return Response({"message": "Customer deleted successfully"}, status=status.HTTP_200_OK)