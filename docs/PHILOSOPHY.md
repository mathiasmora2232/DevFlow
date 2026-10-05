# Filosofía de ejecución

## Regla principal

La solución correcta es la más simple que satisfaga correctamente el problema actual y no bloquee razonablemente el siguiente nivel de escala.

## Orden de decisión

1. Correctitud.
2. Riesgo.
3. Tiempo de salida.
4. Validación de usuario/negocio.
5. Costo operativo.
6. Mantenibilidad.
7. Escalabilidad necesaria.
8. Elegancia técnica.

La escalabilidad hipotética no debe ganarle automáticamente al costo real de hoy.

## Loop DevFlow

### 1. Contexto
¿Qué existe y qué quiere conseguirse?

### 2. Diagnóstico
¿Qué está bien, qué está mal y qué no sabemos?

### 3. Hipótesis
Cuando no hay evidencia suficiente, marcar explícitamente `[Inferencia]`.

### 4. Plan
Ordenar por dependencia, riesgo y valor.

### 5. Ejecución
Cambios pequeños, coherentes y testeables.

### 6. Validación
Pruebas técnicas + criterio de aceptación.

### 7. Revisión
Seguridad, performance, compatibilidad, observabilidad y operación.

### 8. Evidencia
Commits, tests, CI, reportes, métricas.

### 9. Cierre
Actualizar trace, changelog si aplica y pendientes.

### 10. Próximo movimiento
Determinar el siguiente trabajo de mayor impacto.

## Anti-patterns

- Kubernetes para un MVP sin necesidad real.
- Microservicios sin fronteras de dominio ni presión de escala.
- Migrar porque una tecnología está de moda.
- Refactor masivo dentro de un hotfix.
- Puntuar performance sin medir.
- Declarar “seguro” después de una revisión superficial.
- Cerrar trabajo solo porque compiló.
- Dejar decisiones importantes únicamente en un chat.
