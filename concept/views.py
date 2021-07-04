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
def search(request) :
    # concept/?keyword=&page=
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

     