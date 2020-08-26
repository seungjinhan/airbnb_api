from rest_framework import serializers
from users.serializers import RelatedUserSerializer
from .models import Room


class ReadRoomSerializer(serializers.ModelSerializer):

    user = RelatedUserSerializer()

    class Meta:
        model = Room
        exclude = ("modified",)


class WriteRoomSerializer(serializers.Serializer):

    class Meta:
        model = Room
        exclude = ("user", "modified", "created")

    def validate(self, data):
        if self.instance:
            check_in = data.get('check_in', self.instance.check_in)
            check_out = data.get('check_out', self.instance.check_out)
        else:
            check_in = data.get('check_in')
            check_out = data.get('check_out')
        if check_in == check_out or check_in > check_out:
            raise serializers.ValidationError(
                "Not enough time between check in and check out")
        return data


class BigRoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ("__all__")
