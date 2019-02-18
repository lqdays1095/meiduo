from rest_framework import serializers
import logging
from django_redis import get_redis_connection
# from redis.exceptions import RedisError
class RegisterSMSCodeSerializer(serializers.Serializer):
    # 需要校验的是:text和对应的redis中的是否一致
    logger = logging.getLogger('meiduo')
    text = serializers.CharField(label='用户输入的验证码', max_length=4, min_length=4, required=True)
    image_code_id = serializers.UUIDField(label='验证码的标示id')
    def validate(self, attrs):
        text = attrs['text']
        image_code_id = attrs['image_code_id']
        redis_conn = get_redis_connection('code')
        redis_text = redis_conn.get('img_%s' % image_code_id)
        if redis_text is None:
            raise serializers.ValidationError("验证码已经过期")
        # try:
        #     redis_conn.delete('img_%s'% image_code_id)
        # except RedisError as e:
        #     logger.error(e)
        # redis中的数据都是二进制,所以要使用decode来编码
        if redis_text.decode().lower() != text.lower():
            return serializers.ValidationError('验证码错误')
        return attrs

