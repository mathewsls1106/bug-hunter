# Plantillas de reportes

## Reporte por hallazgo: `bug-reports/BUG-NNN_YYYYMMDD_<slug>.md`

```markdown
# BUG-NNN: <título corto>

- **Estado:** CONFIRMADO | SOSPECHADO
- **Severidad:** Crítica | Alta | Media | Baja
- **Clasificación:** validación-ausente | except-amplio | fallo-externo-no-previsto | estado-inválido | contrato-roto | concurrencia | recurso-sin-liberar
- **Ubicación:** `ruta/archivo.py:LINEA` (función `nombre`)
- **Fecha:** YYYY-MM-DD

## Síntoma
Excepción y mensaje esperados.

## Disparador
Entrada o condición mínima que lo provoca.

## Camino de ejecución
`entrada()` → `intermedia()` → `archivo.py:LINEA`

## Causa raíz
Cadena de "por qué" resumida y la causa final.

## Evidencia
Test: `tests/regression/test_bug_NNN_<slug>.py`
Resultado: salida relevante del test al fallar. Si es SOSPECHADO, explica por qué no se pudo reproducir.

## Resolución propuesta
- **Prevenir:** ...
- **Manejar:** ...
- **Observar:** ...

Diff mínimo sugerido (si aplica).

## Historial
- YYYY-MM-DD: detectado.
```

## Resumen de sesión: `bug-reports/HUNT_YYYYMMDD_<modulo>.md`

```markdown
# Hunt YYYY-MM-DD: <módulo o PR>

**Alcance:** archivos analizados
**Contexto:** cómo se ejecuta, manejador global (sí/no), impacto inaceptable
**Herramientas corridas:** ruff, bandit, mypy, pytest (resultado breve)

## Hallazgos
| ID | Estado | Severidad | Ubicación | Resumen |
|---|---|---|---|---|

## Descartados
- `archivo.py:LINEA`: motivo en una línea.

## Siguientes pasos
Orden sugerido de corrección.
```

## Índice: `bug-reports/INDEX.md`

```markdown
| ID | Fecha | Estado | Severidad | Título | Reporte |
|---|---|---|---|---|---|
```
