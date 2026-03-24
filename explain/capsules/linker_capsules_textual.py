# Cápsulas --man solo texto (sin ejemplos de código) para errores del enlazador.
# Claves = regex en explain/patterns/c_lang.py (familia C / C++ / Assembly).

from __future__ import annotations

from typing import Any


def _t(que: str, regla: str) -> dict[str, Any]:
    return {"que_paso": que, "regla": regla}


CAPSULES_LINKER_TEXTUAL: dict[str, dict[str, Any]] = {
    r"ld: cannot find (-l|lib)|/usr/bin/ld: cannot find (-l|lib)": _t(
        "El enlazador no encontró la biblioteca indicada con `-l` o la ruta a un `.so` / `.a`.",
        "Instalá el paquete `-dev`/SDK; usá `pkg-config --libs`; `-L` correcto y, con GCC, suele ayudar poner `-l` al final de la línea.",
    ),
    r"ld: skipping incompatible.*when searching for|/usr/bin/ld: skipping incompatible": _t(
        "Encontró un `.so` o `.a` pero no coincide con la arquitectura o ABI del enlace (p. ej. x86 vs x86_64, libc distinta).",
        "Limpiá e instalá build para el target correcto; revisá `file` sobre la biblioteca y variables de entorno de compilación cruzada.",
    ),
    r"relocation R_[A-Za-z0-9_]+.*(overflow|truncated)|ld:.*relocation.*overflow|cannot relocate": _t(
        "Una relocalización no cabe en el campo previsto (modelo de código PIC, distancia de salto, o objeto mal generado).",
        "Revisá `-fPIC`, `-mcmodel`, thunks del linker y que todos los `.o` usen el mismo ABI y flags de posición independiente.",
    ),
    r"DSO missing from command line|cannot load needed shared.*not found|needed by.*\.so": _t(
        "Falta en la línea de enlace una biblioteca compartida que otro `.so` necesita en tiempo de carga.",
        "Añadí el `-l` o la ruta del DSO dependiente; en algunos sistemas conviene `-Wl,--copy-dt-needed-entries` o enlazar explícitamente las dependencias (según política del proyecto).",
    ),
    r"ld:.*unrecognized option|ld\.bfd: unrecognized option|unrecognized option.*-Wl": _t(
        "El linker no entiende un flag pasado (a menudo vía `-Wl,...` desde gcc/clang).",
        "Separá flags de compilador vs linker; comprobá versión de `ld`/`lld`/`mold` y la sintaxis exacta en la documentación.",
    ),
    r"ld: cannot open output file|ld: cannot open .*: Permission denied|cannot open output file.*Permission denied": _t(
        "No se pudo crear o truncar el binario de salida (permisos, directorio inexistente o filesystem de solo lectura).",
        "Verificá ruta de `-o`, permisos y espacio en disco; no enlaces de salida bajo rutas protegidas sin permisos.",
    ),
    r"attempted static link of dynamic object|dynamic executable.*not allowed": _t(
        "Pedís enlace estático pero algún objeto o `-l` solo existe como compartido, o la política del toolchain lo prohíbe.",
        "Usá `.a` estáticos, `-static` con criterio, o enlazado dinámico; en glibc moderno el estático completo suele ser limitado.",
    ),
    r"hidden symbol.*referenced|undefined reference.*hidden symbol": _t(
        "Un símbolo con visibilidad hidden/local fue referenciado desde otra unidad de traducción o DSO.",
        "Revisá atributos `visibility`, mapas de versión del linker y qué objetos exportan el símbolo.",
    ),
    r"version `[^']*' not found|version node not found|not found \(required by": _t(
        "Falta una versión de símbolo o GLIBC/GLIBCXX que el binario o una dependencia exige.",
        "Compilá o enlazá contra sysroot/libs con la versión adecuada; en despliegue, la máquina destino debe tener esas versiones o usá contenedor/imagen alineada.",
    ),
    r"(ld\.lld|lld): error:|mold: (error|fatal):|gold: error:": _t(
        "El enlazador alternativo (LLVM lld, mold o gold) reportó un error explícito.",
        "Leé la línea anterior/siguiente del log: suele detallar símbolo, archivo o opción; compará con el mismo enlace usando `ld.bfd` si necesitás aislar el backend.",
    ),
    r"ld:.*file format not recognized|is not a recognized object file": _t(
        "El archivo que pasaste al linker no es un objeto ELF/COFF/Mach-O válido para esa herramienta (corrupto, texto, o target distinto).",
        "Regenerá el `.o`/`.a`; comprobá que no mezcles objetos de otra arquitectura o bitcode donde esperás objeto nativo.",
    ),
    r"discarded input section|undefined reference to linker script|memory region.*overflow": _t(
        "Linker script, `--gc-sections` o región de memoria: sección descartada que aún se referencia, o región FLASH/RAM excedida.",
        "Revisá el `.ld`, `KEEP()` para símbolos vitales y tamaños de segmentos en firmware embebido.",
    ),
}

__all__ = ["CAPSULES_LINKER_TEXTUAL"]
