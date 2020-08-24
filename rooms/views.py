from django.shortcuts import render
from . import models
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from .serializers import RoomSerializer, BigRoomSerializer


class ListRoomsView(ListAPIView):
    queryset = models.Room.objects.all()
    serializer_class = RoomSerializer


class SeeRoomView(RetrieveAPIView):
    queryset = models.Room.objects.all()
    serializer_class = BigRoomSerializer

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
