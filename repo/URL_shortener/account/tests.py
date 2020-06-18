from base64 import encode

from django.contrib.auth.hashers import make_password
from munch import Munch
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import Account
from model_bakery import baker

class UserTestCase(APITestCase):
    def setUp(self) -> None:
        #테스트 시작시 계정 1개 생성
        self.testAccount = Account(email="test@example.com", username="test", password="1111", )
        self.data = {"email": self.testAccount.email, "username":"test", "password": "1111", }
        self.testAccount.set_password(self.testAccount.password)
        self.testAccount.save()

    #유저가 제대로 생성되었는지
    def test_should_create(self):
        data={"email":"newemail@example.com", "username":"newuser","password":"1111" }
        response = self.client.post('/api/users/sign_up', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertEqual(user_response.email, data['email'])
        self.assertEqual(user_response.username, data['username'])

    #암호 인증시 토큰 제대로 발급받았는지
    def test_should_login(self):
        response = self.client.post('/api/users/sign_in', data=self.data)
        user_response = Munch(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(user_response.token)
        self.assertEqual(user_response.email, self.data['email'])
        self.assertEqual(user_response.username, self.data['username'])


    #토큰이 DB에서 정말 삭제되었는지
    def test_should_logout(self):
        response = self.client.post('/api/users/sign_in', data=self.data)
        token = response.data['token']
        self.client.force_authenticate(user=self.testAccount, token=token)
        response = self.client.delete('/api/users/sign_out')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Token.objects.filter(pk=token).exists())


    #계정이 DB에서 정말 삭제되었는지
    def test_should_delete_account(self):
        self.client.force_authenticate(user=self.testAccount)
        entry = Account.objects.get(id = self.testAccount.id)
        response = self.client.delete(f'/api/users/{entry.id}/deactivate')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(id = entry.id).exists())

    #계정 정보가 정말 바뀌었는지
    def test_should_update_account(self):
        prev_username = self.testAccount.username
        self.client.force_authenticate(user=self.testAccount)
        data = {'email':self.testAccount.email,'username':'newname','password':'1111'}

        response = self.client.put(f'/api/users/{self.testAccount.id}', data=data)
        user_response = Munch(response.data)
        self.assertTrue(user_response.id)
        self.assertNotEqual(user_response.username, prev_username)
