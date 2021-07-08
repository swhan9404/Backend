from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Concept
from .serializers import ConceptSerializer
from django.core.paginator import Paginator

from django.db.models import Q
from django.db import connection
from django.db.models import Count

@api_view(['get'])
def concept(request) :
    """ 심각하게 오래걸림
    SELECT COUNT(*) AS "__count"
    FROM "concept"
    WHERE ("concept"."concept_name"::text LIKE '%%' OR "concept"."domain_id"::text LIKE '%%' OR "concept"."concept_class_id"::text LIKE '%%')
    """
    # search/concept/?keyword=&page=
    keyword = request.GET.get('keyword', '')
    page= int(request.GET.get('page', 1))
    
    if keyword.isdigit() : # concept_id 로 검색하기
        concepts = Concept.objects.filter(
            concept_id=int(keyword)
        )
    else : # like 이용해서 찾기 - 키워드 검색
        concepts = Concept.objects.filter(
            Q(concept_name__contains=keyword)|
            Q(domain_id__contains=keyword) |
            Q(concept_class_id__contains=keyword)
        )

    p = Paginator(concepts, 10, allow_empty_first_page = True)
    data = p.page(page)
    serializer = ConceptSerializer(data=data, many=True)
    serializer.is_valid()
    return Response(serializer.data)



@api_view(['get'])
def condition_occurence(request) :

    keyword = request.GET.get('keyword', '')
    page= int(request.GET.get('page', 1))

    cursor= connection.cursor()
    sql = """
    SELECT co.condition_occurrence_id, co.person_id, co.condition_concept_id, c1.concept_name as condition_concept_name,
    co.condition_start_date, co.condition_start_datetime, co.condition_end_date, co.condition_end_datetime, co.condition_type_concept_id, c2.concept_name as condition_type_concept_name,
    co.condition_status_concept_id, c3.concept_name as condition_status_concept_name, 
    co.stop_reason, co.provider_id, co.visit_occurrence_id, co.visit_detail_id, co.condition_source_value, co.condition_source_concept_id, co.condition_status_source_value
    FROM condition_occurrence co
    LEFT OUTER JOIN concept c1
    ON co.condition_concept_id=c1.concept_id
    LEFT OUTER JOIN concept c2
    ON co.condition_type_concept_id=c2.concept_id
    LEFT OUTER JOIN concept c3
    ON co.condition_status_concept_id=c3.concept_id
    WHERE c1.concept_name LIKE '%{keyword}%' OR
        c2.concept_name LIKE '%{keyword}%' OR
        c3.concept_name LIKE '%{keyword}%' 
    ORDER BY condition_occurrence_id
    OFFSET {page_num} LIMIT 10;
    """.format(
        keyword=keyword,
        page_num=(page-1)*10,
    )

    cursor.execute(sql)
    row = cursor.fetchall()

    column_name = ['condition_occurrence_id', 'person_id', 'condition_concept_id', 'condition_concept_name',
        'condition_start_date', 'condition_start_datetime', 'condition_end_date', 'condition_end_datetime', 'condition_type_concept_id', 'condition_type_concept_name',
        'condition_status_concept_id', 'condition_status_concept_name', 
        'stop_reason', 'provider_id', 'visit_occurrence_id', 'visit_detail_id', 'condition_source_value', 'condition_source_concept_id', 'condition_status_source_value']
    
    data = []
    for tmp in row :
        tmp_dic = {}
        for i in range(len(tmp)) :
            tmp_dic[column_name[i]] = tmp[i]
        data.append(tmp_dic)

    return Response(data)