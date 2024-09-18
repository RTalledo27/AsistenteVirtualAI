import { Component } from '@angular/core';
import { NavloginComponent } from "./navlogin/navlogin.component";
import { FormcontainerComponent } from "./formcontainer/formcontainer.component";

@Component({
  selector: 'app-form',
  standalone: true,
  imports: [NavloginComponent, FormcontainerComponent],
  templateUrl: './form.component.html',
  styleUrl: './form.component.css'
})
export class FormComponent {

}
