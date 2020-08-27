from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render
from . import models
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RoomSerializer


class OwnPagination(PageNumberPagination):
    page_size = 5


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
        pageinator = OwnPagination()
        rooms = models.Room.objects.all()
        results = pageinator.paginate_queryset(rooms, req)
        serializer = RoomSerializer(results, many=True)
        return pageinator.get_paginated_response(serializer.data)

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
        except models.Room.DoesNotExist:
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


@api_view(["GET"])
def room_search(req):

    max_price = req.GET.get('max_price', None)
    min_price = req.GET.get('min_price', None)
    beds = req.GET.get('beds', None)
    bedrooms = req.GET.get('bedrooms', None)
    bathrooms = req.GET.get('bathrooms', None)

    lat = req.GET.get('lat', None)
    lng = req.GET.get('lgn', None)

    filter_kwargs = {}
    if max_price is not None:
        filter_kwargs["price__lte"] = max_price
    if min_price is not None:
        filter_kwargs["price__gte"] = min_price
    if beds is not None:
        filter_kwargs["beds__gte"] = beds
    if bedrooms is not None:
        filter_kwargs["bedrooms__gte"] = bedrooms
    if bathrooms is not None:
        filter_kwargs["bathrooms__gte"] = bathrooms

    if lat is not None and lng is not None:
        filter_kwargs["lat__gte"] = float(lat) - 0.005
        filter_kwargs["lat__lte"] = float(lat) + 0.005
        filter_kwargs["lng__gte"] = float(lng) - 0.005
        filter_kwargs["lng__lte"] = float(lng) + 0.005

    paginator = OwnPagination()
    try:
        rooms = models.Room.objects.filter(**filter_kwargs)
    except ValueError:
        rooms = models.Room.objects.all()

    results = paginator.paginate_queryset(rooms, req)
    serializer = RoomSerializer(results, many=True)

    return paginator.get_paginated_response(serializer.data)
