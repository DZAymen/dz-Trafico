from rest_framework import serializers

class EdgeState(object):
    def __init__(self, edge_id, current_speed, max_speed, density, vsl_state, congestion_detected):
        self.edge_id = edge_id
        self.current_speed = current_speed
        self.max_speed = max_speed
        self.density = density
        self.vsl_state = vsl_state
        self.congestion_detected = congestion_detected

class EdgeStateSerializer(serializers.Serializer):
    edge_id = serializers.CharField()
    current_speed = serializers.FloatField()
    max_speed = serializers.FloatField()
    density = serializers.FloatField()
    vsl_state = serializers.BooleanField()
    congestion_detected = serializers.BooleanField()