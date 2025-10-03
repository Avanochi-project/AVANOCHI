import { Component, signal, computed, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Task {
  id?: string;
  title: string;
  done: boolean;
  createdAt: number;
  // Fechas clave
  plannedFor?: string | null; // 'YYYY-MM-DD' (local)
  startAt?: string | null; // ISO-8601 UTC
  completedAt?: string | null; // ISO-8601 UTC
  dueAt?: number | string | null; // epoch ms, ISO-8601 UTC o 'YYYY-MM-DD' si solo fecha
  // Estado de ejecución (heredado de Task Log)
  startedAt?: number | null; // epoch ms si está en ejecución
  accumulatedMs?: number | null; // tiempo acumulado si estuvo en ejecución
}

// Helper para 'YYYY-MM-DD' en zona local
function toLocalDateString(d: Date = new Date()): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}

@Component({
  selector: 'app-tasks-today',
  templateUrl: './tasks-today.html',
  styleUrl: './tasks-today.css',
  standalone: true,
  imports: [CommonModule]
})
export class TasksToday implements OnInit {
  timerPaused = signal<boolean>(false);
  // Task list UI state
  filter = signal<'all' | 'pending' | 'done'>('all');
  search = signal<string>('');
  sort = signal<'default' | 'alpha' | 'status' | 'recent'>('default');

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
  // End-of-day banner visibility
  showEndBanner = signal<boolean>(true);
  // Jornada computed status & progress
  workStatus = computed<'idle' | 'running' | 'paused' | 'finished'>(() => {
    if (this.jornadaFin()) return 'finished';
    if (!this.jornadaInicio()) return 'idle';
    return this.timerPaused() ? 'paused' : 'running';
  });
  statusLabel = computed(() => {
    const s = this.workStatus();
    return s === 'idle' ? 'No iniciado' : s === 'running' ? 'En curso' : s === 'paused' ? 'Pausado' : 'Finalizado';
  });
  // Objetivo de jornada (8 horas por defecto)
  dayTargetSeconds = signal<number>(8 * 3600);
  // Convertir "HH:MM:SS" a segundos para el progreso
  elapsedSeconds = computed(() => {
    const t = this.timer();
    const parts = t.split(':');
    if (parts.length !== 3) return 0;
    const [h, m, s] = parts.map(n => Number(n) || 0);
    return h * 3600 + m * 60 + s;
  });
  dayProgressPercent = computed(() => {
    const target = this.dayTargetSeconds();
    if (target <= 0) return 0;
    const p = Math.round((this.elapsedSeconds() / target) * 100);
    return Math.max(0, Math.min(100, p));
  });

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
    this.showEndBanner.set(true);
    // Auto-dismiss the toast after 5 seconds
    if ((this as any)._endToastTimer) clearTimeout((this as any)._endToastTimer);
    (this as any)._endToastTimer = setTimeout(() => this.showEndBanner.set(false), 5000);
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
  dismissEndBanner() { this.showEndBanner.set(false); }
  tasks = signal<Task[]>([]);
  newTask = signal('');
  // Fechas nuevas para creación
  newTaskPlannedFor = signal<string>(toLocalDateString());
  newTaskDueAt = signal<string>('');
  // Inline editing
  editingTask = signal<Task | null>(null);
  editBuffer = signal<string>('');

  addTask() {
    const title = this.newTask().trim();
    if (title) {
      const now = Date.now();
      const planned = this.newTaskPlannedFor().trim();
      const due = this.newTaskDueAt().trim();
      const dueIso = due ? new Date(due + 'T00:00:00').toISOString() : null;
      const task: Task = {
        title,
        done: false,
        createdAt: now,
        plannedFor: planned || toLocalDateString(),
        startAt: null,
        completedAt: null,
        dueAt: dueIso
      };
      this.tasks.update(tasks => [...tasks, task]);
      this.newTask.set('');
      this.newTaskPlannedFor.set(toLocalDateString());
      this.newTaskDueAt.set('');
    }
  }

  deleteTask(index: number) {
    this.tasks.update(tasks => tasks.filter((_, i) => i !== index));
  }

  toggleDone(index: number) {
    this.tasks.update(tasks => tasks.map((t, i) => i === index ? { ...t, done: !t.done } : t));
  }

  // Derived/computed state
  totalCount = computed(() => this.tasks().length);
  doneCount = computed(() => this.tasks().filter(t => t.done).length);
  pendingCount = computed(() => this.tasks().filter(t => !t.done).length);
  newTodayCount = computed(() => {
    const start = new Date();
    start.setHours(0,0,0,0);
    const dayStart = start.getTime();
    return this.tasks().filter(t => t.createdAt >= dayStart).length;
  });
  progressPercent = computed(() => {
    const total = this.totalCount();
    return total ? Math.round((this.doneCount() / total) * 100) : 0;
  });

  // Tareas planificadas para HOY (vista previa de "Tareas de hoy")
  todayTasks = computed(() => this.tasks().filter(t => t.plannedFor === toLocalDateString()));
  todayTotalCount = computed(() => this.todayTasks().length);
  todayDoneCount = computed(() => this.todayTasks().filter(t => t.done).length);
  todayPendingCount = computed(() => this.todayTasks().filter(t => !t.done).length);
  todayProgressPercent = computed(() => {
    const total = this.todayTotalCount();
    return total ? Math.round((this.todayDoneCount() / total) * 100) : 0;
  });
  visibleTasks = computed(() => {
    const mode = this.filter();
    const term = this.search().trim().toLowerCase();
    const sortMode = this.sort();
    // Partimos solo de las tareas planificadas para HOY
    let list = this.todayTasks();
    if (mode === 'pending') list = list.filter(t => !t.done);
    if (mode === 'done') list = list.filter(t => t.done);
    if (term) list = list.filter(t => t.title.toLowerCase().includes(term));
    if (sortMode === 'alpha') {
      list = [...list].sort((a, b) => a.title.localeCompare(b.title, 'es'));
    } else if (sortMode === 'status') {
      list = [...list].sort((a, b) => Number(a.done) - Number(b.done));
    } else if (sortMode === 'recent') {
      list = [...list].sort((a, b) => b.createdAt - a.createdAt);
    } else {
      list = [...list].sort((a, b) => a.createdAt - b.createdAt);
    }
    return list;
  });

  setFilter(mode: 'all' | 'pending' | 'done') { this.filter.set(mode); }
  setSort(mode: 'default' | 'alpha' | 'status' | 'recent') { this.sort.set(mode); }

  // Helpers for filtered views
  deleteTaskByTask(task: Task) {
    this.tasks.update(list => list.filter(t => t !== task));
  }
  toggleDoneTask(task: Task) {
    const nowIso = new Date().toISOString();
    this.tasks.update(list => list.map(t => {
      if (t !== task) return t;
      const nextDone = !t.done;
      return {
        ...t,
        done: nextDone,
        completedAt: nextDone ? nowIso : null
      };
    }));
    this.persistDoneToStorage(task);
  }

  ngOnInit(): void {
    this.loadFromStorage();
  }

  private loadFromStorage() {
    try {
      const raw = localStorage.getItem('tasklog.tasks');
      if (!raw) return;
      const arr = JSON.parse(raw) as any[];
      const mapped: Task[] = arr.map(t => ({
        id: t.id,
        title: t.name || t.title,
        done: !!t.done,
        createdAt: typeof t.createdAt === 'number' ? t.createdAt : Date.now(),
        plannedFor: t.plannedFor || null,
        startAt: t.start_at || t.startAt || null,
        startedAt: typeof t.startedAt === 'number' ? t.startedAt : null,
        accumulatedMs: typeof t.accumulatedMs === 'number' ? t.accumulatedMs : null,
        completedAt: t.completed_at || t.completedAt || null,
        dueAt: t.dueAt != null ? t.dueAt : (t.due_at || null),
      }));
      this.tasks.set(mapped);
    } catch {}
  }

  private persistDoneToStorage(task: Task) {
    try {
      const raw = localStorage.getItem('tasklog.tasks');
      if (!raw) return;
      const arr = JSON.parse(raw) as any[];
      const id = task.id;
      const title = task.title;
      for (const t of arr) {
        if ((id && t.id === id) || (!id && (t.name === title || t.title === title))) {
          t.done = !t.done; // we already flipped in UI; mirror change
          if (t.done) t.completedAt = new Date().toISOString(); else t.completedAt = null;
          break;
        }
      }
      localStorage.setItem('tasklog.tasks', JSON.stringify(arr));
    } catch {}
  }

  // Bulk / cleanup
  clearCompleted() {
    this.tasks.update(tasks => tasks.filter(t => !t.done));
  }
  markAllDone() {
    this.tasks.update(list => list.map(t => t.done ? t : ({ ...t, done: true })));
  }
  clearAllTasks() {
    if (confirm('¿Eliminar todas las tareas? Esta acción no se puede deshacer.')) {
      this.tasks.set([]);
    }
  }

  // Reorder
  moveTask(task: Task, dir: 'up' | 'down') {
    // Operar sobre el orden visible actual (filtro/búsqueda aplicados) para evitar confusiones
    const visible = this.visibleTasks();
    const vIdx = visible.indexOf(task);
    if (vIdx === -1) return;
    const targetVIdx = dir === 'up' ? vIdx - 1 : vIdx + 1;
    if (targetVIdx < 0 || targetVIdx >= visible.length) return;
    const neighbor = visible[targetVIdx];

    this.tasks.update(list => {
      const iA = list.indexOf(task);
      const iB = list.indexOf(neighbor);
      if (iA === -1 || iB === -1) return list;
      const copy = [...list];
      [copy[iA], copy[iB]] = [copy[iB], copy[iA]];
      // Ajustar createdAt para preservar el orden en modo "default"
      const now = Date.now();
      copy[iA] = { ...copy[iA], createdAt: now };
      copy[iB] = { ...copy[iB], createdAt: now - 1 };
      return copy;
    });
  }


  // Inline editing
  startEditing(task: Task) {
    this.editingTask.set(task);
    this.editBuffer.set(task.title);
  }
  saveEditing(task: Task) {
    const value = this.editBuffer().trim();
    if (!value) return;
    this.tasks.update(list => list.map(t => t === task ? { ...t, title: value } : t));
    this.editingTask.set(null);
    this.editBuffer.set('');
  }
  cancelEditing() {
    this.editingTask.set(null);
    this.editBuffer.set('');
  }

  // Estado de la tarea para iconos en vista previa
  taskStatus(t: Task): 'active' | 'paused' | 'pending' | 'done' {
    if (t.done) return 'done';
    if (t.startedAt != null) return 'active';
    const acc = t.accumulatedMs || 0;
    return acc > 0 ? 'paused' : 'pending';
  }

  statusIcon(t: Task): string {
    const st = this.taskStatus(t);
    if (st === 'active') return '▶️';
    if (st === 'paused') return '⏸️';
    if (st === 'pending') return '🕒';
    return '';
  }
}