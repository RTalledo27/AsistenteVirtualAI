import { Component, Input, Output,EventEmitter } from '@angular/core';


@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [],
  templateUrl: './profile.component.html',
  styleUrl: './profile.component.css'
})
export class ProfileComponent {

  @Input() Estudiante: any;
  @Input() isOpen = false;
  @Output() close = new EventEmitter<void>();


  onClose(): void {
    this.close.emit();
  }
}


