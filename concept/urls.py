from django.urls import path
from . import views

app_name = 'concept'

urlpatterns = [
    path('concept', views.concept),
    path('condition', views.condition_occurence),

]
