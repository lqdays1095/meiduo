from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView
# Create your views here.
class RegisterUsernameCountAPIView(APIView):
    def get(self, request, username):  # 这个是拼接在路径后面的参数
        # 通过查询用户名的个数来确定用户是否存在
        count = User.objects.filter(username=username).count()
        context = {
            'count': count,
            'username':username,
        }
        return Response(context)

class RegisterPhoneCountAPIView(APIView):
    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        context = {
            'count': count,
            'phone': mobile,
        }
        return Response(context)