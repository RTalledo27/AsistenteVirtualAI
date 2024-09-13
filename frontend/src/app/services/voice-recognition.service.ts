import { Injectable } from '@angular/core';

//DECLARAR VARIABLE DE RECONOCIMIENTO DE VOZ
declare var webkitSpeechRecognition: any;


@Injectable({
  providedIn: 'root'
})
export class VoiceRecognitionService {

  reconocimiento = new webkitSpeechRecognition();
  reconocimientoActivo = false;
  tempWord: string = '';
  texto:string = '';

  constructor() { }

}
