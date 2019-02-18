from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from django_redis import get_redis_connection
from django.http.response import HttpResponse
from .serializers import RegisterSMSCodeSerializer
from rest_framework import status
from random import randint
from rest_framework.generics import GenericAPIView
# Create your views here.
from libs.captcha.captcha import captcha
class RegisterImageCodeView(APIView):
    def get(self, request, image_code_id):
        # generate:生成
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s' % image_code_id, 60, text)
        # 可以设置返回数据的不同的格式
        return HttpResponse(image, content_type='image/jpeg')

class RegisterSMSCodeView(GenericAPIView):
    serializer_class = RegisterSMSCodeSerializer
    def get(self,request, mobile):

        # 创建序列化器, 定义text和image_code_id
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        # redis
        redis_conn = get_redis_connection('code')
        # 判断该用户是否频繁获取
        if redis_conn.get('sms_flag_%s'%mobile):
            return Response(status=status.HTTP_429_TOO_MANY_REQUESTS)
        # 生成短信验证码
        sms_code = '%06d'%randint(0,999999)
        # redis增加记录
        redis_conn.setex('sms_%s'%mobile,5*60,sms_code)
        redis_conn.setex('sms_flag_%s'%mobile,60,1)
        # 返回响应
        return Response({'message':'ok'})