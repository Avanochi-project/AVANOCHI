import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
// ...existing code...
import { Navbar } from './navbar/navbar';
// ...existing code...

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [Navbar, RouterOutlet],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('avanochi-frontend');
}
