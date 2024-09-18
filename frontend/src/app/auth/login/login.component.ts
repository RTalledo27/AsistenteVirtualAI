import { animate, style, transition, trigger } from '@angular/animations';
import { Component } from '@angular/core';
import { BackgroundComponent } from './background/background.component';
import { FormComponent } from './form/form.component';
@Component({
  selector: 'app-login',
  standalone: true,
  imports: [BackgroundComponent, FormComponent],
  templateUrl: './login.component.html',
  styleUrl: './login.component.css',
  animations: [
    trigger('load', [
      transition(':enter', [
        style({ opacity: 0 }),
        animate(500, style({ opacity: 1 }))
      ]),
      transition(':leave', [
        animate(500, style({ opacity: 0 }))
      ])
    ])
  ]
})
export class LoginComponent {

}
