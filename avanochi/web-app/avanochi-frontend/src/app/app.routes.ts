import { Routes } from '@angular/router';
import { TasksToday } from './tasks-today/tasks-today';
import { TaskLog } from './task-log/task-log';

export const routes: Routes = [
	{ path: '', component: TasksToday },
	{ path: 'tasks', component: TaskLog },
];