from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, authentication
from rest_framework.response import  Response
from .permissions import IsOwnerEventOrReadOnly, IsOrganizerAdminOrReadOnly, IsOwnerCommentRatingOrReadOnly
from rest_framework.views import  APIView
from .serializers import EventSerializer, CommentSerializer, RatingSerializer
from django.http import Http404
from .models import Event, Registration, Comment, Rating
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiResponse



# VISTAS EVENTOS
@extend_schema(
    tags=['Events'],
    request=EventSerializer,
    responses={
        200: OpenApiResponse(response=EventSerializer, description="Lista de eventos"),
        201: OpenApiResponse(response=EventSerializer, description="Evento creado exitosamente"),
        400: OpenApiResponse(description="Bad Request - Datos proporcionados inválidos")
    }
)
class EventCreateListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOrganizerAdminOrReadOnly]
    
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


@extend_schema(
    tags=['Events'],
    request=EventSerializer,
    responses={
        200: OpenApiResponse(response=EventSerializer, description="Detalles del evento"),
        204: OpenApiResponse(description="Evento eliminado exitosamente"),
        400: OpenApiResponse(description="Bad Request - Datos proporcionados inválidos"),
        404: OpenApiResponse(description="Evento no encontrado")
    }
)
class EventDetailUpdateDeleteView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerEventOrReadOnly]
    
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


# VISTAS REGISTRO A EVENTO
@extend_schema(
    tags=['Events Registrations'],
    request=None,
    responses={
        201: OpenApiResponse(description="Inscripción exitosa"),
        204: OpenApiResponse(description="Inscripción cancelada"),
        400: OpenApiResponse(description="Bad Request - Ya estás inscrito o el evento alcanzó su capacidad máxima"),
        404: OpenApiResponse(description="Evento no encontrado")
    }
)
class RegisterEventView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, event_id, format=None):
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


# VISTAS COMENTARIOS
@extend_schema(
    tags=['Events Comments'],
    request=CommentSerializer,
    responses={
        200: OpenApiResponse(response=CommentSerializer, description="Lista de comentarios"),
        201: OpenApiResponse(description="Comentario creado exitosamente"),
        400: OpenApiResponse(description="Bad Request - Datos proporcionados inválidos"),
        404: OpenApiResponse(description="Evento no encontrado")
    }
)
class CommentsEventCreateListView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
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


@extend_schema(
    tags=['Events Comments'],
    request=CommentSerializer,
    responses={
        200: OpenApiResponse(response=CommentSerializer, description="Comentario obtenido exitosamente"),
        204: OpenApiResponse(description="Comentario eliminado exitosamente"),
        400: OpenApiResponse(description="Bad Request - Datos proporcionados inválidos"),
        404: OpenApiResponse(description="Comentario o evento no encontrado")
    }
)

class CommentsEventDetailUpdateDeleteView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerCommentRatingOrReadOnly]

    def get_object(self, event_id, comment_id):
        try:
            event = get_object_or_404(Event, id=event_id)
            return Comment.objects.get(id=comment_id, event=event)
        except Comment.DoesNotExist:
            return Http404

    def get(self, request, event_id, comment_id, format=None):
        comment = self.get_object(event_id, comment_id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, event_id, comment_id, format=None):
        comment = self.get_object(event_id, comment_id)
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, event_id, comment_id, format=None):
        comment = self.get_object(event_id, comment_id)
        comment.delete()
        return Response({'detail': 'Comentario eliminado'}, status=status.HTTP_204_NO_CONTENT)


# VISTAS RATING
@extend_schema(
    tags=['Events Ratings'],
    request=RatingSerializer,
    responses={
        200: OpenApiResponse(response=RatingSerializer, description="Calificaciones obtenidas exitosamente"),
        201: OpenApiResponse(response=RatingSerializer, description="Calificación creada exitosamente"),
        400: OpenApiResponse(description="Bad Request - Datos proporcionados inválidos")
    }
)
class RatingsEventView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, event_id, format=None):
        event = get_object_or_404(Event, id=event_id)
        ratings = Rating.objects.filter(event=event)
        serializer = RatingSerializer(ratings, many=True)
        return Response (serializer.data, status=status.HTTP_200_OK)

    def post(self, request, event_id, format=None):
        event = get_object_or_404(Event, id=event_id)
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid(): 
            serializer.save(event=event, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=['Events Ratings'],
    request=RatingSerializer,
    responses={
        200: OpenApiResponse(response=RatingSerializer, description="Calificación actualizada exitosamente"),
        400: OpenApiResponse(description="Bad Request - Datos proporcionados inválidos"),
        404: OpenApiResponse(description="No se encontró la calificación")
    }
)
class RatingEventUpdateView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerCommentRatingOrReadOnly]

    def get_object(self, event_id, rating_id):
        try:
            event = get_object_or_404(Event, id=event_id)
            return Rating.objects.get(id=rating_id, event=event)
        except Rating.DoesNotExist:
            return Http404

    def put(self, request, event_id, rating_id, format=None):
        comment = self.get_object(event_id, rating_id)
        serializer = RatingSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)