import { animate, state, style, transition, trigger } from '@angular/animations';
import { Component, signal } from '@angular/core';
import { AuthService } from '../../services/auth.service';
import { HomeService } from '../../services/home.service';
import { ProfileComponent } from "./profile/profile.component";
import { NgIf } from '@angular/common';


@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [ProfileComponent,NgIf],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
  animations:[

  ]


})
export class NavbarComponent {

  Estudiante: any;
  profileIsVisible = false;


  constructor(private authService: AuthService, private homeService: HomeService) {
  }

  //abrir y cerrar el profile
  toggleProfile() {
    this.profileIsVisible = !this.profileIsVisible;
  }

  closeProfile() {
    this.profileIsVisible = false;
  }


  ngOnInit() {

    this.getDataEstudiante();
  }

  getDataEstudiante(){
    this.homeService.getData().pipe().subscribe(
      data => {
        this.Estudiante = data;
        console.log(this.Estudiante);
      }
    )
    }


   logout() {
    this.authService.logout();
    console.log('Token', this.authService.getToken());
  }


}
