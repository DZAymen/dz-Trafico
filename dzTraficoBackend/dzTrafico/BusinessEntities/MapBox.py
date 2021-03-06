from rest_framework import serializers

class MapBox(object):

    def __init__(self, left, bottom, right, top):
        self.left = left
        self.bottom = bottom
        self.right = right
        self.top = top

    def get_coords(self):
        return [self.left, self.bottom, self.right, self.top]

class MapBoxSerializer(serializers.Serializer):
    left = serializers.FloatField()
    bottom = serializers.FloatField()
    right = serializers.FloatField()
    top = serializers.FloatField()

    def create(self, validated_data):
        return MapBox(
            validated_data["left"],
            validated_data["bottom"],
            validated_data["right"],
            validated_data["top"]
        )