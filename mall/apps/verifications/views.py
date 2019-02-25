from rest_framework.views import APIView
from libs.captcha.captcha import captcha
from django_redis import get_redis_connection
from django.http import HttpResponse
from .serializers import RegisterSMSCodeSerializer
from random import randint
from rest_framework.response import Response
class RegisterImageCodeView(APIView):
    def get(self, request, image_code_id):
        text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('code')
        redis_conn.setex('img_%s' % image_code_id, 60, text)
        # 这里HtttpResponse中的content_type来返回image格式的返回
        return HttpResponse(image, content_type='image/jpeg')

class RegisterImageCodeView(APIView):
    def get(self, request, mobile):
        """
        1. 对于图片验证码进行验证
        2. 生成手机验证码
        """
        query_params = request.query_params
        serializer = RegisterSMSCodeSerializer(data=query_params)
        serializer.is_valid(raise_exception=True)
        redis_conn = get_redis_connection('code')
        sms_code = '%06d' %randint(0, 999999)
        redis_conn.setex('sms_%s' % mobile, 60, sms_code)
        return Response({'massage': 'ok'})
