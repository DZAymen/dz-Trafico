import { TestBed, inject } from '@angular/core/testing';

import { DepartPointService } from './depart-point.service';

describe('DepartPointService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [DepartPointService]
    });
  });

  it('should ...', inject([DepartPointService], (service: DepartPointService) => {
    expect(service).toBeTruthy();
  }));
});
