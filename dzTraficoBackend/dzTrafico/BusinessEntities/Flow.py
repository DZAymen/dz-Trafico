from rest_framework import serializers
from Location import Location, LocationSerializer

class Flow(object):
    end_depart_time = 10000
    def __init__(self, start, end, depart_time, flow_value):
        self.start_edge = start
        self.end_edge = end
        self.depart_time = depart_time
        self.vehicles_per_hour = flow_value

class InFlowPoint(object):

    id = 0
    def __init__(self, lon, lat, depart_time, value):
        self.id = InFlowPoint.id
        InFlowPoint.id += 1
        self.lon = lon
        self.lat = lat
        self.depart_time = depart_time
        self.value = value

class InFlowPointSerializer(serializers.Serializer):

    id = serializers.CharField(required=False)
    position = LocationSerializer()
    departTime = serializers.FloatField()
    flow = serializers.FloatField()

    def create(self, validated_data):
        return InFlowPoint(
            validated_data["position"]["lng"],
            validated_data["position"]["lat"],
            validated_data["departTime"],
            validated_data["flow"]
        )

class OutFlowPoint(object):
    id = 0
    def __init__(self, lon, lat, value):
        self.id = OutFlowPoint.id
        OutFlowPoint.id += 1
        self.lon = lon
        self.lat = lat
        self.value = value

class OutFlowPointSerializer(serializers.Serializer):
    position = LocationSerializer()
    flow = serializers.FloatField(required=False)

    def create(self, validated_data):
        return OutFlowPoint(
            validated_data["position"]["lng"],
            validated_data["position"]["lat"],
            2000
        )