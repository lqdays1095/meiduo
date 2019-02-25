from rest_framework import serializers
from django_redis import get_redis_connection
class RegisterSMSCodeSerializer(serializers.Serializer):
    text = serializers.CharField(label='图形验证码', min_length=4, max_length=4)
    image_code_id = serializers.UUIDField(label = 'UUID')
    def validate(self, attrs):
        text = attrs['text']
        image_code_id = attrs['image_code_id']
        redis_conn = get_redis_connection('code')
        redis_text = redis_conn.get('img_%s' % image_code_id)
        if redis_text is None:
            return serializers.ValidationError("验证码已经过期")
        if redis_text.decode().lower() != text:
            return serializers.ValidationError("验证码不正确")
        return attrs

