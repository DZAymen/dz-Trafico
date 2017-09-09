import { TestBed, inject } from '@angular/core/testing';

import { RealTimeService } from './real-time.service';

describe('RealTimeService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [RealTimeService]
    });
  });

  it('should ...', inject([RealTimeService], (service: RealTimeService) => {
    expect(service).toBeTruthy();
  }));
});
