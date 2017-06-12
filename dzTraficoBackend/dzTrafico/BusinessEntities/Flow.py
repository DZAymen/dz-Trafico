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

class InFlowPoint(object):

    def __init__(self, lon, lat, departTime, value):
        self.lon = lon
        self.lat = lat
        self.departTime = departTime
        self.value = value

class InFlowPointSerializer(serializers.Serializer):

    lon = serializers.FloatField()
    lat = serializers.FloatField()
    departTime = serializers.CharField()
    value = serializers.FloatField()

class OutFlowPoint(object):

    def __init__(self, lon, lat, value):
        self.lon = lon
        self.lat = lat
        self.value = value

class OutFlowPointSerializer(serializers.Serializer):

    lon = serializers.FloatField()
    lat = serializers.FloatField()
    value = serializers.FloatField()