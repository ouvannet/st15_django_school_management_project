# project_1/routes/web.py

from django.urls import path
from project_1.controllers import subject_controller
from project_1.controllers.subject_controller import listSubject,SubjectAdd,EditSubject,DeleteSubject


urlpatterns = [
    path('subject/', subject_controller.index, name='subject'),
    path('subject/list', listSubject.as_view(), name='submect/list'),
    path('subject/add', SubjectAdd.as_view(), name='subject/add'),
    path('subject/edit', EditSubject.as_view(), name='subject/edit'),
    path('subject/delete', DeleteSubject.as_view(), name='subject/delete'),
]
