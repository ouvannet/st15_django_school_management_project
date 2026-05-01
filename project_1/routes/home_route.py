# project_1/routes/web.py

from django.urls import path
from project_1.controllers import home_controller

urlpatterns = [
    path('', home_controller.index, name='home'),
]
