from rest_framework import serializers
from .models import User
import re
from django_redis import get_redis_connection
class RegisterCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(label='验证密码', write_only=True)
    allow = serializers.CharField(laber='是否同意协议', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', min_length=6, max_length=6, write_only=True)
    class Meta:
        model = User
        fields = ('password', 'password2', 'mobile', 'allow', 'username', 'sms_code')
    def validate_mobile(self, value):
        """
        校验手机号格式是否正确
        :param attrs:
        :return:
        """
        if not re.match(r'1[3-9]\d{9}', value):
            raise serializers.ValidationError('手机号码不正确')
        return value
    def validate_allow(self, value):
        if not value:
            raise serializers.ValidationError('您未同意用户协议')
        return value
    def validate(self, attrs):
        password = attrs['password']
        password2 = attrs['password2']
        sms_code = attrs['sms_code']
        mobile = attrs['mobile']
        if password2 != password:
            return serializers.ValidationError('密码不一致')
        redis_conn = get_redis_connection('code')
        redis_sms_code = redis_conn.get('sms_%s' % mobile)
        if redis_sms_code.decode() != sms_code:
            return serializers.ValidationError('验证码不正确')
        return attrs





