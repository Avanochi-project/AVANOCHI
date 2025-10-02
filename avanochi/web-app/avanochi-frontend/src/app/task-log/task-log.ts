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
  }> = [
    {
      id: cryptoRandomId(),
      name: 'Diseñar UI de registro automático',
      expectedDurationMs: 25 * 60 * 1000,
      startedAt: Date.now() - (2 * 60 + 18) * 1000, // 6m18s ago
      accumulatedMs: 0,
    },
    {
      id: cryptoRandomId(),
      name: 'Escribir casos de prueba',
      expectedDurationMs: 40 * 60 * 1000,
      startedAt: null,
      accumulatedMs: 0,
    },
  ];

  // New task form fields
  newTaskName = '';
  newTaskMinutes: number | null = 25;

  // A ticking signal that triggers change detection in zoneless mode
  nowMs = signal<number>(Date.now());
  private timerId: any;

  ngOnInit(): void {
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
    this.tasks.unshift({
      id: cryptoRandomId(),
      name,
      expectedDurationMs: mins * 60 * 1000,
      startedAt: null,
      accumulatedMs: 0,
    });
    this.newTaskName = '';
    this.newTaskMinutes = 25;
  }

  startTask(t: any): void {
    if (t.done) return;
    if (t.startedAt == null) {
      t.startedAt = Date.now();
    }
  }

  pauseTask(t: any): void {
    if (t.startedAt != null) {
      t.accumulatedMs += Date.now() - t.startedAt;
      t.startedAt = null;
    }
  }

  finishTask(t: any): void {
    if (t.startedAt != null) {
      this.pauseTask(t);
    }
    t.done = true;
  }

  updateExpected(t: any, minutes: number): void {
    const mins = Math.max(1, Math.min(24 * 60, Math.floor(minutes || 0)));
    t.expectedDurationMs = mins * 60 * 1000;
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
