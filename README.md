# explain-errors

**explain** traduce mensajes de compilación y ejecución al español usando **solo patrones en expresiones regulares** y textos fijos: **sin red ni modelos de lenguaje**. Es determinista y auditable: lo que explica está en el código.

**Autor:** Iván Ezequiel Rodriguez · **versión 0.4.3** (también en `pyproject.toml` y `explain --version`).

**Licencia:** [GNU General Public License v3.0](LICENSE) (GPL-3.0). Resumen de copyright en [COPYRIGHT](COPYRIGHT).

## Qué hace

- Ejecuta un comando (por ejemplo `make`, `gcc`, `dotnet`, `cargo`) y **mezcla stdout y stderr** del proceso hijo, así no hace falta acordarse de `2>&1` en ese modo.
- O lee la salida por **stdin** (tubería), por ejemplo `make iv 2>&1 | explain`.
- Detecta el **lenguaje** de la base de patrones (`auto`): herramienta invocada, extensiones en argumentos y en el log, y forma del mensaje.
- Extrae cuando puede **archivo:línea** y **función** (GCC, MSVC, Python, Node, TypeScript, etc.).
- Apartado **Desconocidos (feedback)**: errores que parecen diagnósticos reales pero **no matchean** la base; se listan **en crudo** (copiar/pegar) para ir cargando patrones en `explain/patterns/` en versiones futuras, sin ampliar a nuevos lenguajes obligatoriamente.
- **`--ub-hints`** (solo **C**, **C++** y **Assembly**): la sección **«Posible comportamiento indefinido (indicios)»** solo se muestra si en el **comando** o en la **salida** aparece evidencia de **`-fsanitize`**, mensajes de **ASan/UBSan/TSan**, o flags **`-Wall` / `-Wextra` / `-Wpedantic` / `-Wconversion` / `-Wundef`** (o `CFLAGS`/`CXXFLAGS` con ellos). Si no hay esa evidencia, no se muestra nada extra (con `-v`, aviso en stderr). Incluye heurística **crash:** en la misma etiqueta **UB-RISK** cuando aplica. No analiza el código fuente.

## Requisitos

- Python **≥ 3.9**
- Sin dependencias externas (solo biblioteca estándar).

## Linux, Windows y macOS (aula y uso personal)

El mismo código corre en **Linux**, **Windows** y **macOS**: sirve para corregir prácticas en el lab, en casa o en CI, siempre que haya Python.

- **Instalación recomendada:** entorno virtual + `pip install -e .` (ver abajo). En Windows el ejecutable queda en `.venv\Scripts\explain.exe`.
- **Tuberías:** en **PowerShell** podés usar `comando 2>&1 | explain` cuando el generador de salida mezcla stderr; en **cmd** igual con `2>&1`.
- **`--shell`:** en Windows usa el shell por defecto (**cmd**), no `sh -c`; pasá una cadena válida para ese entorno.
- **`install.sh`:** solo **Unix** (copia a `PREFIX`, man page). En Windows usá **pip**; la **man** no aplica salvo Git Bash/WSL con `man` configurado.

Los mensajes pueden traer rutas con `/` o `\`; la detección de lenguaje por rutas en el log normaliza `\` a `/` al inferir extensiones.

## Documentación del CLI (comandos y salidas de ejemplo)

La referencia detallada con **ejemplos de entrada y salida esperada** está en **[docs/CLI.md](docs/CLI.md)**. Aquí solo un atajo:

```bash
explain make kernel.c
explain gcc -Wall main.c -o main
make iv 2>&1 | explain
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

En el repo hay **`completions/`** con soporte para **bash**, **zsh** y **fish** (cubren las opciones del CLI: `-l`/`--lang`, `-v`/`--verbose`, `--full`, `--ub-hints`, `-nw`, `--max-warnings`, `-m`/`--match`, `--shell`, `-cnt`/`--count`, `--version`, `-h`; valores de `--lang`; números típicos para `--max-warnings`; y **comandos del PATH** para lo que va después de las opciones).

- **Bash** (con [bash-completion](https://github.com/scop/bash-completion)): copiá el script con el nombre del comando:
  ```bash
  mkdir -p ~/.local/share/bash-completion/completions
  cp completions/explain.bash ~/.local/share/bash-completion/completions/explain
  ```
  Abrí una shell nueva o `source` el archivo. Sin bash-completion, podés `source /ruta/al/repo/completions/explain.bash`.

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
  patterns/        # errores, *_warnings.py, *_frameworks.py, assembly*.py (x86/ARM)
docs/              # CLI.md — ejemplos y salidas esperadas
tests/             # unittest (contexto UB, analizar, --help/--version)
completions/       # bash, zsh, fish
man/explain.1      # página de manual
LICENSE            # GNU GPL version 3 (texto completo)
COPYRIGHT          # aviso de copyright del proyecto
MANIFEST.in        # sdist: docs, tests, LICENSE, …
install.sh         # instalación en PREFIX
pyproject.toml     # metadatos, GPL-3.0, console_scripts y data-files de completions
```
