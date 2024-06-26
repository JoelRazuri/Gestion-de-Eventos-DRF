from .serializers import CustomUserSerializer
from .models import CustomUser
from rest_framework import status
from rest_framework.views import  APIView
from rest_framework.response import  Response
from django.http import Http404


class UserListView(APIView):
    def get(self, request, format:None):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data)
    

class UserDetailView(APIView):
    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    
    def get(self, request, pk,format:None):
        user = self.get_object(pk)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)