import { animate, state, style, transition, trigger } from '@angular/animations';
import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';


@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  animations:[

  ]


})
export class NavbarComponent {


  constructor(private authService: AuthService) {
  }

   logout() {
    this.authService.logout();
    console.log('Token', this.authService.getToken());
  }

}
