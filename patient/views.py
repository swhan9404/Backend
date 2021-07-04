from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.shortcuts import render
from django.db.models import Count
from .models import Person, Concept, Death

from .serializers import ConceptSerializer, PersonSerializer, DeathSerializer

# Create your views here.
@api_view(['get'])
def total(request) :
    patient_total = Person.objects.values('person_id').aggregate(total=Count('person_id'))
    return Response(patient_total)

@api_view(['get'])
def gender(request) :
    """
        {
        "person_id": 402435,
        "gender_concept_id": 8532,
        "year_of_birth": 1997,
        "month_of_birth": 4,
        "day_of_birth": 18,
        "birth_datetime": "1997-04-18T00:00:00+09:00",
        "race_concept_id": 8527,
        "ethnicity_concept_id": 0,
        "location_id": null,
        "provider_id": null,
        "care_site_id": null,
        "person_source_value": "a434e3bf-7720-4612-8d18-e274e199f4fd",
        "gender_source_value": "F",
        "gender_source_concept_id": 0,
        "race_source_value": "white",
        "race_source_concept_id": 0,
        "ethnicity_source_value": "hispanic",
        "ethnicity_source_concept_id": 0
    },
    """
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