from rest_framework import serializers

class Incident(object):

    lanes = []

    def __init__(self, lon, lat, time):
        self.lon = lon
        self.lat = lat
        self.time = time

    def set_lanes(self, lanes):
        self.lanes = lanes

class IncidentSerializer(serializers.Serializer):

    lon = serializers.FloatField()
    lat = serializers.FloatField()
    time = serializers.CharField()