#!/usr/bin/env python

import base64
import logging

import requests

from django.conf import settings
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework import generics
from rest_framework import permissions
from rest_framework import response
from rest_framework import status
from rest_framework import views
from rest_framework.exceptions import ValidationError

from rest_framework.authtoken.models import Token


from sahha_service import models
from sahha_service.utils.helpers import SahhaUserSecuredApiView, logger, dict_filter, dict_filter_validate
from .serializers import (
    DjangoUserSerializer,
    DjangoUserLightSerializer,
    SahhaUserSerializer,
    LoginSerializer,
    UserSerializer,
    LogoutViewSerializer,
)

from drf_yasg.utils import swagger_auto_schema
from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY, TYPE_INTEGER, IN_QUERY, Items, Parameter, Response as OpenAPIResponse

User = get_user_model()
logger = logging.getLogger('sahha_service.users')

car_id = Parameter('car_id', in_=IN_QUERY,
                   type=TYPE_INTEGER)


class SignupView(SahhaUserSecuredApiView):
    response_json = {
        'Response': {
            "id": TYPE_INTEGER,
            "created_at": TYPE_STRING,
            "updated_at": TYPE_STRING,
            "phone_number": TYPE_STRING,
            "first_name": TYPE_STRING,
            "last_name": TYPE_STRING,
            "email": TYPE_STRING,
            'phone_number': TYPE_STRING,
        }
    }

    @swagger_auto_schema(
        request_body=Schema(
            type=TYPE_OBJECT,
            properties={
                'first_name': Schema(type=TYPE_STRING, description='User first name'),
                'last_name': Schema(type=TYPE_STRING, description='User last name'),
                'email': Schema(type=TYPE_STRING, description='Email address'),
                'password': Schema(type=TYPE_STRING, description='Password'),
                'confirm_password': Schema(type=TYPE_STRING, description='The same password again'),
                'role': Schema(type=TYPE_STRING, description='RoleID'),
                'agence_id': Schema(type=TYPE_STRING, description='agence_id'),
                'phone_number': Schema(type=TYPE_STRING, description='Phone number'),
            },
            required=['first_name', 'last_name', 'email',
                      'password', 'confirm_password', 'role', 'agence_id', 'phone_number']
        ),
        responses={
            status.HTTP_409_CONFLICT: 'Email already exists',
            status.HTTP_400_BAD_REQUEST: 'Password validation failed',
            status.HTTP_200_OK: OpenAPIResponse(description='', examples=response_json)
        }
    )
    def post(self, request):
        """
        API for user to register and create an account
        """
        data = dict_filter_validate(
            request.data, ['email', 'first_name', 'last_name',
                           'password', 'confirm_password', 'role','agence_id',  'phone_number']
        )
        django_user = models.DjangoUser.objects.filter(
            username=data['email'].lower()).first()
        if django_user and django_user.is_active:
            return response.Response(
                {'error': 'Email already exists.'},
                status=status.HTTP_409_CONFLICT)
        try:
            validate_password(data['password'])
        except ValidationError:
            return response.Response(
                {'error': 'Password not complex enough', },
                status=status.HTTP_400_BAD_REQUEST
            )
        if data["password"] != data["confirm_password"]:
            return response.Response(
                {'error': 'password and  confirm_password does not match', },
                status=status.HTTP_400_BAD_REQUEST
            )

        user_fields = DjangoUserSerializer().get_fields()
        data['django_user'] = {
            k: data.pop(k) for k in data.copy().keys() if k in user_fields
        }
        data['django_user']['username'] = data['django_user']['email'].lower()
        data['django_user']['email'] = data['django_user']['email'].lower()
        data['django_user']['is_active'] = True

        serializer = None
        if django_user and not django_user.is_active:
            serializer = SahhaUserSerializer(
                django_user.sahha_user,
                data=data,
                partial=True
            )
        else:
            serializer = SahhaUserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        logger.debug("User signed up successfully %s" %
                     (serializer.instance.django_user.email))
        return response.Response(SahhaUserSerializer(serializer.instance).data, status=status.HTTP_200_OK)


class LoginView(generics.GenericAPIView):

    authentication_classes = ()
    permission_classes = (permissions.AllowAny, )
    serializer_class = LoginSerializer
    queryset = User.objects.none()

    def post(self, request):
        login_serializer = self.get_serializer(data=request.data)

        if login_serializer.is_valid():

            django_user = login_serializer.save()
            last_login = django_user.last_login

            login(request, django_user)

            logger.info(
                'User (%s, "%s") logged in. Their last login was %s.',
                django_user.id,
                django_user.username,
                last_login
            )
            token, _ = Token.objects.get_or_create(user=django_user)
            data = SahhaUserSerializer(django_user.sahha_user).data
            data['token'] = token.key

            return response.Response(
                data, status=status.HTTP_200_OK
            )
        return response.Response(
            {'error': 'Email address or password is incorrect.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(views.APIView):

    permission_classes = ()
    serializer_class = LogoutViewSerializer

    @swagger_auto_schema(
        manual_parameters=[car_id],
    )
    def post(self, request):
        active_user = False

        if request.user.is_authenticated:
            active_user = True
            username = request.user.username
            user_id = request.user.id
            last_login = request.user.last_login

        logout(request)

        if active_user:
            logger.info(
                'User (%s, "%s") logged out. Their last login was %s.',
                user_id,
                username,
                last_login
            )
        else:
            logger.info('Anonymous user attempted to logout.')

        return response.Response({}, status=status.HTTP_200_OK)


class UserView(generics.RetrieveAPIView):

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )
    queryset = User.objects.none()

    def get_object(self):
        return self.request.user
