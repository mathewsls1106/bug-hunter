# Operaciones Python que pueden lanzar excepciones

Úsalo como checklist en la Fase 2. Para cada fila, sigue la pila de llamadas y aplica el filtro de relevancia antes de reportar.

## Operaciones y excepciones típicas

| Operación | Excepciones habituales | Pregunta clave |
|---|---|---|
| Acceso `d[k]`, `lst[i]` | `KeyError`, `IndexError` | ¿Puede faltar la clave/el elemento con datos reales? |
| Atributo/llamada sobre posible `None` | `AttributeError`, `TypeError` | ¿Alguna ruta devuelve `None` (`.get`, `re.match`, `dict.pop`)? |
| Conversión `int()`, `float()`, `Decimal()`, fechas | `ValueError`, `InvalidOperation` | ¿Viene de input externo sin validar? |
| `json.loads`, `yaml`, `csv`, XML | `JSONDecodeError`, `ParserError` | ¿El cuerpo/archivo puede venir malformado o vacío? |
| Archivos y rutas | `FileNotFoundError`, `PermissionError`, `UnicodeDecodeError`, `IsADirectoryError` | ¿Existe, tiene permisos, qué encoding? |
| Red (`requests`, `httpx`, sockets) | `Timeout`, `ConnectionError`, `HTTPError`, `JSONDecodeError` en la respuesta | ¿Hay timeout? ¿Se valida el status y el cuerpo? |
| Base de datos | `IntegrityError`, `OperationalError`, deadlocks | ¿Hay rollback? ¿Se cierra la conexión? |
| Aritmética | `ZeroDivisionError`, `OverflowError` | ¿El divisor puede ser 0 (listas vacías, totales)? |
| Iteración / generadores | `StopIteration`, `RuntimeError` (mutación durante iteración) | ¿Se modifica la colección que se recorre? |
| Subprocesos | `CalledProcessError`, `FileNotFoundError`, `TimeoutExpired` | ¿Se revisa el código de salida? ¿Hay timeout? |
| Concurrencia / async | `CancelledError`, condiciones de carrera, tareas sin `await` | ¿Se pierde una excepción dentro de una tarea? |
| Recursos | fugas de archivos/conexiones | ¿Se usa `with`/`finally`? |
| Seguridad | `eval`, `pickle`, `subprocess(shell=True)`, SQL concatenado | ¿Input externo llega ahí? |

## Anti-patrones que esconden errores

- `except:` o `except Exception:` seguido de `pass`, `continue` o solo `print`.
- `except` que traga la excepción y devuelve un valor "por defecto" sin log.
- `raise` sin `from` que pierde la causa original.
- `finally` con `return` (descarta la excepción en curso).
- `assert` usado para validar input (se desactiva con `-O`).

