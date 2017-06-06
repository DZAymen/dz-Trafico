import { InMemoryDbService } from 'angular-in-memory-web-api';
export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    let departs = [
      {"id": 1, "departTime": 2012, "from":  {"lat": 36.7596737, "lng": 3.1365537},"flow": 0.4,
       "vehcileType": [
           {"id": 1, "accel": 2012, "decel": 20, "impatience": 0.4},
           {"id": 2, "accel": 2012, "decel": 20, "impatience": 0.4}
           ]
      },
      {"id": 2, "departTime": 2012, "from":  {"lat": 36.7596737, "lng": 3.1365537},"flow": 0.4,
        "vehcileType": [
            {"id": 1, "accel": 2012, "decel": 20, "impatience": 0.4},
            {"id": 2, "accel": 2012, "decel": 20, "impatience": 0.4}
            ]
      },
      {"id": 3, "departTime": 2012, "from":  {"lat": 36.7596737, "lng": 3.1365537},"flow": 0.4,
       "vehcileType": [
           {"id": 1, "accel": 2012, "decel": 20, "impatience": 0.4},
           {"id": 2, "accel": 2012, "decel": 20, "impatience": 0.4}
           ]
      },
      {"id": 4, "departTime": 2012, "from":  {"lat": 36.7596737, "lng": 3.1365537},"flow": 0.4,
        "vehcileType": [
            {"id": 1, "accel": 2012, "decel": 20, "impatience": 0.4},
            {"id": 2, "accel": 2012, "decel": 20, "impatience": 0.4}
            ]
      }
    ];
    return {departs};
  }
}
