import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import { tap, catchError } from 'rxjs/operators';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

interface LoginResponse {
  token: string;
  estudiante: any;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://127.0.0.1:8000';
  private tokenKey = 'token';
  private inMemoryToken: string | null = null;

  constructor(
    private http: HttpClient,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: Object
  ) {}

  login(username: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.apiUrl}/login/`, { username, password }).pipe(
      tap((response: LoginResponse) => {
        if (response && response.token) {
          this.setToken(response.token);
        }
      }),
      catchError(error => {
        console.error('Login error', error);
        return of({ token: '', estudiante: null });
      })
    );
  }

  setToken(token: string): void {
    this.inMemoryToken = token;
    if (isPlatformBrowser(this.platformId)) {
      localStorage.setItem(this.tokenKey, token);
    }
  }

  getToken(): string | null {
    if (isPlatformBrowser(this.platformId)) {
      return localStorage.getItem(this.tokenKey) || this.inMemoryToken;
    }
    return this.inMemoryToken;
  }

  isLoggedIn(): boolean {

    return !!this.getToken();
  }

  logout(): void {
    this.inMemoryToken = null;
    if (isPlatformBrowser(this.platformId)) {
      localStorage.removeItem(this.tokenKey);
    }
    this.router.navigate(['/']);
  }
}
