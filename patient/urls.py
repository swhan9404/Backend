from django.urls import path
from . import views

app_name = 'patient'

urlpatterns = [
    path('', views.total),
    path('gender', views.gender),
    path('race', views.race),
    path('ethnicity', views.ethnicity),
    path('death', views.death)
]
