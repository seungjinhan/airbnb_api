from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from .models import User
from .serializers import ReadUserSerializer


class MeView(APIView):

    def get(self, req):
        if req.user.is_authenticated:
            return Response(ReadUserSerializer(req.user).data)

    def put(self, req):
        pass


@api_view(["GET"])
def user_detail(req, pk):
    try:
        user = User.objects.get(pk=pk)
        return Response(ReadUserSerializer(user).data)
    except User.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
