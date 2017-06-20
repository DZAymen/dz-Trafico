import { TestBed, inject } from '@angular/core/testing';

import { VehicleDistribService } from './vehicle-distrib.service';

describe('VehicleDistribService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [VehicleDistribService]
    });
  });

  it('should ...', inject([VehicleDistribService], (service: VehicleDistribService) => {
    expect(service).toBeTruthy();
  }));
});
