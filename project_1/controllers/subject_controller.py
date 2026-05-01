from psycopg import logger
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from project_1.serializers.subject_serializer import SubjectSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.shortcuts import render,get_object_or_404
from project_1.models.subject import Subject
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'pages/subject/index.html')

class listSubject(APIView):
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
        # Extract DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        search_value = request.GET.get('search[value]', '')
        order_column_idx = int(request.GET.get('order[0][column]', 0))
        order_dir = request.GET.get('order[0][dir]', 'asc')

        # Get all fields from Subject model for dynamic column mapping
        fields = [field.name for field in Subject._meta.fields]
        order_column = request.GET.get(f'columns[{order_column_idx}][data]', fields[0])

        # Validate order_column
        if order_column not in fields:
            order_column = fields[0]  # Fallback to first field

        # Build the queryset
        queryset = Subject.objects.all()

        # Apply search (filtering)
        if search_value:
            # Example: filter on subject_name (adjust based on your Subject model fields)
            queryset = queryset.filter(subject_name__icontains=search_value)

        # Get total records
        records_total = queryset.count()

        # Apply sorting
        if order_dir == 'desc':
            order_column = f'-{order_column}'
        queryset = queryset.order_by(order_column)

        # Apply pagination
        records_filtered = queryset.count()
        queryset = queryset[start:start + length]

        # Get data
        data = list(queryset.values())

        # Log request details for debugging
        logger.info(f"DataTables request: draw={draw}, start={start}, length={length}, search={search_value}, order={order_column}, dir={order_dir}")
        logger.info(f"Returning {len(data)} records")

        # Construct DataTables response
        response = {
            'draw': draw,
            'recordsTotal': records_total,
            'recordsFiltered': records_filtered,
            'data': data
        }

        return Response(response, status=status.HTTP_200_OK)
class SubjectAdd(APIView):
    @swagger_auto_schema(request_body=SubjectSerializer, responses={201: SubjectSerializer})
    def post(self, request):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            subject=serializer.save()
            return Response(SubjectSerializer(subject).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# # Edit Subject (PUT)
class EditSubject(APIView):
    @swagger_auto_schema(request_body=SubjectSerializer, responses={200: SubjectSerializer})
    def put(self, request):
        id = request.data.get('id')
        if not id:
            return Response({"error": "ID is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)
        subject=get_object_or_404(Subject, id=id)
        serializer = SubjectSerializer(subject, data=request.data, partial=True)
        if serializer.is_valid():
            subject=serializer.save()
            return Response(SubjectSerializer(subject).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # Delete subject (DELETE)
class DeleteSubject(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={'id': openapi.Schema(type=openapi.TYPE_INTEGER)},
            required=['id']
        ),
        responses={200: 'Subject deleted', 400: 'Invalid input', 404: 'Subject not found'}
    )
    def delete(self, request):
        id = request.data.get('id')
        if not id:
            return Response({"error": "ID is required in the request body"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Fetch subject or return 404
        subject = get_object_or_404(Subject, id=id)
        
        # Delete subject
        subject.delete()
        return Response({"message": "subject deleted successfully"}, status=status.HTTP_200_OK)