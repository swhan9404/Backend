from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from django.shortcuts import render
from django.db.models import Count
from .models import VisitOccurrence
from concept.models import Concept

from django.db import connection
from datetime import datetime

# Create your views here.
@api_view(['get'])
def total(request) : # foreign key 가 아니라서 ORM 상에서 JOIN 이 안됨;;
    data = VisitOccurrence.objects.values('visit_concept_id').annotate(Count('visit_concept_id'))

    for tmp in data : # JOIN 안해서 생긴 불필요한 반복문(N+1 문제)
        concept_id = tmp['visit_concept_id']
        concept_name = Concept.objects.filter(concept_id=concept_id).values('concept_name')
        tmp['concept_name'] = concept_name[0]['concept_name']

    return Response(data)

@api_view(['get'])
def gender(request) : # ORM 으로는 이제 불가능한 영역이라 raw sql문으로 처리
    cursor= connection.cursor()
    sql = """
    SELECT p.gender_source_value, COUNT(p.gender_source_value) as cnt
    FROM visit_occurrence as v
    LEFT OUTER JOIN person as p
    ON v.person_id = p.person_id
    GROUP BY p.gender_source_value;
    """
    cursor.execute(sql)
    row = cursor.fetchall()

    data = []
    for tmp in row :
        row_data = {}
        row_data["gender"] = tmp[0]
        row_data["cnt"] = tmp[1]
        data.append(row_data)

    return Response(data)

@api_view(['get'])
def race(request) : # ORM 으로는 이제 불가능한 영역이라 raw sql문으로 처리
    cursor= connection.cursor()
    sql = """
    SELECT p.race_source_value, COUNT(p.race_source_value) as cnt
    FROM visit_occurrence as v
    LEFT OUTER JOIN person as p
    ON v.person_id = p.person_id
    GROUP BY p.race_source_value;
    """
    cursor.execute(sql)
    row = cursor.fetchall()

    data = []
    for tmp in row :
        row_data = {}
        row_data["race"] = tmp[0]
        row_data["cnt"] = tmp[1]
        data.append(row_data)

    return Response(data)

@api_view(['get'])
def ethnicity(request) : # ORM 으로는 이제 불가능한 영역이라 raw sql문으로 처리
    cursor= connection.cursor()
    sql = """
    SELECT p.ethnicity_source_value, COUNT(p.ethnicity_source_value) as cnt
    FROM visit_occurrence as v
    LEFT OUTER JOIN person as p
    ON v.person_id = p.person_id
    GROUP BY p.ethnicity_source_value;
    """
    cursor.execute(sql)
    row = cursor.fetchall()

    data = []
    for tmp in row :
        row_data = {}
        row_data["ethnicity"] = tmp[0]
        row_data["cnt"] = tmp[1]
        data.append(row_data)

    return Response(data)

@api_view(['get'])
def age(request) : # ORM 으로는 이제 불가능한 영역이라 raw sql문으로 처리
    cursor= connection.cursor()
    sql = """
    SELECT b.birth, COUNT(b.birth) as cnt
    FROM visit_occurrence as v
    LEFT OUTER JOIN (
        SELECT person_id, ((2021 - person.year_of_birth)/10) as birth
        FROM person
    ) as b
    ON b.person_id = v.person_id
    GROUP BY b.birth
    ORDER BY b.birth;
    """
    # parameter_data  = {
    #     "year" : datetime.today().year
    # }
    cursor.execute(sql)
    row = cursor.fetchall()

    data = []
    for tmp in row :
        row_data = {}
        row_data["birth"] = f"{tmp[0]}0 ~ {tmp[0]}9"
        row_data["cnt"] = tmp[1]
        data.append(row_data)

    return Response(data)

