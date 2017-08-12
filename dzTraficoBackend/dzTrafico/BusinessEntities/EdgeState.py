

class EdgeState(object):
    def __init__(self, edge_id, current_speed, max_speed, vsl_state, congestion_detected):
        self.edge_id = edge_id
        self.current_speed = current_speed
        self.max_speed = max_speed
        self.vsl_state = vsl_state
        self.congestion_detected = congestion_detected
