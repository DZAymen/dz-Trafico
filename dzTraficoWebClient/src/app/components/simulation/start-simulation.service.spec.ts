import { TestBed, inject } from '@angular/core/testing';

import { StartSimulationService } from './start-simulation.service';

describe('StartSimulationService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [StartSimulationService]
    });
  });

  it('should ...', inject([StartSimulationService], (service: StartSimulationService) => {
    expect(service).toBeTruthy();
  }));
});
