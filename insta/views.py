import time

from django.shortcuts import render
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from .serializers import ProfileSerializer, HXProfileSerializer
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from .PACK.instagram import start
import httpx
import json
from lxml.html import fromstring
import urllib.request


@api_view(['GET'])
@throttle_classes([AnonRateThrottle, UserRateThrottle])
def profile(request, username=None):

    if not username:
        return Response({'error': 'Username is required.'}, status=200)

    data = start(username)
    serialized = ProfileSerializer(data=data)
    if not serialized.is_valid():
        return Response(serialized.errors, status=200)
    return Response(serialized.data, status=200)
