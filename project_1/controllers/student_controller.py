import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project_1.serializers.student_serializer import StudentSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.shortcuts import render,get_object_or_404
from project_1.models.student import Student
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

from django.db.models import Q
from django.core.exceptions import FieldError

def index(request):
    return render(request, 'pages/student/index.html')

class ListStudent(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('draw', openapi.IN_QUERY, description="Draw counter", type=openapi.TYPE_INTEGER),
            openapi.Parameter('start', openapi.IN_QUERY, description="Start index for pagination", type=openapi.TYPE_INTEGER),
            openapi.Parameter('length', openapi.IN_QUERY, description="Number of records per page", type=openapi.TYPE_INTEGER),
            openapi.Parameter('search[value]', openapi.IN_QUERY, description="Search term", type=openapi.TYPE_STRING),
            openapi.Parameter('order[0][column]', openapi.IN_QUERY, description="Column index to sort", type=openapi.TYPE_INTEGER),
            openapi.Parameter('order[0][dir]', openapi.IN_QUERY, description="Sort direction (asc/desc)", type=openapi.TYPE_STRING),
        ],
        responses={200: openapi.Schema(type=openapi.TYPE_OBJECT, properties={
            'draw': openapi.Schema(type=openapi.TYPE_INTEGER),
            'recordsTotal': openapi.Schema(type=openapi.TYPE_INTEGER),
            'recordsFiltered': openapi.Schema(type=openapi.TYPE_INTEGER),
            'data': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_OBJECT))
        })}
    )
    def get(self, request):
        # Log request parameters for debugging
        print('Request parameters:', request.GET)

        # Extract DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        order_column_idx = int(request.GET.get('order[0][column]', 0))
        order_dir = request.GET.get('order[0][dir]', 'asc')

        # Map DataTables column index to model field
        column_mapping = {
            0: 'id',
            1: 'first_name',  # Combined with last_name in frontend
            2: 'gender',
            3: 'date_of_birth',
            4: 'salary',
            5: 'photo',
            6: None  # Action column (no sorting)
        }
        order_column = column_mapping.get(order_column_idx, 'id')
        order_prefix = '' if order_dir == 'asc' else '-'

        # Get base queryset
        queryset = Student.objects.all()

        # Get total records (before filtering)
        records_total = queryset.count()

        # Apply search filter
        if search_value:
            queryset = queryset.filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(gender__icontains=search_value) |
                Q(address__icontains=search_value) |
                Q(salary__icontains=search_value)
            )

        # Get filtered records count
        records_filtered = queryset.count()

        # Apply sorting (skip for action column)
        if order_column:
            try:
                queryset = queryset.order_by(f"{order_prefix}{order_column}")
            except FieldError:
                queryset = queryset.order_by('id')  # Fallback to default sorting

        # Apply pagination
        queryset = queryset[start:start + length]

        # Serialize data
        serializer = StudentSerializer(queryset, many=True)

        # Log response data for debugging
        print('Response data:', {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': serializer.data
        })

        # Prepare response
        return Response({
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
class AddStudent(APIView):
    @swagger_auto_schema(request_body=StudentSerializer,responses={201:StudentSerializer})
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            student = serializer.save()
            return Response(
                {"message": "Student added", "id": student.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EditStudent(APIView):
    @swagger_auto_schema(request_body=StudentSerializer, responses={200: StudentSerializer})
    def post(self, request):
        student_id = request.data.get('id')
        if not id:
            return Response({"error": "ID is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)
            
        student = get_object_or_404(Student, id=student_id)

        student.first_name = request.data.get('first_name', student.first_name)
        student.last_name = request.data.get('last_name', student.last_name)
        student.gender = request.data.get('gender', student.gender)
        student.date_of_birth = request.data.get('date_of_birth', student.date_of_birth)
        student.salary = request.data.get('salary', student.salary)

        # Handle photo replacement
        photo = request.FILES.get('photo')
        if photo:
            if student.photo and student.photo.name:
                old_photo_path = os.path.join(settings.MEDIA_ROOT, student.photo.name)
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
            student.photo = photo

        student.save()

        return JsonResponse({'message': 'Student updated', 'id': student.id}, status=status.HTTP_200_OK)
class DeleteStudent(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER)},
            required=['id']
        ),
        responses={200: 'Subject deleted', 400: 'Invalid input', 404: 'Subject not found'}
    )
    def delete(self, request):
        student_id = request.data.get('id')
        if not student_id:
            return Response(
                {"error": "ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        student = get_object_or_404(Student, id=student_id)

        # Handle photo deletion
        if student.photo and student.photo.name:
            photo_path = os.path.join(settings.MEDIA_ROOT, student.photo.name)
            if os.path.exists(photo_path):
                os.remove(photo_path)

        student.delete()
        return Response(
            {"message": "Student deleted"},
            status=status.HTTP_200_OK
        )