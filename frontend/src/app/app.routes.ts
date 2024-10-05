import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './auth/login/login.component';
import { RegisterComponent } from './auth/register/register.component';
import { authGuard } from './guards/auth.guard';
import { NotFound404Component } from './not-found404/not-found404.component';


export const routes: Routes = [
    {
    path: '',
    component: LoginComponent,
    },
    {
      path: 'register',
      component: RegisterComponent
    },
    {
      path: 'home',
      component: HomeComponent,
      canActivate: [authGuard]
    },
    {
      //404 redirect
      path: '**',
      component: NotFound404Component
    },

];
