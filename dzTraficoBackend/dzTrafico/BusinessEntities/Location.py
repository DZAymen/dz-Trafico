from rest_framework import serializers

class Location(object):

    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat

class LocationSerializer(serializers.Serializer):
    lng = serializers.FloatField()
    lat = serializers.FloatField()