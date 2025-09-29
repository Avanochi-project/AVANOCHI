import { Component, signal } from '@angular/core';
// import { RouterOutlet } from '@angular/router';
// ...existing code...
import { Navbar } from './navbar/navbar';
import { TasksToday } from './tasks-today/tasks-today';
// ...existing code...

@Component({
  selector: 'app-root',
  imports: [Navbar, TasksToday],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('avanochi-frontend');
}
