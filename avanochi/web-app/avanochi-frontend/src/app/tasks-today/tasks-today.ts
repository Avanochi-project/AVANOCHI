import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Task {
  title: string;
  done: boolean;
}

@Component({
  selector: 'app-tasks-today',
  templateUrl: './tasks-today.html',
  styleUrl: './tasks-today.css',
  standalone: true,
  imports: [CommonModule]
})
export class TasksToday {
  timerPaused = signal<boolean>(false);

  pausarTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
      this.timerPaused.set(true);
    }
  }

  reanudarTimer() {
    if (!this.timerInterval && this.jornadaInicio() && !this.jornadaFin() && this.timerPaused()) {
      this.startTimer();
      this.timerPaused.set(false);
    }
  }
  jornadaInicio = signal<string | null>(null);
  jornadaFin = signal<string | null>(null);
  timer = signal<string>('00:00:00');
  timerInterval: any = null;

  registrarInicio() {
    const ahora = new Date();
    this.jornadaInicio.set(ahora.toLocaleTimeString());
    this.jornadaFin.set(null);
    this.startTimer();
  }

  registrarFin() {
    const ahora = new Date();
    this.jornadaFin.set(ahora.toLocaleTimeString());
    this.stopTimer();
  }

  startTimer() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    const start = new Date();
    this.timerInterval = setInterval(() => {
      const now = new Date();
      const inicio = this.jornadaInicio();
      if (!inicio) return;
      const [h, m, s] = inicio.split(":");
      const startDate = new Date();
      startDate.setHours(Number(h), Number(m), Number(s), 0);
      const diff = now.getTime() - startDate.getTime();
      const hours = Math.floor(diff / 3600000);
      const minutes = Math.floor((diff % 3600000) / 60000);
      const seconds = Math.floor((diff % 60000) / 1000);
      this.timer.set(`${hours.toString().padStart(2,'0')}:${minutes.toString().padStart(2,'0')}:${seconds.toString().padStart(2,'0')}`);
    }, 1000);
  }

  stopTimer() {
    if (this.timerInterval) clearInterval(this.timerInterval);
    this.timerInterval = null;
  }
  tasks = signal<Task[]>([]);
  newTask = signal('');

  addTask() {
    const title = this.newTask().trim();
    if (title) {
      this.tasks.update(tasks => [...tasks, { title, done: false }]);
      this.newTask.set('');
    }
  }

  deleteTask(index: number) {
    this.tasks.update(tasks => tasks.filter((_, i) => i !== index));
  }

  toggleDone(index: number) {
    this.tasks.update(tasks => tasks.map((t, i) => i === index ? { ...t, done: !t.done } : t));
  }
}