from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import  Response
from .permissions import IsOwnerOrReadOnly, IsOrganizerOrReadOnly
from rest_framework.views import  APIView
from .serializers import EventSerializer, RegistrationSerializer, CommentSerializer, RatingSerializer
from django.http import Http404
from .models import Event, Registration, Comment, Rating


# Events Views
class EventCreateListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerOrReadOnly]
    
    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(organizer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_object(self, event_id):
        try:
            return Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, event_id, format=None):
        event = self.get_object(event_id)
        serializer = EventSerializer(event)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, event_id, format=None):
        event = self.get_object(event_id)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id, format=None):
        event = self.get_object(event_id)
        event.delete()
        return Response({'detail': 'Evento eliminado.'},status=status.HTTP_204_NO_CONTENT)

# Registration Views
class RegisterEventView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, event_id, format=None):
        event = get_object_or_404(Event, id=event_id)
        if Registration.objects.filter(event=event, user=request.user).exists():
            return Response({'detail': 'Ya estás inscrito en este evento.'}, status=status.HTTP_400_BAD_REQUEST)
        if event.capacity <= Registration.objects.filter(event=event).count():
            return Response({'detail': 'El evento ha alcanzado su capacidad máxima.'}, status=status.HTTP_400_BAD_REQUEST)
        
        registration = Registration(event=event, user=request.user)
        registration.save()
        return Response({'detail': 'Inscripción exitosa.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, event_id, format=None):
        event = get_object_or_404(Event, id=event_id)
        registration = get_object_or_404(Registration, event=event, user=request.user)
        registration.delete()
        return Response({'detail': 'Inscripción cancelada.'}, status=status.HTTP_204_NO_CONTENT)

# Comments Views
class CommentsEventCreateListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, event_id, format=None):
        event = get_object_or_404(Event, id=event_id)
        comments = Comment.objects.filter(event=event)
        seriliazer = CommentSerializer(comments, many=True)
        return Response (seriliazer.data, status=status.HTTP_200_OK)

    def post(self, request, event_id, format=None):
        event = get_object_or_404(Event, id=event_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, event=event)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentsEventDetailUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pass