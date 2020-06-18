from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from account.models import Account
from account.permissions import IsCorrectUser
from account.serializers import AccountSerializer
from rest_framework.authtoken.models import Token

#계정
class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsCorrectUser]


    @action(detail=False, methods=['POST'])
    def sign_up(self,request):
        new_account = Account(email=request.data.get('email'),username=request.data.get('username'),)
        new_account.set_password(request.data.get('password'))
        new_account.save()
        return Response({"id":new_account.id,"email":new_account.email,"username":new_account.username }, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['POST'])
    def sign_in(self,request):
        password = request.data.get('password')
        account = Account.objects.get(email=request.data.get('email'),username=request.data.get('username'))

        if account.check_password(password):
            token, created = Token.objects.get_or_create(user=account)
            return Response({'token': token.key,
                             'id': account.id,
                             'email': account.email,
                             'username':account.username,
                             },
                            status=status.HTTP_201_CREATED)
        data = {
            "message": "incorrect password"
        }
        return Response(data, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['DELETE'])
    def sign_out(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['DELETE'])
    def deactivate(self, request, *args, **kwargs):
        return super().destroy(self, request, *args, **kwargs)

    #url: /update시 실행 목적, 이거 넣으면 에러남
    # @action(detail=True, methods=['PUT'])
    # def update(self, request, *args, **kwargs):
    #     return super().update(self, request, *args, **kwargs)

def home_screen_view(request):
    return render(request,"base.html",{})