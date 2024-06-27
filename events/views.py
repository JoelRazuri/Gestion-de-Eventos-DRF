from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework.response import  Response
from .permissions import IsOwnerOrReadOnly
from rest_framework.views import  APIView
from .serializers import EventSerializer
from django.http import Http404
from .models import Event, Registration


# Events Views
class EventCreateListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get(self, request, format=None):
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EventDetailUpdateDeleteView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Event.objects.get(pk=pk)
        except Event.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        event = self.get_object(pk)
        serializer = EventSerializer(event)
        return Response(serializer.data)

    def put(self, request, pk):
        event = self.get_object(pk)
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        event = self.get_object(pk)
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Registration Views
class RegisterForEventView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    
    def post(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        if Registration.objects.filter(event=event, user=request.user).exists():
            return Response({'detail': 'Ya estás inscrito en este evento.'}, status=status.HTTP_400_BAD_REQUEST)
        if event.capacity <= Registration.objects.filter(event=event).count():
            return Response({'detail': 'El evento ha alcanzado su capacidad máxima.'}, status=status.HTTP_400_BAD_REQUEST)
        
        registration = Registration(event=event, user=request.user)
        registration.save()
        return Response({'detail': 'Inscripción exitosa.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, event_id):
        event = get_object_or_404(Event, id=event_id)
        registration = get_object_or_404(Registration, event=event, user=request.user)
        registration.delete()
        return Response({'detail': 'Inscripción cancelada.'}, status=status.HTTP_204_NO_CONTENT)
