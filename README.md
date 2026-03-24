# explain-errors

**explain** es una utilidad de línea de comandos que **clasifica y explica en español** mensajes de compilación y ejecución a partir **únicamente del texto de salida**: cada diagnóstico se contrasta con una base de **expresiones regulares** y textos asociados en el repositorio. **No utiliza red ni modelos de lenguaje.** El resultado es **determinista** y **auditable**: la explicación proviene solo de código y datos versionados.

**Versión:** 0.6.8 (también en `pyproject.toml` y `explain --version`) · **Autor:** Iván Ezequiel Rodriguez · **Licencia:** [GPL-3.0](LICENSE) · **Copyright:** [COPYRIGHT](COPYRIGHT)

## Estado actual del sistema

| Componente | Descripción |
|------------|-------------|
| **Lenguajes soportados** | C, C++, Assembly, C#, Python, JavaScript (incluye salidas típicas de TypeScript/`tsc` en la base JS), Rust |
| **Base de patrones** | ~**1190** entradas (regex → título, explicación, soluciones) en `explain/patterns/`: núcleo por lenguaje, módulos `*_warnings.py`, `*_frameworks.py` y Assembly (varias ISAs en mensaje) |
| **Cápsulas didácticas** | Para cada clave de la base existe registro en `explain/capsules/` (fichas detalladas y entradas de cobertura amplia). Con `--man` / `-f` / `-F`, si un patrón no tuviera cápsula persistida, en lenguajes admitidos se usaría una ficha **sintética** generada desde la base; hoy la cobertura por clave está completa para los lenguajes anteriores |
| **`--man-all`** | Lista fichas usando **solo** cápsulas definidas en `explain/capsules/` (no sintéticas en memoria). Orden: errores, advertencias, ítems UB-RISK |
| **Emparejamiento** | `explain/pattern_index.py`: regex compilados, caché por identidad del diccionario de patrones, **índice invertido** por tokens alfanuméricos para acotar qué patrones se evalúan |
| **Extracción de contexto** | `explain/extract.py`: archivo, línea, columna, severidad y símbolo cuando el formato del log lo permite (p. ej. GCC/Clang, MSVC, trazas Python/Node/TS, Rust) |
| **`--ub-hints`** | Indicadores heurísticos de **posible comportamiento indefinido** solo para **C**, **C++** y **Assembly**, condicionados a señales en comando o salida (sanitizers, flags de advertencia, etiquetas `[-W…]`, etc.). En otros lenguajes la opción se **desactiva de forma explícita** en la salida. **No** inspecciona código fuente |
| **Entrega** | CLI (`explain.cli`), página **man**, completions **bash** / **zsh** / **fish**, tests (`unittest`, sin dependencias de terceros) |
| **Requisitos de ejecución** | Python **≥ 3.9**, solo biblioteca estándar |

## Funcionalidad (resumen)

- **Entrada:** ejecución de un comando posicional (stdout y stderr **mezclados**), tubería por **stdin**, archivo con **`-i` / `--input-file`**, o **`--shell`** con una cadena ejecutada en el shell del sistema.
- **Idioma de la base (`--lang` / `auto`):** inferencia a partir del ejecutable, otros tokens del argv, extensiones en rutas del log y forma del mensaje.
- **Salida principal:** resumen de errores y advertencias reconocidos, con ubicación cuando se pudo parsear; secciones de **retroalimentación** para diagnósticos que parecen válidos pero **no** tienen patrón (**Desconocidos** / **Advertencias fuera de la base**, con tope `--max-warnings`).
- **Índices posicionales (`explain E1 …`, `W2`, `UB1`, combinaciones):** misma numeración que `--man`, sobre la salida estándar del resumen (no abren ficha); compatibles con **`-m`** y **`-cnt`** según reglas del CLI.
- **`--man` / `-f` / `-F`:** fichas por índice; requieren fuente de log (comando, `-i` o stdin no interactivo). Detalle de flags y combinaciones prohibidas: tabla más abajo y **[docs/CLI.md](docs/CLI.md)**.

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
| `--man-all` | — | Todas las fichas del log usando cápsulas **persistidas** en `explain/capsules/` (excluye sintéticas generadas al vuelo). |
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

**Objetivos Make (desarrollo interno):** `make` o `make help` listan `dev`, `venv`, `install-editable`, `completions` y `test`.

`make dev` crea `.venv`, instala el paquete en modo editable y ejecuta **`explain --install-shell-completions`**, que copia bash/zsh/fish a `~/.local/share/bash-completion/`, `~/.zsh/completions/` y `~/.config/fish/completions/`. Abrí una terminal nueva o `source ~/.local/share/bash-completion/completions/explain` (bash).

**Sin Makefile:** `python3 -m venv .venv && .venv/bin/pip install -e . && .venv/bin/explain --install-shell-completions`

**direnv:** en el repo hay **`.envrc`**: con [direnv](https://direnv.net/) ejecutá `direnv allow`. Se añade `.venv/bin` al `PATH` si existe y, en **bash**, se **sourcea** `completions/explain.bash` al entrar al directorio (completions desde el clone, sin copiar al home).

## Linux, Windows, WSL y macOS

El mismo código corre en **Linux**, **Windows** y **macOS** con Python instalado; es apto para desarrollo local, entornos académicos y CI.

- **Instalación recomendada:** entorno virtual + `pip install -e .` (ver abajo). En Windows el ejecutable queda en `.venv\Scripts\explain.exe`.
- **WSL:** tratá WSL como **Linux**: mismos comandos, tuberías y opción de `./install.sh` si querés `explain` en el PATH del distro y página **man**. El binario que compilás con `gcc`/`make` dentro de WSL es el de Linux; pasá la salida del build a `explain` igual que en una máquina nativa.
- **Tuberías:** en **PowerShell** podés usar `comando 2>&1 | explain` cuando el generador de salida mezcla stderr; en **cmd** igual con `2>&1`.
- **`--shell`:** en Windows usa el shell por defecto (**cmd**), no `sh -c`; pasá una cadena válida para ese entorno.
- **`install.sh`:** solo **Unix** (copia a `PREFIX`, man page). En Windows usá **pip**; la **man** no aplica salvo Git Bash/WSL con `man` configurado.

Los mensajes pueden traer rutas con `/` o `\`; la detección de lenguaje por rutas en el log normaliza `\` a `/` al inferir extensiones.

## Posición respecto de otros flujos de trabajo

El diseño apunta a **trazabilidad**: mismo log de entrada → misma salida, sin servicios externos. En entornos con asistentes de código, el resumen en español y las secciones de **Desconocidos** / **Advertencias fuera de la base** sirven como **insumo estructurado** para ampliar patrones o depurar, sin sustituir al compilador ni a los sanitizers. La herramienta **prioriza** y **etiqueta** mensajes; la base de regex se mantiene **manualmente** y crece con el uso.

## Novedades (resumen)

**0.6.8**

- **Más patrones:** C (fatal OOM/escritura, enum duplicado, `void`/`sizeof`), advertencias GCC (`-Wshadow`, `-Wstrict-aliasing`, `-Wjump-misses-init`), C++ (destructor/ctor no accesible, `bad_function_call`), Python (`pickle`, SSL/TLS, `queue`, `zlib`), JS/TS (`fetch` fallido, TS2589, `dlopen`/addon, ESM vs script), Rust (E0584, E0728, E0794), C# (CS0171, CS8410), .NET (**MediatR**, **MassTransit**), ensamblador **AVR** y **Xtensa**.
- **Cápsulas:** módulo `explain/capsules/support_extension_capsules.py` enlazado desde `c_capsules_extended`, `cpp_capsules`, `asm_lang` y `handwritten_extra`.

**0.6.7**

- **Cobertura de cápsulas por clave:** cada regex de la base actual tiene entrada en `explain/capsules/` para **C**, **C++**, **Assembly**, **Python**, **JavaScript**, **Rust** y **C#** (núcleo curado más módulos de cobertura amplia: p. ej. `man_coverage_bulk.py`, gaps C/CPP/Asm, prioridades JS/C#/Python).
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

## Limitaciones

- No analiza código fuente: solo **texto de salida** frente a **regex**.
- Toolchains nuevos o mensajes poco frecuentes pueden quedar fuera de la base hasta incorporar patrones en `explain/patterns/`.
- El mantenimiento de la base y de las cápsulas es **manual** y depende del uso real del proyecto.

## Posibles extensiones

Ejemplos de evolución alineada con el modelo actual: salida estructurada (p. ej. JSON), más lenguajes o familias de mensajes con el mismo esquema `patterns/` + `capsules/`, o utilidades de inspección de la base por `--lang`. **Rendimiento:** con el volumen típico de logs y el índice actual, el cuello de botella suele ser E/S y no el motor de emparejamiento; optimizar el lookup tendría sentido ante **perfilado** o un crecimiento muy superior del número de patrones.

## Estructura del repo (resumen)

```
explain/           # paquete Python
  cli.py           # argumentos, ejecución, formateo
  extract.py       # extracción de archivo:línea, funciones, etc.
  pattern_index.py # regex precompilados + índice invertido
  man_capsule.py   # parseo --man y texto de ficha
  shell_completions.py  # --install-shell-completions (bash/zsh/fish → home)
  capsules/        # --man: c_lang, c_capsules_*, asm_lang, cpp_capsules, rust_capsules, handwritten_extra, *_priority, man_coverage_bulk, support_extension_capsules, etc.
  patterns/        # errores, *_warnings.py, *_frameworks.py, assembly*.py (x86/ARM)
Makefile           # make / make help → ayuda; make dev → venv + pip install -e . + completions
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
