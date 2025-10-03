import { Component, OnDestroy, OnInit, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-task-log',
  standalone: true,
  templateUrl: './task-log.html',
  styleUrl: './task-log.css',
  imports: [CommonModule, FormsModule]
})
export class TaskLog implements OnInit, OnDestroy {
  // Simple model for a task in the log
  tasks: Array<{
    id: string;
    name: string;
    expectedDurationMs: number;
    startedAt: number | null; // epoch ms when started (if running)
    accumulatedMs: number; // time accumulated while previously running
    done?: boolean;
    createdAt: number; // epoch ms when the task was created/scheduled
    description?: string;
    tags?: string[];
    priority?: 'low' | 'medium' | 'high';
    dueAt?: number; // epoch ms
    plannedFor?: string; // 'YYYY-MM-DD' local date
    completedAt?: string; // ISO when finished
    subtasks?: Array<{ id: string; text: string; done: boolean }>;
    notes?: string;
    openNotes?: boolean; // ui state
    newSubtaskText?: string; // ui state
  }> = [
    // Hoy
    {
      id: cryptoRandomId(),
      name: 'Diseñar UI de registro automático',
      expectedDurationMs: 25 * 60 * 1000,
      startedAt: Date.now() - (7 * 60 + 18) * 1000, // 7m 18s
      accumulatedMs: 0,
      createdAt: Date.now(),
  plannedFor: toLocalDateString(),
      description: 'Pantalla principal para registrar varias tareas con contador y progreso.',
      tags: ['UI', 'Frontend'],
      priority: 'high',
      dueAt: Date.now() + 2 * 24 * 60 * 60 * 1000, // +2 días
      subtasks: [
        { id: cryptoRandomId(), text: 'Bocetar estructura de tarjeta', done: true },
        { id: cryptoRandomId(), text: 'Implementar barra de progreso', done: true },
        { id: cryptoRandomId(), text: 'Añadir pestañas (Ayer/Hoy/Semana)', done: true },
        { id: cryptoRandomId(), text: 'Checklist por tarea', done: false },
      ],
      notes: 'Ajustar contrastes y tamaños en móvil.',
    },
    {
      id: cryptoRandomId(),
      name: 'Escribir casos de prueba',
      expectedDurationMs: 40 * 60 * 1000,
      startedAt: null,
      accumulatedMs: 0,
      createdAt: Date.now(),
  plannedFor: toLocalDateString(),
      description: 'Definir pruebas de interacción para el componente de tareas.',
      tags: ['Testing'],
      priority: 'medium',
      dueAt: Date.now() + 4 * 24 * 60 * 60 * 1000,
      subtasks: [
        { id: cryptoRandomId(), text: 'Pruebas de iniciar/pausar/finalizar', done: true },
        { id: cryptoRandomId(), text: 'Pruebas de filtrado por fecha', done: false },
      ],
    },
    // Ayer (una pendiente y otra finalizada)
    {
      id: cryptoRandomId(),
      name: 'Refinar estilos de la barra de progreso',
      expectedDurationMs: 30 * 60 * 1000,
      startedAt: null,
      accumulatedMs: 12 * 60 * 1000, // 12m ya invertidos
  createdAt: (() => { const now = Date.now(); const startToday = startOfDayTs(now); return startToday - 12 * 60 * 60 * 1000; })(),
  plannedFor: toLocalDateString(new Date(startOfDayTs(Date.now()) - 24*60*60*1000)),
      description: 'Ajustar gradientes y transiciones para mayor claridad visual.',
      tags: ['UI', 'CSS'],
      priority: 'low',
      dueAt: Date.now() + 24 * 60 * 60 * 1000,
      subtasks: [
        { id: cryptoRandomId(), text: 'Revisar colores de estado', done: false },
      ],
    },
    {
      id: cryptoRandomId(),
      name: 'Documentar decisiones de diseño',
      expectedDurationMs: 20 * 60 * 1000,
      startedAt: null,
      accumulatedMs: 20 * 60 * 1000,
      done: true,
  createdAt: (() => { const now = Date.now(); const startToday = startOfDayTs(now); return startToday - 10 * 60 * 60 * 1000; })(),
  plannedFor: toLocalDateString(new Date(startOfDayTs(Date.now()) - 24*60*60*1000)),
      description: 'Sección en README con razones de arquitectura y UX.',
      tags: ['Docs'],
      priority: 'medium',
      dueAt: Date.now() + 3 * 24 * 60 * 60 * 1000,
      subtasks: [
        { id: cryptoRandomId(), text: 'Anotar decisiones en README', done: true },
      ],
    },
    // Semana (más generales, no iguales a hoy)
    {
      id: cryptoRandomId(),
      name: 'Revisión de accesibilidad (a11y)',
      expectedDurationMs: 60 * 60 * 1000,
      startedAt: null,
      accumulatedMs: 0,
  createdAt: (() => { const now = Date.now(); const startWeek = startOfWeekMondayTs(now); return startWeek + 1 * 24 * 60 * 60 * 1000; })(), // martes
  plannedFor: toLocalDateString(new Date(startOfWeekMondayTs(Date.now()) + 1 * 24*60*60*1000)),
      description: 'Pasar checklist de contraste, focus y labels.',
      tags: ['A11Y', 'QA'],
      priority: 'high',
      dueAt: (() => { const now = Date.now(); const startWeek = startOfWeekMondayTs(now); return startWeek + 5 * 24 * 60 * 60 * 1000; })(), // viernes
      subtasks: [
        { id: cryptoRandomId(), text: 'Revisar contraste', done: false },
        { id: cryptoRandomId(), text: 'Comprobar navegación por teclado', done: false },
      ],
    },
    {
      id: cryptoRandomId(),
      name: 'Planificar backlog de mejoras',
      expectedDurationMs: 45 * 60 * 1000,
      startedAt: null,
      accumulatedMs: 8 * 60 * 1000,
  createdAt: (() => { const now = Date.now(); const startWeek = startOfWeekMondayTs(now); return startWeek + 2 * 24 * 60 * 60 * 1000; })(), // miércoles
  plannedFor: toLocalDateString(new Date(startOfWeekMondayTs(Date.now()) + 2 * 24*60*60*1000)),
      description: 'Recopilar feedback y priorizar tareas de la semana siguiente.',
      tags: ['Planning'],
      priority: 'low',
      dueAt: (() => { const now = Date.now(); const startWeek = startOfWeekMondayTs(now); return startWeek + 6 * 24 * 60 * 60 * 1000; })(), // sábado
      subtasks: [
        { id: cryptoRandomId(), text: 'Recopilar ideas de usuarios', done: false },
      ],
    },
  ];

  // New task form fields
  newTaskName = '';
  newTaskMinutes: number | null = 25;
  newTaskDescription = '';
  newTaskPriority: 'low' | 'medium' | 'high' = 'medium';
  newTaskTags = '';
  todayStr: string = toLocalDateString();
  newTaskPlannedFor: string = toLocalDateString();
  newTaskDueDate: string = '';
  showNewTask = false;

  // A ticking signal that triggers change detection in zoneless mode
  nowMs = signal<number>(Date.now());
  private timerId: any;

  // Search
  searchTerm = '';
  filterPriority: 'all' | 'low' | 'medium' | 'high' = 'all';
  filterStatus: 'all' | 'running' | 'paused' | 'done' = 'all';
  compactMode = false;

  // Drag & Drop state for subtasks
  private dragTaskId: string | null = null;
  private dragFromIndex: number | null = null;
  private dragOverIndex: number | null = null;

  ngOnInit(): void {
    // Load from localStorage if present
    try {
      const raw = localStorage.getItem('tasklog.tasks');
      if (raw) {
        const arr = JSON.parse(raw);
        if (Array.isArray(arr)) {
          this.tasks = arr;
        }
      } else {
        // seed initial tasks into storage
        this.saveToStorage();
      }
    } catch {}
    this.timerId = setInterval(() => {
      this.nowMs.set(Date.now());
    }, 250);
  }

  ngOnDestroy(): void {
    if (this.timerId) clearInterval(this.timerId);
  }

  // Actions
  addTask(): void {
    const name = (this.newTaskName || '').trim();
    const mins = Math.max(1, Math.min(24 * 60, Math.floor(this.newTaskMinutes ?? 25)));
    if (!name) return;
    const tags = (this.newTaskTags || '')
      .split(',')
      .map(t => t.trim())
      .filter(Boolean);
    const plannedFor = (this.newTaskPlannedFor || '').trim() || toLocalDateString();
    const dueDate = (this.newTaskDueDate || '').trim();
    const dueAt = dueDate ? new Date(dueDate + 'T00:00:00').getTime() : undefined;
    this.tasks.unshift({
      id: cryptoRandomId(),
      name,
      expectedDurationMs: mins * 60 * 1000,
      startedAt: null,
      accumulatedMs: 0,
      createdAt: Date.now(),
      plannedFor,
      description: (this.newTaskDescription || '').trim(),
      tags,
      priority: this.newTaskPriority,
      dueAt,
      subtasks: [],
      notes: '',
    });
    this.saveToStorage();
    this.newTaskName = '';
    this.newTaskMinutes = 25;
    this.newTaskDescription = '';
    this.newTaskPriority = 'medium';
    this.newTaskTags = '';
    this.newTaskPlannedFor = toLocalDateString();
    this.newTaskDueDate = '';
    this.showNewTask = false; // collapse after adding
  }

  startTask(t: any): void {
    if (t.done) return;
    if (t.startedAt == null) {
      t.startedAt = Date.now();
    }
    this.saveToStorage();
  }

  pauseTask(t: any): void {
    if (t.startedAt != null) {
      t.accumulatedMs += Date.now() - t.startedAt;
      t.startedAt = null;
    }
    this.saveToStorage();
  }

  finishTask(t: any): void {
    if (t.startedAt != null) {
      this.pauseTask(t);
    }
    t.done = true;
    t.completedAt = new Date().toISOString();
    this.saveToStorage();
  }

  updateExpected(t: any, minutes: number): void {
    const mins = Math.max(1, Math.min(24 * 60, Math.floor(minutes || 0)));
    t.expectedDurationMs = mins * 60 * 1000;
    this.saveToStorage();
  }

  // Delete
  deleteTask(t: any): void {
    const id = t.id;
    const idx = this.tasks.findIndex(x => x.id === id);
    if (idx >= 0) this.tasks.splice(idx, 1);
    this.saveToStorage();
  }

  // Metrics
  isRunning(t: any): boolean {
    return t.startedAt != null && !t.done;
  }

  elapsedMs(t: any): number {
    const base = t.accumulatedMs || 0;
    const extra = t.startedAt != null ? this.nowMs() - t.startedAt : 0;
    return Math.max(0, base + extra);
  }

  progressPct(t: any): number {
    if (!t.expectedDurationMs) return 0;
    const pct = (this.elapsedMs(t) / t.expectedDurationMs) * 100;
    return Math.max(0, Math.min(100, pct));
  }

  isOvertime(t: any): boolean {
    return this.isRunning(t) && this.elapsedMs(t) > t.expectedDurationMs;
  }

  overtimeMs(t: any): number {
    return Math.max(0, this.elapsedMs(t) - (t.expectedDurationMs || 0));
  }

  progressClass(t: any): string {
    if (this.isOvertime(t)) return 'overtime';
    const p = this.progressPct(t);
    if (p >= 70) return 'warn';
    return '';
  }

  // Format elapsed as HH:MM:SS
  formatElapsed(ms: number): string {
    const totalSeconds = Math.floor(ms / 1000);
    const hours = Math.floor(totalSeconds / 3600);
    const minutes = Math.floor((totalSeconds % 3600) / 60);
    const seconds = totalSeconds % 60;
    const pad = (n: number) => (n < 10 ? '0' + n : '' + n);
    return `${hours > 0 ? pad(hours) + ':' : ''}${pad(minutes)}:${pad(seconds)}`;
  }

  trackById(_idx: number, t: any) { return t.id; }

  // Views: ayer, hoy, semana
  currentView: 'yesterday' | 'today' | 'week' = 'today';
  setView(v: 'yesterday' | 'today' | 'week') { this.currentView = v; }

  get filtered() {
    const now = Date.now();
    const startToday = startOfDayTs(now);
    const startYesterday = startToday - 24 * 60 * 60 * 1000;
    const startWeek = startOfWeekMondayTs(now);
    const endToday = startToday + 24 * 60 * 60 * 1000;
    const endWeek = startWeek + 7 * 24 * 60 * 60 * 1000;

  let list: typeof this.tasks = [];
    if (this.currentView === 'yesterday') {
      // Ayer: por fecha planificada
      list = this.tasks.filter(t => t.plannedFor && dateStrToRange(t.plannedFor).start >= startYesterday && dateStrToRange(t.plannedFor).start < startToday);
    } else if (this.currentView === 'today') {
      list = this.tasks.filter(t => t.plannedFor && dateStrToRange(t.plannedFor).start >= startToday && dateStrToRange(t.plannedFor).start < endToday);
    } else {
      // Semana: por plan (excluye hoy)
      list = this.tasks.filter(t => t.plannedFor && dateStrToRange(t.plannedFor).start >= startWeek && dateStrToRange(t.plannedFor).start < endWeek && !(dateStrToRange(t.plannedFor).start >= startToday && dateStrToRange(t.plannedFor).start < endToday));
    }

    // Text search
    const term = this.searchTerm.trim().toLowerCase();
    if (term) {
      list = list.filter(t =>
        t.name.toLowerCase().includes(term) ||
        (t.description || '').toLowerCase().includes(term) ||
        (t.tags || []).some(tag => tag.toLowerCase().includes(term))
      );
    }

    // Priority filter
    if (this.filterPriority !== 'all') {
      list = list.filter(t => (t.priority || 'low') === this.filterPriority);
    }

    // Status filter
    if (this.filterStatus !== 'all') {
      list = list.filter(t => {
        if (this.filterStatus === 'done') return !!t.done;
        if (this.filterStatus === 'running') return this.isRunning(t);
        if (this.filterStatus === 'paused') return !t.done && !this.isRunning(t);
        return true;
      });
    }

    return list;
  }

  // Quick helpers for UI
  setExpected(t: any, mins: number) {
    this.updateExpected(t, mins);
  }

  priorityClass(p?: 'low' | 'medium' | 'high') {
    return p ? `prio-${p}` : 'prio-low';
  }

  // Summary for current view
  get summary() {
    const list = this.filtered;
    const running = list.filter(t => this.isRunning(t)).length;
    const done = list.filter(t => !!t.done).length;
    const totalElapsed = list.reduce((acc, t) => acc + this.elapsedMs(t), 0);
    return { count: list.length, running, done, totalElapsed };
  }

  // Counts per view for tabs
  get counts() {
    const now = Date.now();
    const startToday = startOfDayTs(now);
    const startYesterday = startToday - 24 * 60 * 60 * 1000;
    const startWeek = startOfWeekMondayTs(now);
    const endToday = startToday + 24 * 60 * 60 * 1000;
    const endWeek = startWeek + 7 * 24 * 60 * 60 * 1000;

    const yesterday = this.tasks.filter(t => t.plannedFor && dateStrToRange(t.plannedFor).start >= startYesterday && dateStrToRange(t.plannedFor).start < startToday).length;
    const today = this.tasks.filter(t => t.plannedFor && dateStrToRange(t.plannedFor).start >= startToday && dateStrToRange(t.plannedFor).start < endToday).length;
    const week = this.tasks.filter(t => t.plannedFor && dateStrToRange(t.plannedFor).start >= startWeek && dateStrToRange(t.plannedFor).start < endWeek && !(dateStrToRange(t.plannedFor).start >= startToday && dateStrToRange(t.plannedFor).start < endToday)).length;

    return { yesterday, today, week };
  }

  // Subtasks
  addSubtask(t: any): void {
    const text = (t.newSubtaskText || '').trim();
    if (!text) return;
    t.subtasks = t.subtasks || [];
    t.subtasks.push({ id: cryptoRandomId(), text, done: false });
    t.newSubtaskText = '';
    this.saveToStorage();
  }

  toggleSubtask(t: any, s: any): void {
    s.done = !s.done;
    this.saveToStorage();
  }

  removeSubtask(t: any, s: any): void {
    const idx = (t.subtasks || []).findIndex((x: any) => x.id === s.id);
    if (idx >= 0) t.subtasks.splice(idx, 1);
    this.saveToStorage();
  }

  subtaskCounts(t: any) {
    const total = (t.subtasks || []).length;
    const done = (t.subtasks || []).filter((s: any) => !!s.done).length;
    const pct = total ? Math.round((done / total) * 100) : 0;
    return { total, done, pct };
  }

  duplicateTask(t: any): void {
    const clone = {
      id: cryptoRandomId(),
      name: t.name,
      expectedDurationMs: t.expectedDurationMs,
      startedAt: null,
      accumulatedMs: 0,
      done: false,
      createdAt: Date.now(),
      description: t.description || '',
      tags: [...(t.tags || [])],
      priority: t.priority || 'low',
      dueAt: t.dueAt || undefined,
      subtasks: (t.subtasks || []).map((s: any) => ({ id: cryptoRandomId(), text: s.text, done: s.done })),
      notes: t.notes || '',
    };
    this.tasks.unshift(clone as any);
    this.saveToStorage();
  }

  // Drag & Drop handlers for subtasks
  onSubtaskDragStart(t: any, index: number, ev: DragEvent) {
    this.dragTaskId = t.id;
    this.dragFromIndex = index;
    this.dragOverIndex = null;
    try { ev.dataTransfer?.setData('text/plain', String(index)); } catch {}
    if (ev.dataTransfer) ev.dataTransfer.effectAllowed = 'move';
  }
  onSubtaskDragOver(t: any, index: number, ev: DragEvent) {
    if (t.id !== this.dragTaskId) return;
    ev.preventDefault();
    this.dragOverIndex = index;
  }
  onSubtaskDrop(t: any, index: number, ev: DragEvent) {
    if (t.id !== this.dragTaskId) return;
    ev.preventDefault();
    const from = this.dragFromIndex;
    const to = index;
    if (from == null || to == null || from === to) {
      this.clearDrag();
      return;
    }
    const arr = t.subtasks || [];
    if (!arr.length) { this.clearDrag(); return; }
    const item = arr.splice(from, 1)[0];
    arr.splice(to, 0, item);
    this.clearDrag();
  }
  onSubtaskDragEnd(_ev: DragEvent) { this.clearDrag(); }
  private clearDrag() { this.dragTaskId = null; this.dragFromIndex = null; this.dragOverIndex = null; }

  private saveToStorage() {
    try {
      localStorage.setItem('tasklog.tasks', JSON.stringify(this.tasks));
    } catch {}
  }

  // Helper for tag chips preview in create form
  parseTags(text: string): string[] {
    return (text || '')
      .split(',')
      .map(t => t.trim())
      .filter(Boolean);
  }
}

// Tiny helper to generate unique IDs without external deps
function cryptoRandomId(): string {
  // window.crypto may not exist in SSR; fall back to Math.random
  try {
    // @ts-ignore
    if (typeof crypto !== 'undefined' && crypto.getRandomValues) {
      // @ts-ignore
      const buf = new Uint8Array(8);
      // @ts-ignore
      crypto.getRandomValues(buf);
      return Array.from(buf, b => b.toString(16).padStart(2, '0')).join('');
    }
  } catch {}
  return Math.random().toString(36).slice(2, 10);
}

// Time helpers
function startOfDayTs(ts: number): number {
  const d = new Date(ts);
  d.setHours(0, 0, 0, 0);
  return d.getTime();
}

function startOfWeekMondayTs(ts: number): number {
  const d = new Date(ts);
  d.setHours(0, 0, 0, 0);
  const day = d.getDay(); // 0=Sun, 1=Mon,...
  const diffToMonday = (day === 0 ? -6 : 1 - day); // move back to Monday
  d.setDate(d.getDate() + diffToMonday);
  return d.getTime();
}

// Local date helpers
function toLocalDateString(d: Date = new Date()): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  return `${y}-${m}-${day}`;
}
function dateStrToRange(dateStr: string): { start: number; end: number } {
  const d = new Date(dateStr + 'T00:00:00');
  const start = d.getTime();
  const end = start + 24 * 60 * 60 * 1000;
  return { start, end };
}
