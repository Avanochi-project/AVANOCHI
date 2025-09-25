import { Component } from '@angular/core';

@Component({
  selector: 'app-tasks',
  standalone: true,
  templateUrl: './tasks.html',
  styleUrl: './tasks.css'
})
export class Tasks {
  // Aquí guardamos una lista de tareas
  tasks = [
    { title: 'Terminar presentación', done: true },
    { title: 'Revisar correos', done: false },
    { title: 'Preparar informe', done: false }
  ];
}
