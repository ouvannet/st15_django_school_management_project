# project_1/routes/web.py

from django.urls import path
from project_1.controllers import customer_controller
from project_1.controllers.customer_controller import listCustomer,CustomerAdd,EditCustomer,DeleteCustomer

urlpatterns = [
    path('customer/', customer_controller.index, name='customer'),
    path('customer/list', listCustomer.as_view(), name='customer/list'),
    path('customer/add', CustomerAdd.as_view(), name='customer/add'),
    path('customer/edit', EditCustomer.as_view(), name='customer/edit'),
    path('customer/delete', DeleteCustomer.as_view(), name='customer/delete'),
]
