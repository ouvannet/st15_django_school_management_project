# project_1/routes/web.py

from django.urls import path
from project_1.controllers import student_controller
from project_1.controllers.student_controller import ListStudent,AddStudent,EditStudent,DeleteStudent

urlpatterns = [
    path('student/', student_controller.index, name='student'),
    path('student/list', ListStudent.as_view(), name='student/list'),
    path('student/add', AddStudent.as_view(), name='student/add'),
    path('student/edit', EditStudent.as_view(), name='student/edit'),
    path('student/delete', DeleteStudent.as_view(), name='student/delete'),
]
