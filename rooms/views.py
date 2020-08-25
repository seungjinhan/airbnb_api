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
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class ListRoomsView(ListAPIView):
#     queryset = models.Room.objects.all()
#     serializer_class = RoomSerializer


class SeeRoomView(RetrieveAPIView):
    queryset = models.Room.objects.all()
    serializer_class = ReadRoomSerializer

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
