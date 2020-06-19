from rest_framework import serializers
from account.models import Account
from custom_url.serializers import URLSerializer


class AccountSerializer(serializers.ModelSerializer):
    urls = URLSerializer(many=True, read_only=True)
    class Meta:
        model = Account
        fields = ['id', 'email', 'username','password' ,'date_joined', 'urls',]
        extra_kwargs = {'password': {'write_only': True}}


