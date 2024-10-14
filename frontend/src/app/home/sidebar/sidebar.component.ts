import { Component } from '@angular/core';
import { CommonModule, NgClass } from '@angular/common';
import { NgFor } from '@angular/common';
import { HomeService } from '../../services/home.service';
import { ConversacionesService } from '../../services/conversaciones.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [NgFor, NgClass,CommonModule],
  templateUrl: './sidebar.component.html',
  styleUrl: './sidebar.component.css'
})
export class SidebarComponent {

  constructor(private home: HomeService, private conversationService: ConversacionesService){}

  messages: any;


  conversations = this.home.getConversations();


  loadConversation(conversacion_id: number)
  {
    this.conversationService.setSelectConversation(conversacion_id);
    localStorage.setItem('idConversacion', conversacion_id.toString());
  }




}
