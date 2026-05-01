from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static

# Import your custom route modules
from project_1.routes import (
    home_route,
    user_route,
    customer_route,
    supplier_route,
    position_route,
    staff_route,
    subject_route,
    teacher_route,
    student_route,
    cache_route
)

# Swagger imports
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Project 1 API",
        default_version="v1",
        description="API documentation for Project 1",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@example.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),

    # Your routes
    path('', include(home_route)),
    path('', include(user_route)),
    path('', include(customer_route)),
    path('', include(supplier_route)),
    path('', include(position_route)),
    path('', include(staff_route)),
    path('', include(subject_route)),
    path('', include(teacher_route)),
    path('', include(student_route)),
    path('', include(cache_route)),

    # Swagger routes
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
