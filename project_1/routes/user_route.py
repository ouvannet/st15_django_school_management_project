# project_1/routes/web.py

from django.urls import path
from project_1.controllers import user_controller

urlpatterns = [
    path('user/', user_controller.index, name='user'),
]
