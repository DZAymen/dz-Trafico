import { InMemoryDbService } from 'angular-in-memory-web-api';
export class TrafficFlowData implements InMemoryDbService {
  createDb() {
    let departs= [
      {"id": 1, "departTime": 2012, "position":  {"lat": 36.7596737, "lng": 3.1365537},"flow": 0.4},
      {"id": 2, "departTime": 2012, "position":  {"lat": 36.7596737, "lng": 3.1365537},"flow": 0.4},
      {"id": 3, "departTime": 2012, "position":  {"lat": 36.7596737, "lng": 3.1365537},"flow": 0.4},
      {"id": 4, "departTime": 2012, "position":  {"lat": 36.7596737, "lng": 3.1365537},"flow": 0.4}
    ];
    let arrivals= [
      {"id": 1, "position":  {"lat": 36.7596737, "lng": 3.1365537}},
      {"id": 2, "position":  {"lat": 36.7596737, "lng": 3.1365537}}
    ];
    let accidents= [

    ];

    let vehicleTypes=[
      {"id": 1, "accel": 2012, "decel": 20, "impatience": 0.4, "sigma": 0.2, "minGap":2,"tau":3, "maxSpeed": 80},
      {"id": 2, "accel": 2012, "decel": 40, "impatience": 0.6, "sigma": 0.2, "minGap":2,"tau":3, "maxSpeed": 80},
      {"id": 3, "accel": 2012, "decel": 60, "impatience": 0.8, "sigma": 0.2, "minGap":2,"tau":3, "maxSpeed": 80},
      {"id": 4, "accel": 2012, "decel": 80, "impatience": 0.1, "sigma": 0.2, "minGap":2,"tau":3, "maxSpeed": 80}
    ];

    let vehpourcentage=[

    ]
    return {departs, arrivals, accidents, vehicleTypes, vehpourcentage};
  }
}
