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
    """
    SELECT COUNT("person"."person_id") AS "total"
    FROM "person"
    """
    patient_total = Person.objects.values('person_id').aggregate(total=Count('person_id'))
    return Response(patient_total)

@api_view(['get'])
def gender(request) :
    # group by
    """
    SELECT "person"."gender_source_value",
       COUNT("person"."gender_source_value") AS "gender_source_value__count"
    FROM "person"
    GROUP BY "person"."gender_source_value"
    """
    data = Person.objects.values('gender_source_value').annotate(Count('gender_source_value'))

    return Response(data)

@api_view(['get'])
def race(request) :
    """
    SELECT "person"."race_source_value",
       COUNT("person"."race_source_value") AS "race_source_value__count"
    FROM "person"
    GROUP BY "person"."race_source_value"
    """
    data = Person.objects.values('race_source_value').annotate(Count('race_source_value'))
    return Response(data)

@api_view(['get'])
def ethnicity(request) :
    """
    SELECT "person"."ethnicity_source_value",
       COUNT("person"."ethnicity_source_value") AS "ethnicity_source_value__count"
    FROM "person"
    GROUP BY "person"."ethnicity_source_value"
    """
    data = Person.objects.values('ethnicity_source_value').annotate(Count('ethnicity_source_value'))
    return Response(data)

@api_view(['get'])
def death(request) :
    """
    SELECT COUNT("death"."person_id") AS "death_total"
    FROM "death"
    """
    data = Death.objects.values('person_id').aggregate(death_total=Count('person_id'))
    return Response(data)