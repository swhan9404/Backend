from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.shortcuts import render
from django.db.models import Count
from .models import Person, Death

from .serializers import PersonSerializer, DeathSerializer

# Create your views here.
@api_view(['get'])
def total(request) :
    patient_total = Person.objects.values('person_id').aggregate(total=Count('person_id'))
    return Response(patient_total)

@api_view(['get'])
def gender(request) :
    # group by
    data = Person.objects.values('gender_source_value').annotate(Count('gender_source_value'))

    return Response(data)

@api_view(['get'])
def race(request) :
    data = Person.objects.values('race_source_value').annotate(Count('race_source_value'))
    return Response(data)

@api_view(['get'])
def ethnicity(request) :
    data = Person.objects.values('ethnicity_source_value').annotate(Count('ethnicity_source_value'))
    return Response(data)

@api_view(['get'])
def death(request) :
    data = Death.objects.values('person_id').aggregate(death_total=Count('person_id'))
    return Response(data)