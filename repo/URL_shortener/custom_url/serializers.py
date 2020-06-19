from rest_framework import serializers
from .models import URL


class URLSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(required=False)
    class Meta:
        model = URL
        fields = ['id', 'title', 'origin_url', 'shorten_url', 'converted_value', 'owner', 'updated_at',]