import { Component, signal } from '@angular/core';
// import { RouterOutlet } from '@angular/router';
// import { Tasks } from './tasks/tasks';
import { Navbar } from './navbar/navbar';
import { TasksToday } from './tasks-today/tasks-today';
import { TasksYesterday } from './tasks-yesterday/tasks-yesterday';
import { TasksWeek } from './tasks-week/tasks-week';

@Component({
  selector: 'app-root',
  imports: [Navbar, TasksToday, TasksYesterday, TasksWeek],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('avanochi-frontend');
}
