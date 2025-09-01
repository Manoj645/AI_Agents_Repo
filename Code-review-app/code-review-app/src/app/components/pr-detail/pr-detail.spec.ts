import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PrDetail } from './pr-detail';

describe('PrDetail', () => {
  let component: PrDetail;
  let fixture: ComponentFixture<PrDetail>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PrDetail]
    })
    .compileComponents();

    fixture = TestBed.createComponent(PrDetail);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
