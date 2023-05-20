#!/usr/bin/env python
import os
from pytz import utc
from datetime import datetime

from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField

from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User as DjangoUser

from sahha_service import models

# ========================
# DjangoUser
# ========================
class DjangoUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DjangoUser
        fields = ('id', 'email', 'password', 'first_name',
                  'last_name', 'username', 'is_active')
        extra_kwargs = {
            'password': {'write_only': True},
            'username': {'write_only': True, 'validators': []}
        }

    def validate_password(self, value):
        if value:
            return make_password(value)
        return value

class DjangoUserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.DjangoUser
        fields = ('email', 'first_name', 'last_name', 'is_active', 'id')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'username'
        )
# ========================
# SahhaUser
# ========================
class SahhaUserSerializer(serializers.ModelSerializer):    
    django_user = DjangoUserSerializer()
    # tag = RoleSerializer(read_only=True, many=True)
    
    class Meta:
        model = models.SahhaUser
        fields = '__all__'

    def create(self, validated_data):
        django_user = DjangoUserSerializer().create(
            {**validated_data.pop('django_user')})
        return super().create({'django_user': django_user, **validated_data})

    def update(self, instance, validated_data):
        django_user = DjangoUserSerializer().update(
            instance.django_user, validated_data.pop('django_user', {}))
        return super().update(instance, {**validated_data, 'django_user': django_user})

    def to_representation(self, instance):           
        response = serializers.ModelSerializer.to_representation(self, instance)
        django_user_info = response.pop('django_user')
        response['django_id'] = django_user_info['id']
        response['first_name'] = django_user_info['first_name']
        response['last_name'] = django_user_info['last_name']
        response['email_address'] = django_user_info['email']
        return response

# ========================
# Login/Registration
# ========================

# pylint: disable=abstract-method
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        validated_data = super().validate(attrs)

        email = validated_data['email']
        password = validated_data['password']

        user = authenticate(
            request=None, username=email.lower().strip(), password=password
        )

        if not user:
            raise ValidationError(
                'Email address or password is incorrect.'
            )
        
        validated_data['user'] = user
        return validated_data

    def create(self, validated_data):
        """This is implemented so that we can use `GenericAPIVIew`"""
        return validated_data.get('user', None)


class LogoutViewSerializer(serializers.Serializer):
    pass

