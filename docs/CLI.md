# CLI de `explain` — comandos, opciones y salidas de ejemplo

Referencia detallada del ejecutable. El [README](../README.md) resume instalación y filosofía del proyecto.

**Entornos:** el mismo paquete funciona en **Linux**, **macOS** y **Windows** (Python ≥ 3.9, sin dependencias extra). En Windows el script suele ser `.venv\Scripts\explain.exe` tras `pip install`.

---

## Salida compacta (defecto)

`explain` agrupa bloques con título, mensaje original, *por qué* y *qué hacer*. Si no hay coincidencias en la base, puede listar **Desconocidos** para feedback.

### Error de C que sí está en la base

**Entrada (stdin):**

```text
main.c:10:3: error: implicit declaration of function 'malloc' [-Wimplicit-function-declaration]
```

**Comando:**

```bash
explain --lang C < entrada.txt
# o: cat entrada.txt | explain --lang C
```

**Salida esperada (estructura):**

- Cabecera `(explain · C)` y línea separadora.
- Sección **Errores** con un ítem numerado.
- Título del patrón (p. ej. función no declarada), línea `error: …`, apartados **por qué** y **qué hacer** con lista de sugerencias.

*(El texto exacto depende de la entrada; los títulos vienen de `explain/patterns/c_lang.py`.)*

### Advertencia con patrón

**Entrada:**

```text
gcc -Wall -c x.c
x.c:4:1: warning: unused variable 'n' [-Wunused-variable]
```

**Comando:**

```bash
explain --lang C < entrada.txt
```

**Salida esperada:**

- Sección **Advertencias** (después de errores, si los hay).
- Bloque explicando variable no usada y sugerencias (`(void)n`, eliminar, etc.).

### `--ub-hints` (C / C++ / Assembly)

Solo tiene efecto extra si en el **comando** o en la **texto** hay evidencia de `-fsanitize`, salida de sanitizers, o flags tipo `-Wall` / `-Wextra` / … (ver README).

**Entrada:**

```text
gcc -Wall -c x.c
x.c:1:2: warning: comparison is always false [-Wtautological-compare]
```

**Comando:**

```bash
explain --lang C --ub-hints < entrada.txt
```

**Salida esperada:**

- Igual que sin `--ub-hints` para errores/advertencias estándar.
- Bloque adicional **Posible comportamiento indefinido (indicios)** con etiquetas **UB-RISK** (*fuerte* / *moderado* / *heurística*) y, a veces, **`· crash: …`**.
- Si **no** hay evidencia de flags/sanitizers en la salida ni en `explain …`, esa sección **no aparece** (con `-v`, aviso en stderr).

### `-cnt` / `--count`

**Comando:**

```bash
printf '%s\n' 'x.c:1:1: error: implicit declaration of function bar' | explain -cnt --lang C
```

**Salida esperada (líneas):**

```text
(explain · conteo · C)
errores: 1
advertencias explicadas: 0
líneas warning (listado): 0
desconocidos: 0
total explicados (err+adv): 1
```

Con `--ub-hints` activo y sección UB visible, aparece también `indicios UB-RISK: N`.

### `-m` / `--match`

Filtra bloques cuyo mensaje, `archivo:línea`, título o símbolo contengan el texto.

```bash
explain make all -m memcpy
```

### `--full`

Mismo contenido que el modo compacto pero con separadores largos (`━━━`), prefijos `ERROR` / `WARNING` y bloques más verbosos.

### `-v` / `--verbose`

Antes del resumen, vuelca la **salida cruda** del comando o stdin en **stderr**.

### `--shell CMD`

Ejecuta `CMD` con `shell=True` del sistema (en Windows suele ser **cmd**), captura stdout+stderr y los analiza.

```bash
explain --shell "gcc -Wall -c main.c 2>&1"
```

---

## Opciones resumidas

| Opción | Rol |
|--------|-----|
| `-h`, `--help` | Ayuda |
| `--version` | Versión y autor |
| `-l`, `--lang` | Base de patrones: `auto`, `C`, `C++`, `Assembly`, `C#`, `Python`, `JavaScript`, `Rust` |
| `-v`, `--verbose` | Log crudo en stderr |
| `--full` | Formato extendido |
| `--ub-hints` | Sección UB-RISK (con condiciones; ver README) |
| `-nw`, `--no-warnings` | Oculta advertencias |
| `--max-warnings N` | Tope de líneas `warning` sin patrón al final |
| `-m`, `--match` | Filtro por subcadena |
| `--shell CMD` | Ejecutar vía shell |
| `-cnt`, `--count` | Solo conteos |

---

## Windows (PowerShell / cmd)

- Activar venv: `.venv\Scripts\activate`
- Tubería en PowerShell: `make all 2>&1 | explain` (si `make` existe en PATH; en puro Windows a menudo se usa `cmake --build` o MSBuild y se redirige igual).
- Sin mezclar stderr: `explain` no ve los warnings del compilador; usá `2>&1` o ejecutá con `--shell`.

---

## Tests automatizados

Desde la raíz del repo:

```bash
python3 -m unittest discover -s tests -v
```
