from rest_framework import serializers
from .models import Event, Rating, Registration, Comment


class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.ReadOnlyField(source='organizer.username')
    
    class Meta:
        model = Event
        fields = '__all__'


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Registration
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    event = serializers.ReadOnlyField(source='event.tilte')

    class Meta:
        model = Comment
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    event = serializers.ReadOnlyField(source='event.tilte')
    
    class Meta:
        model = Rating
        fields = '__all__'