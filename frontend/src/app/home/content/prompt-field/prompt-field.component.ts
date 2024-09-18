import { Component, signal } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatCommonModule } from '@angular/material/core';
import { ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { VoiceRecognitionService } from '../../../services/voice-recognition.service';
import { trigger } from '@angular/animations';

@Component({
  selector: 'app-prompt-field',
  standalone: true,
  imports: [MatIconModule,
    MatCommonModule,
    ReactiveFormsModule,
    MatInputModule,
  ],
  templateUrl: './prompt-field.component.html',
  styleUrl: './prompt-field.component.css',

})
export class PromptFieldComponent {

  textoReconocido = signal('');
  reconociendo: boolean = false;


 /* constructor(public voiceRecognitionService: VoiceRecognitionService) {
    this.voiceRecognitionService.init();
  }*/


  grabar() {
    /*if (this.reconociendo) {
      this.voiceRecognitionService.stop();
      this.textoReconocido.set(this.voiceRecognitionService.texto);
      console.log(this.textoReconocido());
      this.voiceRecognitionService.texto = '';
      this.reconociendo = false;
    } else {
      this.voiceRecognitionService.start();
      this.reconociendo = true;
    }*/
  }






}
