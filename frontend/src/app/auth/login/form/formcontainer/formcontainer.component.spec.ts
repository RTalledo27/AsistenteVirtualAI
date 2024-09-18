import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FormcontainerComponent } from './formcontainer.component';

describe('FormcontainerComponent', () => {
  let component: FormcontainerComponent;
  let fixture: ComponentFixture<FormcontainerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FormcontainerComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(FormcontainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
