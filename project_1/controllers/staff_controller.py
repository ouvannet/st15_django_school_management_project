from django.shortcuts import render,get_object_or_404
from project_1.models.staff import Staff
from project_1.models.position import Position
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    # Fetch all positions to display in the staff page
    positions = Position.objects.all()
    return render(request, 'pages/staff/index.html', {'positions': positions})

def list_staff(request):
    if request.method == 'GET':
        staff = list(Staff.objects.select_related('position').values('position__position_name','position_id', 'id', 'last_name', 'first_name', 'gender', 'date_of_birth'))
        return JsonResponse({'staff': staff}, status=200)
@csrf_exempt
def add_staff(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        staff = Staff.objects.create(
            last_name=data.get('last_name'),
            first_name=data.get('first_name'),
            gender=data.get('gender'),
            date_of_birth=data.get('date_of_birth'),
            position_id=data.get('position')
        )
        return JsonResponse({'message': 'Staff added', 'id': staff.id}, status=201)

# Edit staff (PUT)
@csrf_exempt
def edit_staff(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        id = data.get('id')
        # Ensure the staff exists
        staff = get_object_or_404(Staff, id=id)
        # Update staff details
        staff.last_name = data.get('last_name', staff.last_name)
        staff.first_name = data.get('first_name', staff.first_name)
        staff.gender = data.get('gender', staff.gender)
        staff.date_of_birth = data.get('date_of_birth', staff.date_of_birth)
        staff.position_id = data.get('position_id', staff.position_id)

        staff.save()
        return JsonResponse({'message': 'Staff updated'}, status=200)

# Delete staff (DELETE)
@csrf_exempt
def delete_staff(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        staff = get_object_or_404(Staff, id=id)
        staff.delete()
        return JsonResponse({'message': 'Staff deleted'}, status=200)