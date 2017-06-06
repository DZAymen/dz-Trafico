import { TestBed, inject } from '@angular/core/testing';

import { OsmService } from './osm.service';

describe('OsmService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [OsmService]
    });
  });

  it('should ...', inject([OsmService], (service: OsmService) => {
    expect(service).toBeTruthy();
  }));
});
