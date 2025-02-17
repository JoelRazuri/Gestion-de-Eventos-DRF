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
from drf_spectacular.utils import OpenApiResponse


# VISTAS DE PERFIL PARA USUARIO
@extend_schema(
    tags=['Users'],
    request=CustomUserUpdateSerializer,  
    responses={
        200: OpenApiResponse(response=CustomUserListSerializer),
        400: OpenApiResponse(description="Bad Request - Datos proporcionados inválidos"),
        204: OpenApiResponse(description="Perfil de usuario eliminado con éxito")
    }
)
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
        return Response({'detail': 'Perfil eliminado.'}, status=status.HTTP_204_NO_CONTENT)
        


@extend_schema(
    tags=['Users'],
    responses={200: RegistrationSerializer}
)
class ProfileListRegistrationsView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        registrations = Registration.objects.filter(user=request.user)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

# VISTAS DE REGISTRO E INICIO DE SESIÓN
@extend_schema(
    tags=['Users'],
    request=CustomUserSerializer, 
    responses={201: CustomUserSerializer}
)
class RegisterUserView(APIView):
    def post(self, request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Users'],
    request=CustomUserTokenSerializer, 
    responses={
        201: CustomUserTokenSerializer,  
        401: OpenApiResponse(description="El usuario no está activo"),
        409: OpenApiResponse(description="Ya ha iniciado sesión")
    }
)
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
    

@extend_schema(
    tags=['Users'],
    responses={
        200: OpenApiResponse(description="Sesión cerrada exitosamente")
    }
)
class LogoutUserView(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAuthenticated]  

    def post(self, request, format=None):
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({'message': 'Sesión cerrada'}, status=status.HTTP_200_OK)
    

# LISTA DE USUARIOS PARA ADMINISTRADORES
@extend_schema(tags=['Users'])
class ListUsersView(APIView):
    authentication_classes = [TokenAuthentication] 
    permission_classes = [IsAdministrator]

    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserListSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)