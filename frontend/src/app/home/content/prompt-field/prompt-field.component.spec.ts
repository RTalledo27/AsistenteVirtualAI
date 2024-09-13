import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PromptFieldComponent } from './prompt-field.component';

describe('PromptFieldComponent', () => {
  let component: PromptFieldComponent;
  let fixture: ComponentFixture<PromptFieldComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PromptFieldComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PromptFieldComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
