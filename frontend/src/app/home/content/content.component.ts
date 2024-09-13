import { Component } from '@angular/core';
import { PromptContentComponent } from './prompt-content/prompt-content.component';
import { PromptFieldComponent } from './prompt-field/prompt-field.component';
import { PromptResultComponent } from './prompt-result/prompt-result.component';

@Component({
  selector: 'app-content',
  standalone: true,
  imports: [PromptContentComponent,
    PromptFieldComponent,
    PromptResultComponent,],
  templateUrl: './content.component.html',
  styleUrl: './content.component.css'
})
export class ContentComponent {

}
