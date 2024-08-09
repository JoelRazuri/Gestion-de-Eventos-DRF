from django.shortcuts import get_object_or_404
from events.serializers import RegistrationSerializer
from events.models import Registration
from .serializers import CustomUserSerializer, CustomUserListSerializer, CustomUserTokenSerializer
from .models import CustomUser
from rest_framework import status
from rest_framework.views import  APIView
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import  Response
from django.http import Http404


# Profile Views for user
class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        profile = CustomUser.objects.get(id=request.user.id)
        serializer = CustomUserListSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileListRegistrationsView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request):
        registrations = Registration.objects.filter(user=request.user)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Register and Login views
class RegisterUserView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(ObtainAuthToken):
    def post(self, request, format=None):
        login_serializer = self.serializer_class(data=request.data, context={'request':request})
        if login_serializer.is_valid():
            user = login_serializer.validated_data['user']
            if user.is_active:
                token, created = Token.objects.get_or_create(user=user)
                user_serializer = CustomUserTokenSerializer(user)
                if created:
                    return Response(
                        {
                            'token': token.key,
                            'user': user_serializer.data
                        }, 
                        status=status.HTTP_201_CREATED
                    )
                token.delete()
                return Response({'message_error': 'Ya ha iniciado sesión'}, status=status.HTTP_409_CONFLICT)
            return Response({'message': 'El usuario no esta activo'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(login_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutUserView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, format=None):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Sesión cerrada'}, status=status.HTTP_200_OK)