import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PromptResultComponent } from './prompt-result.component';

describe('PromptResultComponent', () => {
  let component: PromptResultComponent;
  let fixture: ComponentFixture<PromptResultComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PromptResultComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PromptResultComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
