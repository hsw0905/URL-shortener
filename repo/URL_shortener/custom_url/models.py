import math
import random

from django.db import models

# Create your models here.
from rest_framework import status
from rest_framework.response import Response

from account.models import Account


class URL(models.Model):
    origin_url = models.CharField(max_length=1024, blank=True, null=True)
    shorten_url = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    converted_value = models.CharField(max_length=32)
    updated_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(Account, related_name='urls',on_delete=models.CASCADE,null=True)

    shorten = []
    #아스키코드 48 ~ 57 : 숫자 0 ~ 9
    #아스키코드 65 ~ 90 : 알파벳 A ~ Z
    #아스키코드 97 ~ 122 : 알파벳 a ~ z(코드번호 사이 특수문자)
    def generate_hash(self, min_length, max_length):
        if min_length <= 1:
            min_random = 0
        else:
            min_random = math.pow(74, min_length - 1)

        #두 정수 사이의 난수(최소값 초과 최대값 미만)
        max_random = math.pow(74, max_length - 1)
        result = math.floor(random.random() * (max_random - min_random) + min_random)

        return self.value_to_string(int(result))

    def value_to_string(self, value):
        x = value % 74
        y = math.floor(value / 74)

        if y > 0 :
            return self.value_to_string(int(y)) + self.value_to_char(int(x))
        else :
            return self.value_to_char(int(x))

    def value_to_char(self, value):
        asciiDec = 48 + value

        if asciiDec > 57 and asciiDec < 65: # 사이 특수문자 건너뜀
            asciiDec += 7
        elif asciiDec > 90 and asciiDec < 97:
            asciiDec += 6
        elif asciiDec > 122 :
            asciiDec -= 5
        self.shorten.append(chr(asciiDec))
        return chr(asciiDec)
