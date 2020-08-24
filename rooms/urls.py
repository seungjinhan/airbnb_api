from rest_framework.routers import DefaultRouter
from django.urls import path
from . import views
from . import viewsets

router = DefaultRouter()
router.register("", viewsets.RoomViewset, basename="room")

app_name = "rooms"

urlpatterns = router.urls
# [
# path("list/", views.ListRoomsView.as_view()),
# path("<int:pk>/", views.SeeRoomView.as_view())
# ]
