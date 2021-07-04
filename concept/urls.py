from django.urls import path
from . import views

app_name = 'concept'

urlpatterns = [
    path('', views.search),
]
