from rest_framework import serializers

class Flow(object):

    def __init__(self, start, end, flow_value):
        self.start_edge = start
        self.end_edge = end
        self.vehicles_per_hour = flow_value


class FlowPoint(object):

    startType = "start"
    endType = "end"

    def __init__(self, lon, lat, type, value):
        self.lon = lon
        self.lat = lat
        self.type = type
        self.value = value

class FlowPointSerializer(serializers.Serializer):

    lon = serializers.FloatField()
    lat = serializers.FloatField()
    type = serializers.CharField()
    value = serializers.FloatField()