from rest_framework import serializers
from Location import Location, LocationSerializer

class Flow(object):
    end_depart_time = 10000
    # via_edges = "26322664#2"
    via_edges = ""
    def __init__(self, start, end, depart_time, flow_value):
        self.start_edge = start
        self.end_edge = end
        self.depart_time = depart_time
        self.vehicles_per_hour = flow_value

class InFlowPoint(object):

    id = 0
    def __init__(self, lon, lat, departTime, flow, outs):
        self.id = InFlowPoint.id
        InFlowPoint.id += 1
        self.lon = lon
        self.lat = lat
        self.position = Location(lon, lat)
        self.departTime = departTime
        self.flow = flow
        self.left_flow = flow
        self.outs = outs

    def get_left_flow(self, percentage):
        flow = percentage * self.left_flow
        self.left_flow -= flow
        return flow

    def reset_flow_value(self):
        self.left_flow = self.flow

class OutSerializer(serializers.Serializer):
    outIndex = serializers.IntegerField()

class InFlowPointSerializer(serializers.Serializer):

    id = serializers.CharField(required=False)
    position = LocationSerializer()
    departTime = serializers.FloatField()
    flow = serializers.FloatField()
    outs = serializers.ListField(
        child = serializers.IntegerField(min_value=0, max_value=1000)
    )

    def create(self, validated_data):
        return InFlowPoint(
            validated_data["position"]["lng"],
            validated_data["position"]["lat"],
            validated_data["departTime"],
            validated_data["flow"],
            validated_data["outs"]
        )

class OutFlowPoint(object):
    id = 0
    def __init__(self, lon, lat, percentage):
        self.id = OutFlowPoint.id
        OutFlowPoint.id += 1
        self.lon = lon
        self.lat = lat
        self.position = Location(lon, lat)
        self.percentage = percentage

class OutFlowPointSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=False)
    position = LocationSerializer()
    percentage = serializers.FloatField(required=False)

    def create(self, validated_data):
        return OutFlowPoint(
            validated_data["position"]["lng"],
            validated_data["position"]["lat"],
            validated_data["percentage"]
        )
