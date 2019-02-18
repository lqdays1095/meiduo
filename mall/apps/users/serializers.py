from rest_framework import serializers
from .models import User
import re
from django_redis import get_redis_connection
class RegisterCreateSerializer(serializers.Modelserializer):
    password2 = serializers.CharField(label='校验密码')
    sms_code = serializers.CharField(label='短信验证码', max_length=6, min_length=6, write_only=True)
    allow = serializers.CharField(label='是否同意协议', write_only=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'mobile', 'password2', 'sms_code', 'allow')
    def validate_mobile(self, value):
        if not re.match(r'1[345789]\d{9}', value):
            raise serializers.ValidationError('手机号码格式不正确')
        return value
    def validate_allow(self, value):
        if value != 'true':
            raise serializers.ValidationError('您未同意协议')
        return value
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        if password != password2:
            raise serializers.ValidationError('密码不一致')
        code = attrs['sms_code']
        redis_conn = get_redis_connection('code')
        mobile = attrs['mobile']
        redis_code = redis_conn.get('sms_%' % mobile)
        if redis_code is None:
            raise serializers.ValidationError('短信验证码过期')
        if redis_code.decode() != code:
            raise serializers.ValidationError('验证码不正确')
        return attrs
