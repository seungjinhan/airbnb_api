from django.shortcuts import render
from . import models
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ReadRoomSerializer, WriteRoomSerializer


@api_view(["GET", "POST"])
def room_view(req):
    if req.method == 'GET':
        rooms = models.Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(data=serializer)
    elif req.method == 'POST':
        if not req.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=req.data)
        if serializer.is_valid():
            room = serializer.save(user=req.user)
            room_serializer = ReadRoomSerializer(room).data
            return Response(status=status.HTTP_200_OK, data=room_serializer)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 위와 동일한 기능


class RoomsView(APIView):

    def get(self, req):
        rooms = models.Room.objects.all()
        serializer = ReadRoomSerializer(rooms, many=True).data
        return Response(data=serializer)

    def post(self, req):
        if not req.user.is_authenticated:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = WriteRoomSerializer(data=req.data)

        if serializer.is_valid():
            room = serializer.save(user=req.user)
            room_serializer = ReadRoomSerializer(room).data
            return Response(status=status.HTTP_200_OK, data=room_serializer)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class ListRoomsView(ListAPIView):
#     queryset = models.Room.objects.all()
#     serializer_class = RoomSerializer


class SeeRoomView(RetrieveAPIView):
    queryset = models.Room.objects.all()
    serializer_class = ReadRoomSerializer


class RoomView(APIView):

    def get_object(self, pk):
        try:
            room = models.Room.objects.get(pk=pk)
            return room

        except models.Room.DoesNotExist:
            return None

    def get(self, req, pk):
        room = self.get_object(pk)
        if room is not None:
            serializer = ReadRoomSerializer(room).data
            return Response(serializer)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, req, pk):
        room = self.get_object(pk)
        if room is not None:
            if room.user != req.user:
                return Response(status=status.HTTP_403_FORBIDDEN)
            serializer = WriteRoomSerializer(room, data=req.data, partial=True)
            if serializer.is_valid():
                room = serializer.save()
                return Response(ReadRoomSerializer(room).data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, req, pk):
        room = self.get_object(pk)
        if room.user != req.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        if room is not None:
            room.delete()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_NOT_FOUND)

    def post(self, req):
        pass

    # @api_view(["GET"])
    # def list_rooms(req):
    #     rooms = models.Room.objects.all()
    #     serialized = RoomSerializer(rooms, many=True)
    #     return Response(data=serialized.data)

    # class ListRoomsView(APIView):
    #     def get(self, req):
    #         rooms = models.Room.objects.all()
    #         serializer = RoomSerializer(rooms, many=True)
    #         return Response(data=serializer.data)
