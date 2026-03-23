# explain-errors

**explain** traduce mensajes de compilación y ejecución al español usando **solo patrones en expresiones regulares** y textos fijos: **sin red ni modelos de lenguaje**. Es determinista y auditable: lo que explica está en el código.

**Autor:** Iván Ezequiel Rodriguez · **versión 0.6.7** (también en `pyproject.toml` y `explain --version`).

**Licencia:** [GNU General Public License v3.0](LICENSE) (GPL-3.0). Resumen de copyright en [COPYRIGHT](COPYRIGHT).

## Qué hace

- Ejecuta un comando (por ejemplo `make`, `gcc`, `dotnet`, `cargo`) y **mezcla stdout y stderr** del proceso hijo, así no hace falta acordarse de `2>&1` en ese modo.
- O lee la salida por **stdin** (tubería), por ejemplo `make iv 2>&1 | explain`.
- Detecta el **lenguaje** de la base de patrones (`auto`): primer token del comando (o el argv parseado de `--shell` si no hay posicionales), **cualquier otro token** reconocible (`cargo`, `node`, `dotnet`, `python`, …), extensiones en argumentos y en el log, y forma del mensaje.
- Extrae cuando puede **archivo:línea** y **función** (GCC, MSVC, Python, Node, TypeScript, etc.).
- Apartado **Desconocidos (feedback)**: **solo errores o enlace** que parecen diagnósticos reales pero **no matchean** la base; texto **en crudo** para copiar y ampliar `explain/patterns/`.
- Apartado **Advertencias fuera de la base (feedback)**: **warnings** sin patrón en la base (mismo espíritu que Desconocidos, pero separado: no mezclar errores con advertencias). El tope de líneas lo da **`--max-warnings`** (defecto 5).
- **`--ub-hints`** (solo **C**, **C++** y **Assembly**): con **Python**, **C#**, **Rust**, **JavaScript**, etc., la opción **no activa UB-RISK**; en la salida aparece un aviso **«--ub-hints (no aplica)»** para que no parezca un fallo silencioso. La sección **«Posible comportamiento indefinido (indicios)»** depende de **contexto** visible en el **comando** o en la **salida mezclada**: **`-fsanitize`**, mensajes de **ASan/UBSan/TSan**, líneas de invocación con **`-Wall` / `-Wextra` / `-Wpedantic` / `-Wconversion` / `-Wundef`**, **`CFLAGS`/`CXXFLAGS`/`CPPFLAGS`/`LDFLAGS`** con esas opciones, o **cualquier etiqueta de diagnóstico `[-W…]`** en un mensaje del compilador (útil cuando `make` no imprime el `gcc …`). Si pedís `--ub-hints` y **no** hay contexto, verás **«--ub-hints (sección UB-RISK no activada)»** con el detalle. Si hay contexto pero ningún mensaje recibe etiqueta UB-RISK, un **pie** al final lo aclara (no afirma UB del estándar). Heurística opcional **crash:** en la etiqueta cuando aplica. **No** analiza código fuente.
- **Índice al inicio del comando (`explain E1 …`):** misma numeración que **`--man`** (`E1`, `W2`, `UB1`, `E1-2`, varios tokens seguidos `E1 W2 make`…), pero la salida es la **habitual** (resumen compacto o `--full`), **sin** ficha ni cápsula. Ej.: `explain E1 make iv`, `explain W2 gcc -Wall x.c`. **Compatible con `-cnt` y `-m`** (el filtro por índice se aplica **después** de `-m`). **No** uses esos IDs posicionales junto con **`--man-all`** (error).
- **`--man` / `-f` / `-F` (fichas):** **cápsulas didácticas**; entrada = comando, **`-i`/`--input-file`** o **stdin**. Un ítem: `E1`, `W2`, `UB1`. Varios: `E1-2-5` o `E1/2/3`; mezcla: `E1-2 W3 UB1` (entre comillas en el shell si hay espacios). Si existe **cápsula escrita a mano** para ese patrón (`explain/capsules/c_lang.py` en C/C++/Asm; en **Python**, **JavaScript** y **C#** vía `handwritten_extra.py` más `python_priority_capsules.py`, `js_priority_capsules.py` y `csharp_capsules.py`; **Rust** vía `rust_capsules.py` (importado desde `handwritten_extra.py`)), se usa esa (ejemplos ❌/✅). Si no, en esos lenguajes se genera una **cápsula sintética** desde `explain/patterns/…`. **Entrada obligatoria:** tubería, **`-i` archivo** o **comando**. **Tubo:** salida **cruda** (`make iv 2>&1 | explain --man E1`). **`-i` es solo `--input-file`**. **Incompatible** con `-cnt`. **UBn** con contexto en el log aunque no pases `--ub-hints`.
- **`--man-all`:** solo fichas con **cápsula manual** (no sintética): `c_lang.py` + todo lo que aporta `handwritten_extra.py` (incluye los módulos `*_priority` y `csharp_capsules`); orden E…, W…, UB…. Para el resto usá `--man` / `-f` / `-F` por índice.
- **`-i` / `--input-file`:** leer log desde archivo UTF-8; **no** con **`--shell`**. Opcional: tokens **después de las opciones** (`cargo`, `npm`, `gcc`…) solo como **pista de `--lang`**, sin ejecutarlos.

## Requisitos

- Python **≥ 3.9**
- Sin dependencias externas (solo biblioteca estándar).

## Tabla del CLI (flags, entradas, combinaciones)

### Opciones (orden alfabético lógico)

| Opción | Corta | Rol |
|--------|--------|-----|
| `--help` | `-h` | Ayuda y sale (exit 0). |
| `--version` | — | Versión y autor. |
| `--lang` | `-l` | Base de patrones: `auto`, `C`, `C++`, `Assembly`, `C#`, `Python`, `JavaScript`, `Rust`. Con `auto` no hace falta `-l` si el argv ya deja claro la herramienta (p. ej. `make … cargo …`, `node`, `dotnet`). |
| `--verbose` | `-v` | Vuelca el log crudo en **stderr** antes del resumen. |
| `--full` | — | Salida extendida (separadores, bloques largos). |
| `--ub-hints` | — | Solo **C / C++ / Assembly**: sección UB-RISK si hay contexto; en otros lenguajes avisa que no aplica. |
| `--no-warnings` | `-nw` | Oculta advertencias explicadas y la sección de warnings sin patrón. |
| `--max-warnings` | — | Tope numérico para «Advertencias fuera de la base» (default 5). |
| `--match` | `-m` | Filtra bloques cuyo mensaje, ruta, título o símbolo contengan la subcadena. **Afecta** a `--man` y a los índices posicionales `E1`/`W1`/… (sobre listas ya filtradas). |
| `--shell` | — | Ejecuta una cadena con el shell del sistema; analiza stdout+stderr. **No** con `-i`. |
| `--count` | `-cnt` | Solo conteos; sin bloques de texto. |
| `--man` | `-f`, `-F` | Una o varias fichas (`E1`, `E1-2 W3`, …). Requiere **fuente de texto** (ver abajo). |
| `--man-all` | — | Todas las fichas con cápsula **manual** (`c_lang.py`, `handwritten_extra.py` y módulos enlazados; no sintéticas). |
| `--input-file` | `-i` | Lee el log desde archivo UTF-8. **No** con `--shell`. Tokens posicionales opcionales: pista de idioma (`cargo`, `npm`, …), no se ejecutan. |
| `--install-shell-completions` | — | Copia completions bash/zsh/fish al home (Unix); **termina**; sin comando. |

### Formas de invocación (fuente del log)

| Modo | Ejemplo | Notas |
|------|---------|--------|
| Comando posicional | `explain make iv` | Mezcla stdout+stderr del proceso. |
| Resumen solo ítem *n* | `explain E1 make iv` | Misma numeración que `--man`; salida **normal** (no ficha). Varios: `E1-2`, `E1 W2 make …`. |
| Tubería | `make iv 2>&1 \| explain` | stdin no es TTY. |
| Tubería + pista de idioma | `make iv 2>&1 \| explain --man E1 cargo` | El log sigue siendo el **stdin**; `cargo` (u otro token) solo infiere `--lang`, **no** se ejecuta. |
| Archivo | `explain -i build.log` | Sin `--shell`. |
| Archivo + pista | `explain -i build.log npm` | `npm` solo infiere `--lang`. |
| `--shell` | `explain --shell 'gcc -c a.c 2>&1'` | Una cadena; captura salida. |

Cualquier uso de **`--man` / `-f` / `-F` o `--man-all`** exige **una** de las filas anteriores (o TTY interactivo **sin** fuente → error explícito en stderr, exit 2).

### Combinaciones prohibidas o a tener en cuenta

| Combinación | Resultado |
|-------------|-----------|
| `--man` o `--man-all` con `-cnt` / `--count` | Error (exit 2), mensaje en stderr. |
| `--man` y `--man-all` a la vez | Error (exit 2). |
| `-i` con `--shell` | Error (exit 2). |
| ID posicional (`E1`…) con `--man-all` | Error (exit 2). |
| `--install-shell-completions` con comando posicional | Error (exit 2). |
| `--ub-hints` con `Python` / `Rust` / … | No activa UB; mensaje «no aplica» en salida. |
| `-m` + `--man` | Válido: índices E1, W2… son **después** del filtro. |

## Clonar el repo (desarrollo)

Para quien **clona** el proyecto y quiere venv, `pip install -e .` y **Tab completion** sin pasos manuales extra:

```bash
cd /ruta/al/repo
make dev
source .venv/bin/activate
```

`make dev` crea `.venv`, instala el paquete en modo editable y ejecuta **`explain --install-shell-completions`**, que copia bash/zsh/fish a `~/.local/share/bash-completion/`, `~/.zsh/completions/` y `~/.config/fish/completions/`. Abrí una terminal nueva o `source ~/.local/share/bash-completion/completions/explain` (bash).

**Sin Makefile:** `python3 -m venv .venv && .venv/bin/pip install -e . && .venv/bin/explain --install-shell-completions`

**direnv:** en el repo hay **`.envrc`**: con [direnv](https://direnv.net/) ejecutá `direnv allow`. Se añade `.venv/bin` al `PATH` si existe y, en **bash**, se **sourcea** `completions/explain.bash` al entrar al directorio (completions desde el clone, sin copiar al home).

## Linux, Windows, WSL y macOS (aula y uso personal)

El mismo código corre en **Linux**, **Windows** y **macOS**: sirve para corregir prácticas en el lab, en casa o en CI, siempre que haya Python.

- **Instalación recomendada:** entorno virtual + `pip install -e .` (ver abajo). En Windows el ejecutable queda en `.venv\Scripts\explain.exe`.
- **WSL:** tratá WSL como **Linux**: mismos comandos, tuberías y opción de `./install.sh` si querés `explain` en el PATH del distro y página **man**. El binario que compilás con `gcc`/`make` dentro de WSL es el de Linux; pasá la salida del build a `explain` igual que en una máquina nativa.
- **Tuberías:** en **PowerShell** podés usar `comando 2>&1 | explain` cuando el generador de salida mezcla stderr; en **cmd** igual con `2>&1`.
- **`--shell`:** en Windows usa el shell por defecto (**cmd**), no `sh -c`; pasá una cadena válida para ese entorno.
- **`install.sh`:** solo **Unix** (copia a `PREFIX`, man page). En Windows usá **pip**; la **man** no aplica salvo Git Bash/WSL con `man` configurado.

Los mensajes pueden traer rutas con `/` o `\`; la detección de lenguaje por rutas en el log normaliza `\` a `/` al inferir extensiones.

## Visión del proyecto, sin IA y con IA en el editor

**Sin modelos:** `explain` es una capa **determinista** sobre el texto del compilador: auditable, repetible y barata de ejecutar en cualquier máquina. Para quien programa **sin IA** es un glosario y una checklist en español al lado del terminal.

**Con IA (Cursor, Copilot, etc.):** encaja bien como **regla o hábito de flujo**: por ejemplo *“después de un build fallido, ejecutar `explain …` (o la tubería) y solo entonces pedir ayuda al asistente, pegando ya el resumen en español”*. Así la IA parte de **mensajes ya interpretados** y de secciones **Desconocidos / Advertencias fuera de la base** cuando haya que ampliar patrones, en lugar de adivinar sobre el crudo en inglés.

En conjunto, el sistema es **sólido para enseñanza y día a día**: no sustituye al compilador ni a sanitizers; **ordena** la salida, **prioriza** qué leer primero y **documenta** el criterio de `--ub-hints` para no confundir “no hubo indicios” con “no funcionó la opción”. La base de regex crece con el uso; cuanto más heterogéneo el entorno (Linux, Windows, WSL), más vale **tests en los dos sistemas** antes de publicar (ya indicado abajo).

## Novedades (resumen)

**0.6.7**

- **Cápsulas manuales al 100%** de la base actual: cada regex en `explain/patterns/` tiene ficha con ejemplos ❌/✅ en **C**, **C++**, **Assembly**, **Python**, **JavaScript**, **Rust** y **C#** (módulos nuevos o ampliados: `rust_capsules.py`, `cpp_capsules.py`, `c_capsules_gap.py`, más prioridad JS/TS y C#).
- **TypeScript:** más códigos `TSxxxx` en `js_ts.py` con fichas en `js_priority_capsules.py`.
- Documentación (`README`, `docs/CLI.md`, `man/explain.1`) alineada con la estructura de `explain/capsules/`.

**0.6.6**

- **Tabla del CLI** en este README (flags, entradas, combinaciones).
- **`--man` / `-f` / `-F`:** cápsula sintética también para **JavaScript**, **Rust** y **C#**.
- Más patrones en **Rust**, **JS/TS** y **C#** (errores/advertencias).

**0.6.5**

- Mensaje claro si usás **`--man` / `-f` sin log** (TTY sin tubería ni `-i` ni comando); antes parecía “solo help”.

**0.6.4**

- **`explain --install-shell-completions`:** instala bash/zsh/fish en el home (Unix).
- **`make dev`:** venv + editable + completions; **`.envrc`** opcional con direnv (bash + PATH venv).

**0.6.3**

- **`-f`:** alias de **`--man`** (junto con **`-F`**).
- **Cápsulas sintéticas** para **todo** patrón reconocido en **C**, **C++**, **Assembly** y **Python** al usar `--man` / `-f` / `-F`; **asm** hereda la misma base que C más `ERRORES_ASM` / `WARNINGS_ASM`.
- **`--man-all`:** aclarado: solo entradas **manuales** en `explain/capsules/`.

**0.6.2**

- **`--man` / `-F`:** varias fichas en una sola opción (`E1-2-5`, `E1/2/3`, `E1-2 W3 UB1`).

**0.6.1**

- **`-i` / `--input-file`**, **`--man-all`** (todas las fichas con cápsula); documentación del tubo correcto (`make … 2>&1 | explain --man …`).

**0.6.0**

- **`--man ID`:** fichas didácticas (E1, W2, UB1…); cápsulas ricas en `explain/capsules/c_lang.py` y `handwritten_extra.py`.

**0.5.0**

- **`--ub-hints`:** contexto también por **`[-W…]`**; pie de resumen; inferencia UB ampliada; aviso **no aplica** fuera de C/C++/Assembly.
- **Salida:** **Advertencias fuera de la base** vs **Desconocidos**; patrones C extra (**sign-conversion**, etc.).

## Documentación del CLI (comandos y salidas de ejemplo)

La referencia detallada con **ejemplos de entrada y salida esperada** está en **[docs/CLI.md](docs/CLI.md)**. Aquí solo un atajo:

```bash
explain make kernel.c
explain gcc -Wall main.c -o main
make iv 2>&1 | explain
printf '%s\n' 'f.c:1:1: error: conflicting types' | explain --lang C --man E1
make iv 2>&1 | explain -f 'E1-2 W3'
explain --man-all -i /tmp/build.log
explain --help
```

Tabla de opciones y casos (`--full`, `-m`, `-cnt`, `--ub-hints`, …): **[docs/CLI.md](docs/CLI.md)**.

## Instalación

### Entorno virtual (desarrollo o uso local)

```bash
cd /ruta/al/repo
python3 -m venv .venv
source .venv/bin/activate   # Linux / macOS
# Windows (cmd o PowerShell):  .venv\Scripts\activate
pip install -e .
explain --version
```

### Sistema (`/usr/local` o `/usr`) — Unix

Desde la raíz del repositorio:

```bash
sudo ./install.sh                    # default: PREFIX=/usr/local
sudo PREFIX=/usr ./install.sh        # explain en /usr/bin
sudo ./install.sh uninstall          # mismo PREFIX que al instalar
```

Instala el lanzador `explain`, los módulos bajo `PREFIX/share/explain-errors/` y la página **man** `explain.1`. Para actualizar, volvé a ejecutar `./install.sh`. En **Windows** usá solo **pip** (esta ruta no aplica).

### Completado en shell (flags y comandos)

En el repo hay **`completions/`** con soporte para **bash**, **zsh** y **fish**. Cubren las opciones del CLI (alineadas con `explain --help`), entre otras: `-h`/`--help`, `--version`, `-l`/`--lang`, `-v`/`--verbose`, `--full`, `--ub-hints`, `-nw`/`--no-warnings`, `--max-warnings`, `-m`/`--match`, `--shell`, `-cnt`/`--count`, **`-f` / `-F` / `--man`**, **`--man-all`**, **`-i` / `--input-file`**; valores de `--lang`; rutas tras `-i`; números típicos para `--max-warnings`; y **comandos del PATH** para lo que va después de las opciones. **Si tras un `git pull` Tab no muestra flags nuevos**, volvé a ejecutar `bash completions/install-bash-user.sh` y `source ~/.local/share/bash-completion/completions/explain`.

#### Bash (Ubuntu, GNOME Terminal, etc.)

1. **Shell:** tiene que ser **bash**, no zsh. Comprobá: `echo "$0"` o `ps -p $$`.
2. **Paquete del sistema:** hace falta **bash-completion** (sin eso, Tab casi nunca carga completions dinámicos):
   ```bash
   sudo apt install bash-completion
   ```
3. **Archivo con el nombre del comando:** el fichero en `~/.local/share/bash-completion/completions/` debe llamarse **`explain`**, no `explain.bash` (el cargador busca un archivo igual al comando).
4. **Instalación rápida** (desde la raíz del repo; **repetir tras actualizar el repo** para refrescar flags):
   ```bash
   bash completions/install-bash-user.sh
   ```
   O manual:
   ```bash
   mkdir -p ~/.local/share/bash-completion/completions
   cp completions/explain.bash ~/.local/share/bash-completion/completions/explain
   ```
5. **Nueva sesión:** cerrá y abrí GNOME Terminal, o `source ~/.bashrc`.
6. **Comprobación:** con **bash-completion**, el script en `~/.local/.../explain` suele cargarse **la primera vez** que escribís `explain ` y pulsás **Tab** (carga diferida). **Antes** de eso, `complete -p explain` puede responder *no hay especificación para completado* — no significa que falte el archivo.

   Para registrar **al instante** (recomendado tras instalar):
   ```bash
   source ~/.local/share/bash-completion/completions/explain
   complete -p explain   # ahora sí: complete -F _explain_complete explain
   ```

   También podés añadir esa línea `source .../explain` al final de `~/.bashrc` **después** de que se cargue bash-completion, si querés que exista siempre sin depender del primer Tab.

   ```bash
   type -a explain       # ejecutable del venv/pip
   ```

**Carga manual** (depurar): `source /ruta/al/repo/completions/explain.bash` (o el archivo en `~/.local/.../explain`) y probá `explain --` + Tab.

**Si usás `python3 -m explain`:** el autocompletado del repo solo registra el comando **`explain`**; para `python3 -m explain` hace falta otro hook o un alias `alias explain='python3 -m explain'` *después* de registrar el completion sobre `explain`.

- **Zsh**: copiá `_explain` a un directorio del `fpath` (p. ej. `~/.zsh/completions/`), luego:
  ```zsh
  fpath+=(~/.zsh/completions)
  autoload -Uz compinit && compinit
  ```

- **Fish**:
  ```fish
  cp completions/explain.fish ~/.config/fish/completions/explain.fish
  ```
  Fish solo ofrece opciones cortas de **una** letra; para el modo conteo usá **`--count`** (equivalente a **`-cnt`** de argparse en bash/zsh).

Tras **`pip install`** (wheel/sdist), los mismos archivos suelen quedar en  
`$(python -c 'import sysconfig; print(sysconfig.get_path("data"))')/share/explain-errors/completions/`  
(o el `data` de tu venv). **`install.sh`** también copia `completions/` a `$PREFIX/share/explain-errors/completions/`.

## Tests

Sin dependencias extra (`unittest` de la biblioteca estándar):

```bash
python3 -m unittest discover -s tests -v
```

Conviene ejecutarlos en **Linux y Windows** antes de publicar o en un pipeline CI (misma versión de Python en ambos).

## Lenguajes y patrones

Los patrones viven en **`explain/patterns/`**: núcleo por lenguaje (`python_lang.py`, `csharp.py`, `js_ts.py`, …), **Assembly** en `assembly.py` y `assembly_warnings.py` (x86 IA-32, x86-64, ARM 32‑bit / Thumb, AArch64), advertencias en `*_warnings.py`, y **frameworks** en `python_frameworks.py`, `csharp_frameworks.py` y `js_frameworks.py`. La búsqueda usa **`explain/pattern_index.py`** (regex compilados + índice por tokens).

Para ampliar la base: agregá o editá entradas en el módulo que corresponda; cada entrada es un **regex** con `titulo`, `explicacion` y `soluciones` (lista).

## Limitaciones (a propósito)

- No “entiende” código: solo **texto de salida** frente a **regex**.
- Mensajes raros o de toolchains nuevos caen en **desconocidos**: revisá ese apartado y sumá regex al módulo del lenguaje que ya usás.
- El mantenimiento es **manual**: cuanto más usés la herramienta, más vale ir nutriendo `explain/patterns/`.

## Ideas para seguir (sugerencias)

- **Depuración de base:** flag para listar títulos de patrones por `--lang`.
- **Windows:** completions o notas para **PowerShell** (Git Bash/WSL ya cubren mucho).
- **Más adelante:** salida `--json` / `-cnt` en JSON, código de salida configurable en CI, o **nuevos lenguajes** (Go, Java, …) con el mismo esquema `patterns/`.

## Estructura del repo (resumen)

```
explain/           # paquete Python
  cli.py           # argumentos, ejecución, formateo
  extract.py       # extracción de archivo:línea, funciones, etc.
  pattern_index.py # regex precompilados + índice invertido
  man_capsule.py   # parseo --man y texto de ficha
  shell_completions.py  # --install-shell-completions (bash/zsh/fish → home)
  capsules/        # --man: c_lang + c_capsules_extended + c_capsules_gap + asm + cpp_capsules; rust_capsules; handwritten_extra + python_priority + js_priority + csharp_capsules
  patterns/        # errores, *_warnings.py, *_frameworks.py, assembly*.py (x86/ARM)
Makefile           # make dev → venv + pip install -e . + install completions
.envrc             # opcional: direnv (PATH .venv + source completions en bash)
docs/              # CLI.md — ejemplos y salidas esperadas
tests/             # unittest (UB, analizar, --man, snippets, --help/--version)
completions/       # bash, zsh, fish + install-bash-user.sh
man/explain.1      # página de manual
LICENSE            # GNU GPL version 3 (texto completo)
COPYRIGHT          # aviso de copyright del proyecto
MANIFEST.in        # sdist: docs, tests, LICENSE, …
install.sh         # instalación en PREFIX
pyproject.toml     # metadatos, GPL-3.0, console_scripts y data-files de completions
```
