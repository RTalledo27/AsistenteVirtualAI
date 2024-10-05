import { Component, signal } from '@angular/core';


@Component({
  selector: 'app-content',
  standalone: true,
  imports: [],
  templateUrl: './content.component.html',
  styleUrl: './content.component.css'
})
export class ContentComponent {

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
