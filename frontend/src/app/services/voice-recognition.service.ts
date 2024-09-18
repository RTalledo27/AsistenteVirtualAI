import { Injectable } from '@angular/core';

//DECLARAR VARIABLE DE RECONOCIMIENTO DE VOZ
declare var webkitSpeechRecognition: any  ;

@Injectable({
  providedIn: 'root',
})
export class VoiceRecognitionService {
  webkitSpeechRecognition = 0;
    reconocimiento = new webkitSpeechRecognition();
  reconocimientoPausa = false;
  tempWord: string = '';
  texto: string = '';

  constructor() {
    this.reconocimiento.interimResults = true;
    this.reconocimiento.lang = 'es-ES';
  }

  init() {
    this.reconocimiento.addEventListener('result', (event: any) => {
      const transcripcion = Array.from(event.results)
        .map((result: any) => result[0])
        .map((result: any) => result.transcript)
        .join('');
      this.tempWord = transcripcion;
    });
  }

  start() {
    this.reconocimientoPausa = false;
    this.reconocimiento.start();
    console.log('Reconocimiento de voz iniciado');

    this.reconocimiento.addEventListener('end', () => {
      if (this.reconocimientoPausa) {
        this.reconocimiento.stop();
        console.log('Reconocimiento de voz detenido');
      }else{
        this.wordConcat();
        this.start();
      }
    });
  }


  stop() {
    this.reconocimientoPausa = true;
    this.wordConcat();  
    this.reconocimiento.stop();
    console.log('Reconocimiento de voz detenido');
  }

  wordConcat() {
    this.texto = `${this.texto} ${this.tempWord}.`;
    this.tempWord = '';
  }
}
