# explain-errors

**explain** traduce mensajes de compilación y ejecución al español usando **solo patrones en expresiones regulares** y textos fijos: **sin red ni modelos de lenguaje**. Es determinista y auditable: lo que explica está en el código.

**Autor:** Iván Ezequiel Rodriguez · **versión 0.3.0** (también en `pyproject.toml` y `explain --version`).

## Qué hace

- Ejecuta un comando (por ejemplo `make`, `gcc`, `dotnet`, `cargo`) y **mezcla stdout y stderr** del proceso hijo, así no hace falta acordarse de `2>&1` en ese modo.
- O lee la salida por **stdin** (tubería), por ejemplo `make iv 2>&1 | explain`.
- Detecta el **lenguaje** de la base de patrones (`auto`): herramienta invocada, extensiones en argumentos y en el log, y forma del mensaje.
- Extrae cuando puede **archivo:línea** y **función** (GCC, MSVC, Python, Node, TypeScript, etc.).
- Lista **errores sin patrón** como entradas numeradas *desconocido*, para que no queden “silencios” si el mensaje no está en la base.

## Requisitos

- Python **≥ 3.9**
- Sin dependencias externas (solo biblioteca estándar).

## Windows, Linux y macOS

El CLI es **multiplataforma**: mismo código en Windows, Linux y macOS. Tras `pip install` (editable o desde PyPI si publicás el paquete), el arranque `explain` lo genera setuptools como script en el `PATH` (en Windows suele ser `explain.exe` en `Scripts` del venv).

- **Tuberías**: en **PowerShell** podés hacer `make iv 2>&1 | explain` si `make` está en el PATH; en **cmd** también mezclá stderr con stdout antes de pipear (p. ej. `2>&1`).
- **`--shell`**: usa `shell=True` del sistema — en Windows es el shell por defecto (**cmd**), no `sh -c`; pasá una cadena válida para ese entorno.
- **`install.sh`**: solo **Unix** (copia a `PREFIX`, man page). En Windows instalá con **pip** (arriba); la página **man** no aplica salvo Git Bash/WSL con `man` configurado.

Los mensajes pueden traer rutas con `/` o `\`; la detección de lenguaje por rutas en el log normaliza `\` a `/` al inferir extensiones.

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

## Uso rápido

```bash
explain make kernel.c
explain make script.py
explain gcc -Wall main.c -o main
explain dotnet build
explain cargo build
```

**Tubería** (stderr del comando anterior hay que mezclarlo vos):

```bash
make iv 2>&1 | explain
make iv 2>&1 | explain > resumen.txt    # el resumen va al archivo; con -v el log completo va a stderr
```

**Filtrar** entradas por texto (mantiene el bloque completo *por qué* / *qué hacer*; mejor que `grep` sobre la salida):

```bash
explain make iv -m backup
```

**Ayuda y versión**

```bash
explain -h
explain --help
explain --version
man explain    # si instalaste con install.sh y MANPATH incluye share/man
```

## Opciones principales

| Opción | Descripción |
|--------|-------------|
| `-l`, `--lang` | `auto` (defecto), `C`, `C++`, `Assembly`, `C#`, `Python`, `JavaScript`, `Rust` |
| `-v`, `--verbose` | Vuelca la salida cruda en **stderr** antes del resumen |
| `--full` | Formato largo con separadores (por defecto: compacto) |
| `-nw`, `--no-warnings` | Oculta advertencias: ni bloques explicados ni listado de líneas con `warning` (por defecto **sí** se muestran, **después** de los errores) |
| `-m`, `--match` | Solo bloques que contengan el texto; en TTY resalta la subcadena en rojo (respeta `NO_COLOR`) |
| `--shell CMD` | Ejecuta `CMD` con el shell del sistema (`shell=True`; en Windows suele ser **cmd**) |

## Lenguajes y patrones

Los patrones viven en **`explain/patterns/`**: núcleo por lenguaje (`python_lang.py`, `csharp.py`, `js_ts.py`, …), **Assembly** en `assembly.py` y `assembly_warnings.py` (x86 IA-32, x86-64, ARM 32‑bit / Thumb, AArch64), advertencias en `*_warnings.py`, y **frameworks** en `python_frameworks.py`, `csharp_frameworks.py` y `js_frameworks.py`. La búsqueda usa **`explain/pattern_index.py`** (regex compilados + índice por tokens).

Para ampliar la base: agregá o editá entradas en el módulo que corresponda; cada entrada es un **regex** con `titulo`, `explicacion` y `soluciones` (lista).

## Limitaciones (a propósito)

- No “entiende” código: solo **texto de salida** frente a **regex**.
- Mensajes muy raros o de versiones nuevas del compilador pueden caer en **desconocido** hasta que alguien agregue un patrón.
- El mantenimiento es **manual**: cuanto más usés la herramienta, más vale ir nutriendo `explain/patterns/`.

## Estructura del repo (resumen)

```
explain/           # paquete Python
  cli.py           # argumentos, ejecución, formateo
  extract.py       # extracción de archivo:línea, funciones, etc.
  pattern_index.py # regex precompilados + índice invertido
  patterns/        # errores, *_warnings.py, *_frameworks.py, assembly*.py (x86/ARM)
install.sh         # instalación en PREFIX
man/explain.1      # página de manual
pyproject.toml     # metadatos y entrada console_scripts
```
