# project_1/routes/web.py

from django.urls import path
from project_1.controllers.cache_controller import getCache

urlpatterns = [
    path('cache/get', getCache.as_view(), name='cache/get'),
]
