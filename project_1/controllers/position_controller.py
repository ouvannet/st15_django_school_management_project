from django.shortcuts import render,get_object_or_404
from project_1.models.position import Position
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json

def index(request):
    return render(request, 'pages/position/index.html')

def list_position(request):
    if request.method == 'GET':
        positions = list(Position.objects.values())
        return JsonResponse({'positions': positions}, status=200)
@csrf_exempt
def add_position(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)
        position = Position.objects.create(
            position_name=data.get('name')
        )
        return JsonResponse({'message': 'Position added', 'id': position.id}, status=201)

# Edit position (PUT)
@csrf_exempt
def edit_position(request):
    if request.method == 'PUT':
        data = json.loads(request.body)
        id = data.get('id')
        # Ensure the position exists
        position = get_object_or_404(Position, id=id)
        position.position_name = data.get('name')
        position.save()
        return JsonResponse({'message': 'Position updated'}, status=200)

# Delete position (DELETE)
@csrf_exempt
def delete_position(request):
    if request.method == 'DELETE':
        data = json.loads(request.body)
        id = data.get('id')
        position = get_object_or_404(Position, id=id)
        position.delete()
        return JsonResponse({'message': 'Position deleted'}, status=200)