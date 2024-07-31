from rest_framework import serializers
from .models import CustomUser
from events.models import Event

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'last_name', 'email', 'password', 'role']

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user
    

class CustomUserListSerializer(serializers.ModelSerializer):
    events = serializers.PrimaryKeyRelatedField(many=True, queryset=Event.objects.all())
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'name', 'last_name', 'email', 'password', 'role', 'events']
