import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
import json
from django.conf import settings
from upstash_redis import Redis
import time

class getCache(APIView):
    def get(self, request):
            redis = Redis(url="https://meet-goldfish-14149.upstash.io", token="ATdFAAIncDExMTNjZGQ2MzkzNjI0ODA1YWE2NzY1ZDJmYTc1YmJmZHAxMTQxNDk")

            value = redis.get("list")
            if value:
                return Response(
                    value,
                    status=status.HTTP_200_OK
                )
            time.sleep(2)
            list={ "key": "user:1","value": "John Doe" }
            redis.set("list", list)
            return Response(
                list,
                status=status.HTTP_200_OK
            )
