import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TaskLog } from './task-log';

describe('TaskLog', () => {
  let component: TaskLog;
  let fixture: ComponentFixture<TaskLog>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [TaskLog]
    })
    .compileComponents();

    fixture = TestBed.createComponent(TaskLog);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
