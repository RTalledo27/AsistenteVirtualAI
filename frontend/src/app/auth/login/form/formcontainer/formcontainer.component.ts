import { AuthService } from './../../../../services/auth.service';
import { Component, signal } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { HttpClientModule } from '@angular/common/http'; // Import HttpClientModule
import { response } from 'express';
import { error } from 'console';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-formcontainer',
  standalone: true,
  imports: [CommonModule,ReactiveFormsModule], // Add HttpClientModule here
  templateUrl: './formcontainer.component.html',
  styleUrls: ['./formcontainer.component.css'] // Corrected styleUrl to styleUrls
})
export class FormcontainerComponent {
  loginForm: FormGroup;

  constructor(
    private formBuilder:FormBuilder,
    private authService: AuthService,
    private router:Router,
  ){
    this.loginForm = this.formBuilder.group({
      username:['',[Validators.required]],
      password:['',[Validators.required]]
    });
  }

  onSubmit(){
    if(this.loginForm.valid){
      const {username,password}= this.loginForm.value;
      this.authService.login(username,password).subscribe(
        response=>{
          console.log('login exitoso',response);

          this.router.navigate(['/home']);
        },
        error=>{
          console.error('Error;',error)
        }
      )
    }
  }

}
