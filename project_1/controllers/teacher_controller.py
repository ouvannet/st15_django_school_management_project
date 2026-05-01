import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project_1.serializers.teacher_serializer import TeacherSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.shortcuts import render,get_object_or_404
from project_1.models.teacher import Teacher
from project_1.models.subject import Subject
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings

from django.db.models import Q
from django.core.exceptions import FieldError

def index(request):
    subjects=list(Subject.objects.values())
    return render(request, 'pages/teacher/index.html',{'subjects':subjects})

class ListTeacher(APIView):
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
        print('Teacher request parameters:', request.GET)

        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        order_column_idx = int(request.GET.get('order[0][column]', 0))
        order_dir = request.GET.get('order[0][dir]', 'asc')

        column_mapping = {
            0: 'id',
            1: 'first_name',
            2: 'gender',
            3: 'date_of_birth',
            4: 'salary',
            5: 'photo',
            6: 'subject_id__subject_name',  # Updated to match model
            7: None
        }
        order_column = column_mapping.get(order_column_idx, 'id')
        order_prefix = '' if order_dir == 'asc' else '-'

        queryset = Teacher.objects.select_related('subject_id').all()
        records_total = queryset.count()

        if search_value:
            queryset = queryset.filter(
                Q(first_name__icontains=search_value) |
                Q(last_name__icontains=search_value) |
                Q(gender__icontains=search_value) |
                Q(salary__icontains=search_value) |
                Q(subject_id__subject_name__icontains=search_value, subject_id__isnull=False)
            )

        records_filtered = queryset.count()

        if order_column:
            try:
                queryset = queryset.order_by(f"{order_prefix}{order_column}")
            except FieldError:
                queryset = queryset.order_by('id')

        queryset = queryset[start:start + length]
        serializer = TeacherSerializer(queryset, many=True)

        print('Teacher response data:', {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': serializer.data
        })

        return Response({
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
class AddTeacher(APIView):
    @swagger_auto_schema(request_body=TeacherSerializer,responses={201:TeacherSerializer})
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            teacher = serializer.save()
            return Response(
                {"message": "Teacher added", "id": teacher.id},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class EditTeacher(APIView):
    @swagger_auto_schema(request_body=TeacherSerializer, responses={200: TeacherSerializer})
    def post(self, request):
        teacher_id = request.data.get('id')
        if not id:
            return Response({"error": "ID is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)
            
        teacher = get_object_or_404(Teacher, id=teacher_id)

        teacher.first_name = request.data.get('first_name', teacher.first_name)
        teacher.last_name = request.data.get('last_name', teacher.last_name)
        teacher.gender = request.data.get('gender', teacher.gender)
        teacher.date_of_birth = request.data.get('date_of_birth', teacher.date_of_birth)
        teacher.salary = request.data.get('salary', teacher.salary)

        subject_id = request.data.get('subject_id')
        # print('Subject ID:', subject_id)
        if subject_id:
            teacher.subject_id = get_object_or_404(Subject, id=subject_id)

        # Handle photo replacement
        photo = request.FILES.get('photo')
        if photo:
            if teacher.photo and teacher.photo.name:
                old_photo_path = os.path.join(settings.MEDIA_ROOT, teacher.photo.name)
                if os.path.exists(old_photo_path):
                    os.remove(old_photo_path)
            teacher.photo = photo

        teacher.save()

        return JsonResponse({'message': 'Teacher updated', 'id': teacher.id}, status=status.HTTP_200_OK)
class DeleteTeacher(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER)},
            required=['id']
        ),
        responses={200: 'Subject deleted', 400: 'Invalid input', 404: 'Subject not found'}
    )
    def delete(self, request):
        teacher_id = request.data.get('id')
        if not teacher_id:
            return Response(
                {"error": "ID is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        teacher = get_object_or_404(Teacher, id=teacher_id)

        # Handle photo deletion
        if teacher.photo and teacher.photo.name:
            photo_path = os.path.join(settings.MEDIA_ROOT, teacher.photo.name)
            if os.path.exists(photo_path):
                os.remove(photo_path)

        teacher.delete()
        return Response(
            {"message": "Teacher deleted"},
            status=status.HTTP_200_OK
        )