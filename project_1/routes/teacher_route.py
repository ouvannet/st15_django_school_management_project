# project_1/routes/web.py

from django.urls import path
from project_1.controllers import teacher_controller
from project_1.controllers.teacher_controller import ListTeacher,AddTeacher,EditTeacher,DeleteTeacher

urlpatterns = [
    path('teacher/', teacher_controller.index, name='teacher'),
    path('teacher/list', ListTeacher.as_view(), name='teacher/list'),
    path('teacher/add', AddTeacher.as_view(), name='teacher/add'),
    path('teacher/edit', EditTeacher.as_view(), name='teacher/edit'),
    path('teacher/delete', DeleteTeacher.as_view(), name='teacher/delete'),
]
