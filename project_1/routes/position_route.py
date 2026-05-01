# project_1/routes/web.py

from django.urls import path
from project_1.controllers import position_controller

urlpatterns = [
    path('position/', position_controller.index, name='position'),
    path('position/list', position_controller.list_position),
    path('position/add', position_controller.add_position, name='position/add'),
    path('position/edit', position_controller.edit_position, name='position/edit'),
    path('position/delete', position_controller.delete_position, name='position/delete'),
]
