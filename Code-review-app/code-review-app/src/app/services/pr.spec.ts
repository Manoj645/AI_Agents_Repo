import { TestBed } from '@angular/core/testing';

import { Pr } from './pr';

describe('Pr', () => {
  let service: Pr;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Pr);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
