import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

interface ChatbotResponse {
  response: string;
}

@Injectable({
  providedIn: 'root'
})
export class ChatbotService {
  private apiUrl = 'http://127.0.0.1:8000';
  constructor(private http: HttpClient) { }

  sendConsulta(prompt: string): Observable<ChatbotResponse> {
    const headers ={
      'Content-Type': 'application/json',
      'Authorization': 'Token ' + this.getAuthToken()
    };
    return this.http.post<ChatbotResponse>(`${this.apiUrl}/chatbot/`, { prompt }, { headers });

  }

  getAuthToken(): string {
    const token = localStorage.getItem('token');
    return token ? token : '';
  }





}
