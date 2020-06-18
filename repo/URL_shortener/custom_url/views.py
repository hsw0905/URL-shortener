from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from custom_url.models import URL
from custom_url.serializers import URLSerializer


class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    # base_url = 'http://localhost:8000'

    @action(detail=False, methods=['POST'])
    def shorten_url(self,request):
        instance = URL(title=request.data.get('title'),
                       origin_url=request.data.get('origin_url'),
                       owner_id=request.data.get('owner'), )
        instance.generate_hash(4, 6)
        instance.converted_value = "".join(instance.shorten)
        instance.save()
        return Response({"id": instance.id,
                         "origin_url": instance.origin_url,
                         "title": instance.title,
                         "shorten_url": instance.shorten_url,
                         "converted_value": instance.converted_value,
                         "owner": instance.owner_id},
                        status=status.HTTP_201_CREATED)
