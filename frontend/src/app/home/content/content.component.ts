import { Component, signal, SimpleChanges } from '@angular/core';
import { ChatbotService } from '../../services/chatbot.service';
import { Console } from 'console';
import { randomInt } from 'crypto';
import { HomeService } from '../../services/home.service';
import { response } from 'express';
import { ConversacionesService } from '../../services/conversaciones.service';

@Component({
  selector: 'app-content',
  standalone: true,
  imports: [],
  templateUrl: './content.component.html',
  styleUrl: './content.component.css',
})
export class ContentComponent {
  messages: { prompt: string; tipo: 'user' | 'bot' }[] = [];
  newMessage = '';
  tipo = '';
  textoReconocido = signal('');
  reconociendo: boolean = false;
  inputValue: string = '';
  idConversacion: number = 0;

  constructor(private chatBot: ChatbotService, private home: HomeService, private conversationService: ConversacionesService) {}

  /* constructor(public voiceRecognitionService: VoiceRecognitionService) {
    this.voiceRecognitionService.init();
  }*/

    ngOnInit(): void {
      //Called after the constructor, initializing input properties, and the first call to ngOnChanges.
      //Add 'implements OnInit' to the class.
      this.conversationService.selectedConversationId$.subscribe(
        id=>{
          if(id !== null){
            this.idConversacion = id;
            this.loadMessages();
          }
        }
      )

  }



  loadMessages() {
    this.home.loadMessages(this.idConversacion).subscribe(
      (messages) => {
        this.messages = messages;
        console.table(this.messages);
      },
      (error) => {
        console.error('Error loading messages:', error);
      }
    );
  }



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

  sendMessage(inputElement: HTMLInputElement) {
    const prompt = inputElement.value;

    if (localStorage.getItem('idConversacion')) {
      this.idConversacion = Number(localStorage.getItem('idConversacion'));
      if (this.idConversacion === 0) {
        this.idConversacion = this.ranmdomCodeConversation(1000, 9999);
        localStorage.setItem('idConversacion', this.idConversacion.toString());

        console.log(this.idConversacion);
      }
      console.log('EXISTE');
    }

    /*else{
      console.log("CREANDO");
      localStorage.setItem(
        'idConversacion',
        this.idConversacion.toString()
      )
    }*/
    this.messages.push({ prompt: prompt, tipo: 'user' });


     this.chatBot.sendConsulta(prompt).subscribe(
    (response) => {
      this.messages.push({ prompt: response.response, tipo: 'bot' });
      this.newMessage = '';

      // Add the message to the conversation AFTER getting the bot's response
      this.addMensajeConversation(prompt, response.response);
    },
    (error) => {
      console.error('Error sending message:', error);
    }
  );
  }

  createNewConversation() {
    this.home.createConversation(this.idConversacion).subscribe(
      (response) => {
        console.log(response);
      },
      (error) => {
        console.error('Error creating conversation:', error);
      }
    );
  }

  addMensajeConversation(userMessage: string, botMessage: string) {
    this.home
      .createMessageConversation(this.idConversacion, userMessage, 'user')
      .subscribe(
        () => {
          // Successfully added user message, now add bot message
          this.home
            .createMessageConversation(this.idConversacion, botMessage, 'bot')
            .subscribe(
              () => console.log('Mensajes agregados a la conversación'),
              (error) =>
                console.error('Error al agregar el mensaje del bot:', error)
            );
        },
        (error) => {
          console.error('Error al agregar el mensaje del usuario:', error);
        }
      );
  }

  //generar codigo de conversacion aleatorio
  ranmdomCodeConversation(min: number, max: number) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
}
