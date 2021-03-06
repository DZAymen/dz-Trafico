from rest_framework import serializers
from Location import Location, LocationSerializer

class Incident(object):

    id = 0
    def __init__(self, lon, lat, accidentTime, accidentDuration, lane):
        self.id = Incident.id
        Incident.id += 1
        self.lon = lon
        self.lat = lat
        self.position = Location(lon, lat)
        self.accidentTime = accidentTime
        self.accidentDuration = accidentDuration
        self.lane = lane

    def set_lane(self, lane_id):
        self.lane_id = lane_id

    def set_edge(self, edge):
        self.edge = edge

    def set_lane_position(self, lane_position):
        self.lane_position = lane_position

class IncidentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    position = LocationSerializer()
    accidentTime = serializers.FloatField()
    accidentDuration = serializers.FloatField()
    lane = serializers.IntegerField()

    def create(self, validated_data):
        return Incident(
            validated_data["position"]["lng"],
            validated_data["position"]["lat"],
            validated_data["accidentTime"],
            validated_data["accidentDuration"],
            validated_data["lane"]
        )