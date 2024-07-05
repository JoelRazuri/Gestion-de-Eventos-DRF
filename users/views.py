from django.shortcuts import get_object_or_404
from events.serializers import RegistrationSerializer
from events.models import Registration
from .serializers import CustomUserSerializer
from .models import CustomUser
from rest_framework import status, permissions
from rest_framework.views import  APIView
from rest_framework.response import  Response
from django.http import Http404

# Users Views for administration
# faltan crear permisos para quien utiliza estas vistas, solo deben ser administradores (role=1)
class UserListView(APIView):
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
  

class UserDetailView(APIView):
    def get_object(self, user_id):
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise Http404
    
    def get(self, request, user_id, format=None):
        user = self.get_object(user_id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserListRegistrationsView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(CustomUser, id=user_id)
        registrations = Registration.objects.filter(user=user)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



# Profile Views for user
class ProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = CustomUser.objects.get(id=request.user.id)
        serializer = CustomUserSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileListRegistrationsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        registrations = Registration.objects.filter(user=request.user)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)