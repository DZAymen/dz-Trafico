from rest_framework import serializers

class Incident(object):

    def __init__(self, lon, lat, time):
        self.lon = lon
        self.lat = lat
        self.time = time

class IncidentSerializer(serializers.Serializer):

    lon = serializers.FloatField()
    lat = serializers.FloatField()
    time = serializers.CharField()