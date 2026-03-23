# CLI de `explain` — comandos, opciones y salidas de ejemplo

Resumen tabular de **flags, entradas e incompatibilidades**: ver **[README.md](../README.md#tabla-del-cli-flags-entradas-combinaciones)** en el repositorio.

Referencia detallada del ejecutable. El [README](../README.md) resume instalación y filosofía del proyecto.

**Entornos:** el mismo paquete funciona en **Linux**, **macOS** y **Windows** (Python ≥ 3.9, sin dependencias extra). En Windows el script suele ser `.venv\Scripts\explain.exe` tras `pip install`.

---

## Salida compacta (defecto)

`explain` agrupa bloques con título, mensaje original, *por qué* y *qué hacer*. Al final pueden aparecer dos bloques de **feedback** distintos:

- **Desconocidos:** líneas que **parecen errores** (o enlace) y **no** matchean la base.
- **Advertencias fuera de la base:** líneas con **`warning`** que **no** tienen patrón; texto crudo numerado (tope `--max-warnings`, defecto 5). No se mezclan con Desconocidos a propósito.

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

Con **`--lang`** distinto de C, C++ o Assembly, **`--ub-hints` no hace nada útil**: no se calcula contexto UB ni ítems UB-RISK; la salida incluye un bloque **«--ub-hints (no aplica)»** (y en `-cnt` una línea `ub-hints: no aplica …`).

Hay **contexto UB** si en el **argv** del comando o en la **salida** aparece algo de: **`-fsanitize`**, mensajes **ASan/UBSan/TSan**, línea de compilación con **`-Wall` / `-Wextra` / `-Wpedantic` / `-Wconversion` / `-Wundef`**, variables tipo **`CFLAGS=`** / **`CXXFLAGS=`** / **`CPPFLAGS=`** / **`LDFLAGS=`** con esas flags, o **cualquier** etiqueta **`[-Walgo]`** en un mensaje del compilador (útil si `make` no imprime el `gcc …`).

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
- Si **no** hay contexto UB, aparece **«--ub-hints (sección UB-RISK no activada)»** al inicio (compacto o `--full`) con el detalle de qué se busca.
- Si hay contexto pero **ningún** mensaje recibe etiqueta UB-RISK, al **pie** se indica que no hubo evidencia de riesgo en esa salida (la heurística sí estuvo activa).
- Si hay ítems UB-RISK, el pie resume el conteo.

### Advertencias sin patrón (sección de feedback)

**Entrada** (ejemplo inventado, no en la base):

```text
weird.c:1:1: warning: totally unknown diagnostic [-Wfoobar]
```

**Salida (compacto):** sección **«Advertencias fuera de la base (feedback)»** con bloques `[1/1] warning crudo (copiar):` y el texto literal. Si hay muchas, `Total: N (mostrando M; usá --max-warnings para más).`

### `--man` (ficha / cápsula)

Misma fuente que sin `--man`: **comando**, **`-i`/`--input-file`**, o **stdin**. **No** combina con **`-cnt`**.

**TTY sin fuente:** si ejecutás `explain --man E1` en una terminal **sin** tubería, **sin** `-i` y **sin** comando posicional, no hay texto que analizar: verás un error claro en stderr (exit 2), no la ficha. **No** es un fallo de `--man`: hace falta el log crudo por uno de esos tres medios.

**IDs:** `E1`, `E2`, … = ítem *n* de la sección **Errores**; `W1`, … = **Advertencias** explicadas; `UB1`, … = **UB-RISK** (requiere contexto UB en el log para haber ítems).

**Compatibilidad con `-m` / `--match`:** sí. Primero se analiza el log, luego **`filtrar_por_match`** reduce las listas de errores, advertencias explicadas, etc.; **`E1` / `W2` / `UB1` se refieren a la numeración ya filtrada**. Si pedís un índice que no existe tras el filtro, verás el error `no hay En (hay 0 ítem(s)…)` o un número menor al esperado.

Ejemplo (dos errores en stdin; con `-m implicit` solo queda el de declaración implícita, y **E1** es ese):

```bash
printf '%s\n%s\n' \
  'a.c:1:1: error: conflicting types for f' \
  'b.c:2:2: error: implicit declaration of function bar' \
  | explain --lang C --man E1
# Ficha del error «conflicting types» (primer error sin filtro).

printf '%s\n%s\n' \
  'a.c:1:1: error: conflicting types for f' \
  'b.c:2:2: error: implicit declaration of function bar' \
  | explain --lang C -m implicit --man E1
# Ficha del error «implicit declaration» (único que pasa el filtro → E1).
```

**Alias `-f` y `-F`:** mismo valor que **`--man`** (`explain -f E1-2-5 …`).

**Varias fichas en un solo `--man` / `-f` / `-F`:** misma categoría con `-` o `/` entre números (`E1-2-5`, `E1/2/3`, `W2-6-7`, `UB1-2`); varios grupos separados por espacio (entre comillas en el shell): `E1-2 W3 UB1`. También podés separar IDs en argv: `explain --man E1 W1 make iv` (los tokens `W1`, `UB2`, … inmediatamente después del valor de `--man` cuentan como más fichas; lo que sigue es el comando). `E12` es el ítem 12, no «E1 y E2»; para dos errores usá `E1-2`.

**Índice pedido que no existe:** si pedís `E1` y no hay errores, verás el aviso en stderr y, si había más fichas (`W1`, …), igual se imprimen las que sí existan; exit 2 solo cuando **ninguna** ficha pudo mostrarse.

**Cápsula en `--man`:** en **C**, **C++**, **Assembly**, **Python**, **JavaScript**, **Rust** y **C#**, la base actual (`explain/patterns/` por idioma) tiene **una entrada manual por cada clave regex** en `explain/capsules/`: bloques **incorrecto / corregido** ilustrativos, «Qué pasó» y regla. Archivos principales: `c_lang.py`, `c_capsules_extended.py`, `c_capsules_gap.py`, `asm_lang.py`, `cpp_capsules.py`; `rust_capsules.py` (Rust); `handwritten_extra.py` con `python_priority_capsules.py`, `js_priority_capsules.py`, `csharp_capsules.py`. **Si** en el futuro un patrón nuevo en `patterns/` no tuviera aún ficha en `capsules/`, **`resolver_capsula`** generaría una **cápsula sintética** (referencia al mensaje crudo + texto desde la base + **Lista de acciones**).

**Tubería:** tiene que ser la **salida cruda** de gcc/clang/make, por ejemplo:

```bash
make iv 2>&1 | explain --man E1
```

No uses `explain make iv | explain --man E1`: el segundo `explain` vería el resumen en español, no el log del compilador.

**Desde archivo volcado:**

```bash
explain --man E1 -i build.log
explain --lang C --man-all -i build.log
```

**`--man-all`:** imprime **varias** fichas seguidas solo para ítems con **cápsula manual** en `explain/capsules/` (no usa sintéticas), orden E → W → UB. Si ninguno califica, exit 1 y aviso en stderr (sugerirá `--man` / `-f` / `-F`).

**Ejemplo mínimo (stdin):**

```bash
printf '%s\n' "x.c:1:1: error: conflicting types for 'f'" | explain --lang C --man E1
```

**Salida:** cabecera `(explain · man · C · E1)` o `(explain · man-all · C · N ficha(s)…)`, mensaje crudo, bloques de ejemplo (manual o sintético) y cierre con texto de la base o solo lista de acciones si la cápsula es sintética.

### `--install-shell-completions`

**Unix:** copia `completions/explain.bash`, `_explain` y `explain.fish` a `~/.local/share/bash-completion/completions/explain`, `~/.zsh/completions/_explain` y `~/.config/fish/completions/explain.fish`. No acepta comando posicional ni log.

```bash
explain --install-shell-completions
```

Tras clonar el repo, el flujo típico es **`make dev`** (venv + `pip install -e .` + este comando). Con **direnv** y el **`.envrc`** del repo, en bash podés tener completions al entrar al directorio sin copiar al home.

**Windows:** el comando no falla; avisa que los completions de shell son para Unix (Git Bash/WSL).

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
advertencias sin patrón: 0
desconocidos: 0
total explicados (err+adv): 1
```

Con `--ub-hints` activo y sección UB visible, aparece también `indicios UB-RISK: N`.

### `-m` / `--match`

Filtra bloques cuyo mensaje, `archivo:línea`, título o símbolo contengan el texto (subcadena, sin regex). Afecta también a **`--man` / `-f` / `-F`**: los índices `E1`, `W2`, … son sobre las listas **después** del filtro (ver sección **`--man`** arriba).

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
| `-f`, `-F`, `--man ID` | Una o varias fichas (`E1`, `E1-2 W3`, …; C/C++/Asm/Python con cápsula manual o sintética) |
| `--man-all` | Solo fichas con cápsula **manual** en `explain/capsules/` |
| `-i`, `--input-file` | Log desde archivo (no con `--shell`); tokens posicionales opcionales solo como pista de `--lang` |
| `--install-shell-completions` | Copia completions bash/zsh/fish al home (Unix); sin comando; tras `git clone` suele usarse con `make dev` |
| `-l`, `--lang` | Base de patrones: `auto`, `C`, `C++`, `Assembly`, `C#`, `Python`, `JavaScript`, `Rust` |
| `-v`, `--verbose` | Log crudo en stderr |
| `--full` | Formato extendido |
| `--ub-hints` | Sección UB-RISK (con condiciones; ver README) |
| `-nw`, `--no-warnings` | Oculta advertencias explicadas y la sección de advertencias sin patrón |
| `--max-warnings N` | Tope en la sección «Advertencias fuera de la base» (feedback) |
| `-m`, `--match` | Filtro por subcadena |
| `--shell CMD` | Ejecutar vía shell |
| `-cnt`, `--count` | Solo conteos |

Con **`--lang auto`** (valor por defecto), el lenguaje se infiere en este orden: primer token del comando posicional (en **TTY** eso suele ser el ejecutable que `explain` lanza; con **tubería** o **`-i`**, los posicionales son solo pista y **no** se ejecutan); si no hay posicionales pero sí **`--shell`**, los tokens del comando shell (`shlex` en Unix); si el primero es genérico (`make`, `cmake`, …), **cualquier token** del argv que sea una herramienta conocida (`cargo`, `node`, `npm`, `dotnet`, `python`, `gcc`, …); extensiones en los argumentos; rutas en el texto del log; patrones en la salida; si no hay señal, **C**.

**Índice sin `--man`:** si los posicionales **empiezan** por `E1`, `W2`, `UB1`, `E1-2` o varios IDs seguidos (`E1 W2 …`), esos tokens se quitan y el resto es el comando (o pistas con tubería/`-i`). La salida es la **resumen habitual** (compacto o `--full`), mostrando solo los errores/advertencias/UB-RISK pedidos; **no** es la ficha didáctica de `--man`. Ej.: `explain E1 dotnet build`, `make iv 2>&1 | explain E1-2 cargo`.

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
