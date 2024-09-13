import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PromptContentComponent } from './prompt-content.component';

describe('PromptContentComponent', () => {
  let component: PromptContentComponent;
  let fixture: ComponentFixture<PromptContentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PromptContentComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(PromptContentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
