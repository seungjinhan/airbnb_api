from django.conf import settings
import jwt
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rooms.serializers import RoomSerializer
from rooms.models import Room


class UsersView(APIView):

    def post(self, req):
        serializer = UserSerializer(data=req.data)
        if serializer.is_valid():
            new_user = serializer.save()
            return Response(UserSerializer(new_user).data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, req):
        return Response(UserSerializer(req.user).data)

    def put(self, req):
        serializer = UserSerializer(req.user, data=req.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FavsView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, req):
        user = req.user
        serializer = RoomSerializer(user.favs.all(), many=True).data
        return Response(serializer)

    def put(self, req):
        pk = req.data.get('pk')
        user = req.user
        if pk is not None:
            try:
                room = Room.objects.get(pk=pk)
                if room in user.favs.all():
                    user.favs.remove(room)
                else:
                    user.favs.add(room)
                return Response()
            except Room.DoesNotExist:
                pass
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def user_detail(req, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(UserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def login(req):
    username = req.data.get("username")
    password = req.data.get("password")
    if not username or not password:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    user = authenticate(username=username, password=password)
    if user is not None:
        user_jwt = jwt.encode(
            {'pk': user.pk}, settings.SECRET_KEY, algorithm='HS256')
        return Response(data={'token': user_jwt})
    else:
        return Response(status=status.HTTP_401_UNAUTHORIZED)
