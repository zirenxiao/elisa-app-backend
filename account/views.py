# Create your views here.

from django.contrib import auth
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView

from common.code import *
from common.common import get_user_instance
from .models import ExtendedUser as User


class LogOutViewSet(APIView):

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        try:
            Token.objects.get(key=token).delete()
            return JsonResponse({"code": ACCOUNT_LOGOUT_SUCCESS,
                                 "msg": 'ACCOUNT_LOGOUT_SUCCESS'})
        except:
            return JsonResponse({"code": ACCOUNT_TOKEN_ERROR,
                                 "msg": 'ACCOUNT_TOKEN_ERROR'})


class GetViewSet(APIView):

    def post(self, request, *args, **kwargs):
        user = get_user_instance(request)
        if user is None:
            return JsonResponse({"code": ACCOUNT_TOKEN_ERROR,
                                 "msg": 'ACCOUNT_TOKEN_ERROR'})

        return JsonResponse({"code": ACCOUNT_GET_SUCCESS,
                             "msg": 'ACCOUNT_GET_SUCCESS',
                             "details": {
                                 'username': user.username,
                                 'email': user.email,
                                 'birthday': user.birthday,
                                 'first_name': user.first_name,
                                 'last_name': user.last_name,
                             }})


class UpdateViewSet(APIView):

    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        birthday = request.data.get('birthday')
        password = request.data.get('password')
        email = request.data.get('email')

        try:
            user_id = Token.objects.get(key=token).user_id
        except:
            return JsonResponse({"code": ACCOUNT_TOKEN_ERROR,
                                 "msg": 'ACCOUNT_TOKEN_ERROR'})
        user_obj = User.objects.get(id=user_id)

        if first_name is not None:
            user_obj.first_name = first_name
        if last_name is not None:
            user_obj.last_name = last_name
        if birthday is not None:
            user_obj.birthday = birthday
        if password is not None:
            try:
                user_obj.set_password(password)
            except:
                return JsonResponse({"code": ACCOUNT_UPDATE_PASSWORD_INVALID,
                                     "msg": 'ACCOUNT_UPDATE_PASSWORD_INVALID'})
        try:
            if email is not None:
                user_obj.email = email
                user_obj.username = email
            user_obj.save()
        except Exception as e:
            return JsonResponse({"code": ACCOUNT_UPDATE_FAIL,
                                     "msg": 'ACCOUNT_UPDATE_FAIL'})

        return JsonResponse({"code": ACCOUNT_UPDATE_SUCCESS,
                             "msg": 'ACCOUNT_UPDATE_SUCCESS'})


class RegisterViewSet(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        try:
            User.objects.create_user(username=username, password=password, email=email, first_name=first_name,
                                     last_name=last_name, birthday="1970-01-01")
        except Exception as e:
            return JsonResponse({"code": ACCOUNT_REGISTER_ERROR,
                                     "msg": str(e)})

        return JsonResponse({"code": ACCOUNT_REGISTER_SUCCESS,
                             "msg": 'ACCOUNT_REGISTER_SUCCESS'})


class LoginViewSet(APIView):

    def validate_user(self, request):
        pass

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = auth.authenticate(username=username, password=password)
        if not user:
            return JsonResponse({"code": ACCOUNT_LOGIN_FAIL,
                                 "msg": 'ACCOUNT_LOGIN_FAIL'})
        Token.objects.filter(user=user).delete()
        return JsonResponse({"code": ACCOUNT_LOGIN_SUCCESS,
                             "msg": 'ACCOUNT_LOGIN_SUCCESS',
                             "token": Token.objects.create(user=user).key})
