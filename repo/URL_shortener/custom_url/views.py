from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect
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
    lookup_field = 'converted_value'


    @action(detail=False, methods=['POST'])
    def shorten_url(self,request):
        instance = URL(title=request.data.get('title'),
                       origin_url=request.data.get('origin_url'),
                       owner_id=request.data.get('owner'), )
        #5글자로 해싱
        instance.generate_hash(4, 6)
        instance.converted_value = "".join(instance.shorten)
        instance.shorten.clear()
        instance.shorten_url = f"http://127.0.0.1:8000/api/urls/{instance.converted_value}"
        instance.save()
        return Response({"id": instance.id,
                         "origin_url": instance.origin_url,
                         "title": instance.title,
                         "shorten_url": instance.shorten_url,
                         "converted_value": instance.converted_value,
                         "owner": instance.owner_id},
                        status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return HttpResponsePermanentRedirect(redirect_to=serializer.data['origin_url'])