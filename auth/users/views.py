from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt
import datetime


class RegisterView(APIView):
    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    @staticmethod
    def post(request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('Пользователь не найден')
        if not user.check_password(password):
            raise AuthenticationFailed('Неверный пароль')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=300),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
        }

        return response


class UserView(APIView):
    @staticmethod
    def get(request):
        token = request.COOKIES.get('jwt')
        user = User.objects(id=payload['id']).first()
        serializer = UserSerializer(user)

        if not token:
            raise AuthenticationFailed('не прошедший проверку подлинности')
        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('не прошедший проверку подлинности')
        return Response(serializer.data)


class Logout(APIView):
    @staticmethod
    def post(request):
        response = Response()
        response .delete_cookie('jwt')
        response.data = {
            'message': "Успешно"
        }

        return response
