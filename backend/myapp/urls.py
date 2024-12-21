from django.contrib import admin  # Import the admin module
from django.urls import path
from django.http import JsonResponse
from .views import compile_code  # Import your `compile_code` view

urlpatterns = [
    # Welcome message for the root endpoint
    path('', lambda request: JsonResponse({'message': 'Welcome to my online compiler! :)'})),

    # Admin interface
    path('admin/', admin.site.urls),

    # API endpoint for compile requests
    path('api/compile/', compile_code, name='compile_code'),
]
