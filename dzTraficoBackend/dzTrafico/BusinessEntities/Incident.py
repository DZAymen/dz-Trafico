from rest_framework import serializers

class Incident(object):

    edge_id = ""

    def __init__(self, lon, lat, time):
        self.lon = lon
        self.lat = lat
        self.time = time

    def set_edge_id(self, edge_id):
        self.edge_id = edge_id

class IncidentSerializer(serializers.Serializer):

    lon = serializers.FloatField()
    lat = serializers.FloatField()
    time = serializers.CharField()