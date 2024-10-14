import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ConversacionesService {

  private selectConversation = new BehaviorSubject<number|null>(null);
  selectedConversationId$ = this.selectConversation.asObservable();


  constructor() { }


  setSelectConversation(id:number) {
    this.selectConversation.next(id);
  }

  getSelectConversation() {
    return this.selectConversation.asObservable();
  }

}
