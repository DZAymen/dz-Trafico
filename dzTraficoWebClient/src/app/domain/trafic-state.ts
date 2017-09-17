import { Polyline } from './polyline';

export class TraficState {
  edge_id: string;
  edge_coords: Polyline;
  current_speed: number;
  max_speed: number;
  density: number;
  vsl_state: boolean;
  congestion_detected: boolean;
}
