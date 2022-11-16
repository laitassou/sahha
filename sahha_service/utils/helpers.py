from django.core.files import File
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.core.paginator import Paginator
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

from rest_framework import views
from rest_framework.parsers import JSONParser
from rest_framework_api_key.permissions import HasAPIKey

from sahha_service.utils import exceptions, permissions
from sahha_service import models
from sahha_service.settings import MEDIA_ROOT, SIMPLE_JWT

from io import BytesIO, StringIO
from logging import getLogger
from pathlib import Path
from os import path
from mimetypes import guess_extension
from sys import getsizeof, maxsize
from urllib.parse import urlparse
import json, random, string, os, requests, subprocess, hashlib, binascii, sys, jwt
from pytz import utc
from datetime import datetime
import random, string, base64

logger = getLogger(__name__)

def fix_search_args(data, *args):
    fixed_args = []
    for arg in args:
        if type(arg) == tuple:
            if data.get(arg[1]):
                data[arg[1]] = arg[0](data[arg[1]])
            fixed_args.append(arg[1])

        else:
            fixed_args.append(arg)

    return fixed_args

def dict_filter_validate(data, *args, fix_args=False):
    filtered_data = []
    missings = []

    for list_index, list_fields in enumerate(args):        
        filtered_data.append({})
        missings.append([])        
        for k in list_fields:
            if data.get(k) is not None:
                if isinstance(data[k], str):
                    filtered_data[list_index][k] = data[k].strip()
                else:
                    filtered_data[list_index][k] = data[k]
            else:
                missings[list_index].append(k)

        if len(missings[list_index]) == 0:
            return filtered_data[list_index]

    raise exceptions.missingFields(missings)

def dict_filter(data, *args):
    args = fix_search_args(data, *args)

    return {k: v for k, v in data.items() if k in args}

class SahhaUserApiView(views.APIView):
    parser_classes = (JSONParser,)
    permission_classes = (permissions.IsActiveUser,)

class SahhaUserSecuredApiView(SahhaUserApiView):
    # permission_classes = [HasAPIKey]
    permission_classes = []



