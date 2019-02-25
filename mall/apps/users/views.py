from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .serializers import RegisterCreateSerializer
class RegisterUsernameCountAPIView(APIView):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        context = {
            'count':count,
            'username': username,
        }
        return Response(context)

class RegisterPhoneCountAPIView(APIView):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        context = {
            'mobile': mobile,
            'count': count,
        }
        return Response(context)

class RegisterCreateView(GenericAPIView):
    """
    实现注册功能:
        1.获取参数
        2.校验参数
        3.保存
    """
    serializer_class = RegisterCreateSerializer
    def post(self, request):
        serializer = self.get_serializer(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
