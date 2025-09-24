# AVANOCHI
Aplicación de `productividad` con un enfoque lúdico, diseñada para mejorar la `gestión del tiempo` y el `rendimiento` durante la jornada laboral. Avanochi funciona como un “tamagochi” productivo, que motiva al empleado mientras organiza sus tareas, mide su rendimiento y promueve hábitos saludables.

## 1. Objetivos
- `Incrementar la productividad` y organización personal.
- Promover `hábitos laborales saludables` mediante recordatorios.
- Ofrecer `estadísticas y recomendaciones` personalizadas mediante IA.
- Integrar la gestión de tareas con un `sistema interactivo y gamificado`.

## 2. Recursos de Azure propuestos
- Gestión de tareas (To-Do list gamificada)
    - Crear, consultar y actualizar `tareas diarias y semanales`.
    - Registro automático de `progreso y tiempos invertidos`.

- Asistente inteligente (IA Foundry)
    - `Consejos de organización` según carga laboral y hábitos previos.
    - `Ajuste dinámico del horario` en base al rendimiento histórico.
    - `Voice assistant` para poder interactuar con el como si fuera un compañero mas

- Estadísticas de rendimiento
    - `Horas trabajadas` diarias y semanales.
    - `Tareas completadas vs pendientes` por cada jornada.
    - Control de `descansos`.

- Integración “Healthy life”
    - `Jornada de trabajo`: Avanochi trabaja a tu lado. Si superas las 8,5h, se cansa y te pide descansar, igual que él.
    - `Hora de comer`: Avanochi necesita comer. Si no le das de comer, asume que tú tampoco lo has hecho y te recuerda parar para almorzar.
    - `Hidratación`: Avanochi tiene sed periódicamente. Cuando le das agua, entiendes que también debes hidratarte.

![alt text](assets/image.png)

## 3. Caso de uso
1. El empleado inicia sesión en Avanochi al `comenzar su jornada`.
2. Si es lunes, se cargan las tareas pendientes de la semana anterior o se generan nuevas.
3. Durante el día:
    - El empleado marca `avances en las tareas`.
    - Avanochi registra `tiempos, descansos y progreso`.
    - `Recomienda pausas` si detecta sobrecarga.
4. Al final de la jornada:
    - Se realiza un `resumen de horas, tareas y descansos`.
    - Se generan `estadísticas de rendimiento`.
    - Se preparan `recomendaciones para el día siguiente`.

## 4. Aprendizaje continuo
El modelo de IA `analiza el historial de trabajo del empleado` y ajusta las recomendaciones con el tiempo, personalizando horarios y estrategias para `optimizar la productividad`.

Las métricas para evaluar la productividad serían las siguientes:

### Métricas de productividad

| Métrica                                   | Propósito                                                                 |
|-------------------------------------------|---------------------------------------------------------------------------|
| Horas trabajadas                          | Medir la carga diaria y semanal del empleado.                             |
| Tiempo en tareas activas vs. inactivo     | Detectar productividad real frente a tiempos muertos.                     |
| Número de tareas completadas vs. pendientes | Evaluar cumplimiento de objetivos diarios y semanales.                   |
| Progreso porcentual de tareas             | Ver el avance sobre lo planificado.                                       |
| Tiempo promedio por tarea                 | Identificar eficiencia en la ejecución de tareas.                         |
| Desviación entre tiempo estimado y real   | Mejorar la planificación futura y la precisión en estimaciones.           |
| Número y duración de descansos            | Asegurar un balance saludable durante la jornada.                         |
| Cumplimiento de descansos recomendados    | Medir si el empleado sigue las recomendaciones de Avanochi.               |
| Balance trabajo-descanso                  | Prevenir sobrecargas y fomentar hábitos sostenibles.                      |
| Horarios de inicio y fin de jornada       | Analizar consistencia y disciplina en la rutina laboral.                  |
| Días con sobrecarga laboral               | Detectar exceso de horas trabajadas (más de 8,5h).                        |
| Nivel de regularidad semanal              | Observar patrones de rendimiento a lo largo de la semana.                 |
| Tareas reprogramadas o arrastradas        | Identificar retrasos o dificultades recurrentes.                          |
| Tiempo de respuesta al feedback de Avanochi | Medir la efectividad de las recomendaciones dadas.                       |
| Frecuencia de interacciones con Avanochi  | Evaluar adopción y uso del sistema por parte del empleado.                |
