from events.serializers import RegistrationSerializer
from events.models import Registration
from .serializers import CustomUserSerializer, CustomUserListSerializer, CustomUserTokenSerializer, CustomUserUpdateSerializer
from .models import CustomUser
from rest_framework import status
from rest_framework.views import  APIView
from rest_framework.authtoken.views import ObtainAuthToken 
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import  Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdministrator

# Profile Views for user
@extend_schema(tags=['Users'])
class ProfileView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        serializer = CustomUserListSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, format=None):
        serializer = CustomUserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, format=None):
        request.user.delete()
        return Response({'detail': 'Perfil eliminado.'},status=status.HTTP_204_NO_CONTENT)
        


@extend_schema(tags=['Users'])
class ProfileListRegistrationsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        registrations = Registration.objects.filter(user=request.user)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# Register and Login views
@extend_schema(tags=['Users'])
class RegisterUserView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['Users'])
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
    

@extend_schema(tags=['Users'])
class LogoutUserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Sesión cerrada'}, status=status.HTTP_200_OK)
    

# List users for Administrators
@extend_schema(tags=['Users'])
class ListUsersView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdministrator]

    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)