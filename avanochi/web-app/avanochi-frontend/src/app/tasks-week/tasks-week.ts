import { Component, signal } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Task {
  title: string;
  done: boolean;
}

@Component({
  selector: 'app-tasks-week',
  templateUrl: './tasks-week.html',
  styleUrl: './tasks-week.css',
  standalone: true,
  imports: [CommonModule]
})
export class TasksWeek {
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