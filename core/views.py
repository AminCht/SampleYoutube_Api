from django.http import HttpResponse
from django.shortcuts import render
from django.core.cache import cache
import requests
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializer import ActivationCodeSerializer, RedeemCodeSerializer
from .tasks import notify_birth_day
import redis
from django.conf import settings


# Create your views here.


def notify(message):
    notify_birth_day.delay('hbd')
    return HttpResponse('ok')


redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)


class ActivationCodeApi(APIView):
    def post(self, request):
        serializer = ActivationCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        redis_instance.set(serializer.validated_data['email'], 2121, 120)
        return Response('ok')


class RedeemCode(APIView):

    def post(self, request):
        serializer = RedeemCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(redis_instance.get("amin@gmail.com").decode("utf-8"))
        print(serializer.validated_data['code'])
        if redis_instance.get("amin@gmail.com").decode("utf-8") == serializer.validated_data['code']:
            return Response('correct')
        return Response('not correct')

