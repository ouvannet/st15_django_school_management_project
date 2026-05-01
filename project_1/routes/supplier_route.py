# project_1/routes/web.py

from django.urls import path
from project_1.controllers import supplier_controller

urlpatterns = [
    path('supplier/', supplier_controller.index, name='supplier'),
]
