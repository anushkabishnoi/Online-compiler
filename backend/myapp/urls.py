from django.urls import path
from .views import compile_code

urlpatterns = [
    path('api/compile/', compile_code, name='compile_code')
]