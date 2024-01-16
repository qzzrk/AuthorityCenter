from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
import random
import string
import base64
import hashlib

from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from rest_framework import generics, permissions, serializers
from users.models import User
from oauth2_provider.signals import app_authorized


@api_view(['POST'])
def jwt_login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = User.objects.filter(username=username).first()
    if user and user.check_password(password):
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({"error": "Wrong Credentials"}, status=400)


@csrf_exempt
@api_view(['POST'])
def get_code_verifier(request):
    code_verifier = ''.join(
        random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
    code_challenge = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode('utf-8').replace('=', '')
    return Response({'code_challenge': code_challenge, 'code_verifier': code_verifier})


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', "first_name", "last_name")


class UserList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetails(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserTokenDetails(APIView):
    permission_classes = [permissions.IsAuthenticated, TokenHasReadWriteScope]

    def get(self, request, *args, **kwargs):
        # 获取用户对象
        user = request.user
        print(user)
        # 确保用户已经通过验证
        if not user or not user.is_authenticated:
            return JsonResponse({'error': 'Invalid token'}, status=401)

        # 从用户对象获取信息
        user_data = {
            'username': user.username,
            'openid': user.open_id,
            # 添加您需要的其他字段
        }

        return JsonResponse(user_data)


def handle_app_authorized(sender, request, token, **kwargs):
    print(token.user.open_id)
    print('App {} was authorized'.format(token.application.name))


app_authorized.connect(handle_app_authorized)
