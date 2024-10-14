import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class HomeService {

  constructor(private http: HttpClient) { }

  private apiUrl = "http://127.0.0.1:8000";


  getData(){
    const headers={
      'Content-Type': 'application/json',
      'Authorization': 'Token ' + localStorage.getItem('token')
    }

    return this.http.post(`${this.apiUrl}/getData`, {headers});
  }

  //Registrar conversacion en la base de datos
  createConversation(idConversacion: number){
    const headers={
      'Content-Type': 'application/json',
      'Authorization': 'Token ' + localStorage.getItem('token')
    }

    return this.http.post(`${this.apiUrl}/conversationCreate`,{conversacion_id: idConversacion}, {headers});
  }

  createMessageConversation(idConversacion: number, mensaje: string, tipo: string){
    const headers={
      'Content-Type': 'application/json',
      'Authorization': 'Token ' + localStorage.getItem('token')
      }
      return this.http.post(`${this.apiUrl}/mensajeCreate`,{conversacion_id: idConversacion, mensaje: mensaje, tipo: tipo}, {headers});
    }


    //Obtener conversaciones
    getConversations(){
      const headers={
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
      return this.http.post<any[]>(`${this.apiUrl}/getConversations`, {headers});
    }

    loadMessages(conversacion_id: number): Observable<any[]>{
      const headers={
        'Content-Type': 'application/json',
        'Authorization': 'Token ' + localStorage.getItem('token')
      }
      return this.http.post<any[]>(`${this.apiUrl}/getMessages`,{conversacion_id}, {headers});
    }

}
