# explain-errors

**explain** traduce mensajes de compilación y ejecución al español usando **solo patrones en expresiones regulares** y textos fijos: **sin red ni modelos de lenguaje**. Es determinista y auditable: lo que explica está en el código.

**Autor:** Iván Ezequiel Rodriguez · versión actual: ver `pyproject.toml` o `explain --version`.

## Qué hace

- Ejecuta un comando (por ejemplo `make`, `gcc`, `dotnet`, `cargo`) y **mezcla stdout y stderr** del proceso hijo, así no hace falta acordarse de `2>&1` en ese modo.
- O lee la salida por **stdin** (tubería), por ejemplo `make iv 2>&1 | explain`.
- Detecta el **lenguaje** de la base de patrones (`auto`): herramienta invocada, extensiones en argumentos y en el log, y forma del mensaje.
- Extrae cuando puede **archivo:línea** y **función** (GCC, MSVC, Python, Node, TypeScript, etc.).
- Lista **errores sin patrón** como entradas numeradas *desconocido*, para que no queden “silencios” si el mensaje no está en la base.

## Requisitos

- Python **≥ 3.9**
- Sin dependencias externas (solo biblioteca estándar).

## Instalación

### Entorno virtual (desarrollo o uso local)

```bash
cd /ruta/al/repo
python3 -m venv .venv
source .venv/bin/activate   # o .venv\Scripts\activate en Windows
pip install -e .
explain --version
```

### Sistema (`/usr/local` o `/usr`)

Desde la raíz del repositorio:

```bash
sudo ./install.sh                    # default: PREFIX=/usr/local
sudo PREFIX=/usr ./install.sh        # explain en /usr/bin
sudo ./install.sh uninstall          # mismo PREFIX que al instalar
```

Instala el lanzador `explain`, los módulos bajo `PREFIX/share/explain-errors/` y la página **man** `explain.1`. Para actualizar, volvé a ejecutar `./install.sh`.

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
| `--warnings` | Incluye líneas `warning` al buscar patrones |
| `-m`, `--match` | Solo bloques cuyo mensaje, archivo, título o función contengan el texto |
| `--shell CMD` | Ejecuta `CMD` con `sh -c` (captura stdout+stderr) |

## Lenguajes y patrones

Los patrones viven en el paquete **`explain/patterns/`** (un módulo por familia: C, C++, ensamblador, C#, Python, JavaScript/TypeScript, Rust). Cada entrada es un **regex** asociado a título, explicación y lista de pasos sugeridos.

Para ampliar la base: agregá o editá entradas en el archivo del lenguaje que corresponda; no hace falta tocar la lógica del CLI salvo que quieras nuevos formatos de salida o detección.

## Limitaciones (a propósito)

- No “entiende” código: solo **texto de salida** frente a **regex**.
- Mensajes muy raros o de versiones nuevas del compilador pueden caer en **desconocido** hasta que alguien agregue un patrón.
- El mantenimiento es **manual**: cuanto más usés la herramienta, más vale ir nutriendo `explain/patterns/`.

## Estructura del repo (resumen)

```
explain/           # paquete Python
  cli.py           # argumentos, ejecución, formateo
  extract.py       # extracción de archivo:línea, funciones, etc.
  patterns/        # bases por lenguaje
install.sh         # instalación en PREFIX
man/explain.1      # página de manual
pyproject.toml     # metadatos y entrada console_scripts
```
