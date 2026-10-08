---
name: exception-bug-hunter
description: Caza excepciones no controladas y bugs en código Python que sean alcanzables y relevantes, los confirma con un test si existen, analiza la causa raíz, propone correcciones modulares y guarda reportes con nomenclatura fija. Úsala siempre que el usuario pida auditar, revisar, buscar bugs, cazar fallos, QA adversarial, revisar un traceback, un crash o un error 500, o validar robustez antes de un PR o release.
---

# Exception & Bug Hunter

Encuentra dónde puede fallar el código y lo **demuestra**. Casi cualquier línea puede lanzar alguna excepción en teoría; un reporte que lista todas es ruido y el equipo deja de leerlo. Por eso esta skill solo reporta lo que cumple el **filtro de relevancia** y separa lo confirmado de lo sospechado.

## 1. Cuándo actuar

**Actúa** cuando el usuario pida : "¿dónde puede fallar esto?", "Revisa el codigo", "revisa el manejo de errores", "analiza este traceback / crash / error 500", "qué casos límite me faltan", "estoy por hacer un PR, revísalo", "bug hunt".

**No actúes** (o dilo y propón otra cosa) cuando: pidan escribir una feature nueva sin revisar riesgos, formatear/estilizar código, o explicar qué hace un fragmento sin buscar fallos. Si la petición es ambigua entre "revisar" y "arreglar", pregunta cuál (ver §2).

## 2. Protocolo interactivo (fases)

Haz **una sola pregunta por mensaje** y espera la respuesta. Ofrece 2-4 opciones concretas cuando sea posible, para que responder sea rápido. Antes de preguntar, intenta inferir la respuesta del contexto (archivos subidos, repo, mensajes previos); no preguntes lo que ya sabes. Si el usuario dice "tú decide", elige el valor por defecto indicado y continúa.

**Fase 0 – Alcance.** Pregunta qué analizar: un archivo/módulo, un diff/PR, o un traceback concreto. Por defecto: el código que el usuario haya compartido, o los cambios que hay en git.

**Fase 1 – Contexto.** Una pregunta a la vez, solo las que falten:
1. ¿Cómo se ejecuta? (API web, script/batch, worker, librería). Define qué entradas son "reales".
2. ¿Hay manejador global de errores? (middleware, `excepthook`, decorador). Por defecto: asumir que no.
3. ¿Qué es inaceptable? (perder datos, 500 al cliente, crash silencioso). Define el impacto.

**Fase 2 – Caza.** Sin preguntas. Ejecuta análisis (ver §3), aplica el filtro y clasifica cada candidato.

**Fase 3 – Confirmación.** Para cada candidato relevante escribe un test que intente provocarlo y ejecútalo. Estados posibles:
- `CONFIRMADO`: el test falla de forma reproducible.
- `SOSPECHADO`: plausible pero no reproducido (di por qué no se pudo).
- `DESCARTADO`: otro código lo maneja o no es alcanzable (una línea de motivo; no lo infles).

**Fase 4 – Causa raíz y resolución.** Aplica §4 a cada hallazgo `CONFIRMADO`/`SOSPECHADO`. Presenta un resumen priorizado y pregunta (una pregunta): ¿qué hallazgo corregimos primero? Aplica correcciones **de una en una** y solo con aprobación.

**Fase 5 – Documentación.** Genera los archivos de §5 y confirma las rutas al usuario.

## 3. Cómo cazar

**Filtro de relevancia.** Reporta un candidato solo si cumple las tres:
1. **Alcanzable**: existe una entrada o condición real que lo provoca (indícala concretamente, p. ej. `{"qty": null}`). Si el resto del código lo hace imposible, descártalo.
2. **Sin manejar**: sigue la pila de llamadas hacia arriba hasta el punto de entrada. Si algo lo captura de forma adecuada, descártalo.
3. **Importa**: la consecuencia es crash, pérdida de datos, estado inconsistente o error equivocado (500 en vez de 400). Si fallar ruidosamente es el comportamiento correcto, no es hallazgo.

También reporta los `except` demasiado amplios (`except Exception: pass`) que **esconden** errores, porque son el reverso del mismo problema.

## 4. Causa raíz y resolución

Para cada hallazgo, completa **todos** estos pasos en orden (así los reportes son comparables):

1. **Síntoma**: qué se observa (excepción, tipo y mensaje esperados).
2. **Disparador**: la entrada o condición mínima que lo provoca.
3. **Camino de ejecución**: función → función → línea donde se lanza.
4. **Causa raíz**: aplica "por qué" iterativo (hasta 5) hasta llegar a algo que se pueda cambiar. Quédate con la causa, no con el síntoma ("falta `.get()`" es síntoma; "el contrato de entrada no está validado en el borde" es causa).
5. **Clasificación** (elige una): `validación-ausente` · `except-amplio` · `fallo-externo-no-previsto` (red/IO/BD) · `estado-inválido` · `contrato-roto` (tipos/None) · `concurrencia` · `recurso-sin-liberar`.
6. **Severidad**: Crítica (pérdida/corrupción de datos o seguridad) · Alta (crash en flujo principal) · Media (crash en flujo secundario, error mal reportado) · Baja (solo con entradas improbables).
7. **Resolución modular**, en tres niveles independientes, aplicando solo los que correspondan:
   - **Prevenir**: validar en el borde del sistema.
   - **Manejar**: capturar la excepción **específica** donde se pueda hacer algo útil (reintentar, valor por defecto, error claro).
   - **Observar**: log con contexto o métrica, y dejar subir lo que deba fallar.
8. **Test de regresión**: el mismo test de la Fase 3, que debe pasar tras la corrección.

Reglas de las correcciones: cada hallazgo es un cambio pequeño e independiente (un parche, un test, un commit lógico); nunca propongas `except Exception: pass` ni "envolver todo en try/except"; no modifiques código de producción sin aprobación explícita.

## 5. Documentación y nomenclatura (estricta)

Usa siempre `scripts/next_bug_id.py` para obtener el siguiente ID y los nombres de archivo; así la numeración no se repite ni se desordena:

```bash
python scripts/next_bug_id.py --dir bug-reports --title "KeyError en parse_order con qty nulo"
```

Devuelve JSON con `id`, `report` y `test`. Con eso, crea:

| Artefacto | Ruta y nombre |
|---|---|
| Reporte por hallazgo | `bug-reports/BUG-NNN_YYYYMMDD_<slug>.md` |
| Resumen de la sesión | `bug-reports/HUNT_YYYYMMDD_<modulo>.md` |
| Test de regresión | `tests/regression/test_bug_NNN_<slug_con_guion_bajo>.py` |
| Índice | `bug-reports/INDEX.md` (una fila por hallazgo; créalo si no existe) |

Usa las plantillas de `references/report-template.md`. Los reportes en estado `DESCARTADO` van solo como una línea en el resumen `HUNT_`, no como archivo propio. Nunca sobrescribas un reporte existente: si el hallazgo ya está documentado, actualiza su estado y añade una nota fechada.

## 6. Cierre

Termina con un resumen corto: cuántos hallazgos `CONFIRMADO` / `SOSPECHADO` / `DESCARTADO`, el más grave en una frase, y las rutas de los archivos creados. Si no encontraste nada relevante, dilo con claridad; un reporte vacío honesto vale más que uno inflado.
