# project_1/routes/web.py

from django.urls import path
from project_1.controllers import staff_controller

urlpatterns = [
    path('staff/', staff_controller.index, name='staff'),
    path('staff/list', staff_controller.list_staff),
    path('staff/add', staff_controller.add_staff, name='staff/add'),
    path('staff/edit', staff_controller.edit_staff, name='staff/edit'),
    path('staff/delete', staff_controller.delete_staff, name='staff/delete'),
]
