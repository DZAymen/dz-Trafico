from rest_framework import serializers
from Location import Location, LocationSerializer

class Incident(object):

    lanes = []

    def __init__(self, lon, lat, time):
        self.lon = lon
        self.lat = lat
        self.time = time

    def set_lanes(self, lanes):
        self.lanes = lanes

class IncidentSerializer(serializers.Serializer):
    location = LocationSerializer()
    time = serializers.CharField()