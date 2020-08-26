from django.shortcuts import render
from . import models
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer


@api_view(["GET", "POST"])
def room_view(req):
    if req.method == 'GET':
        rooms = models.Room.objects.all()
        serializer = RoomSerializer(rooms, many=True).data
        return Response(data=serializer)
    elif req.method == 'POST':
        if not req.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=req.data)
        if serializer.is_valid():
            room = serializer.save(user=req.user)
            room_serializer = RoomSerializer(room).data
            return Response(status=status.HTTP_200_OK, data=room_serializer)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 위와 동일한 기능


class RoomsView(APIView):

    def get(self, req):
        rooms = models.Room.objects.all()
        serializer = RoomSerializer(rooms, many=True).data
        return Response(data=serializer)

    def post(self, req):
        if not req.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = RoomSerializer(data=req.data)

        if serializer.is_valid():
            room = serializer.save(user=req.user)
            room_serializer = RoomSerializer(room).data
            return Response(status=status.HTTP_200_OK, data=room_serializer)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ListRoomsView(ListAPIView):
#     queryset = models.Room.objects.all()
#     serializer_class = RoomSerializer


class SeeRoomView(RetrieveAPIView):
    queryset = models.Room.objects.all()
    serializer_class = RoomSerializer


class RoomView(APIView):
    def get_room(self, pk):
        try:
            room = models.Room.objects.get(pk=pk)
            return room
        except Room.DoesNotExist:
            return None

    def get(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            serializer = RoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = RoomSerializer(room, data=request.data, partial=True)
            if serializer.is_valid():
                room = serializer.save()
                return Response(RoomSerializer(room).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        room = self.get_room(pk)
        if room is not None:
            if room.user != request.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
