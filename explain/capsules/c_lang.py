# Cápsulas escritas a mano para --man / --man-all (clave = regex exacta en explain/patterns/*).
# El resto de patrones C/C++/Assembly usan cápsula sintética en explain/capsules/__init__.py.

from __future__ import annotations

from typing import Any

_CAPSULES_C_MANUAL_CORE: dict[str, dict[str, Any]] = {
    r"conflicting types for": {
        "codigo_incorrecto": """// en foo.h
int foo(int a);
// en foo.c
void foo(int a) {
    (void)a;
}""",
        "codigo_correcto": """// mismo tipo de retorno y parámetros en .h y .c
int foo(int a);
int foo(int a) {
    return a * 2;
}""",
        "que_paso": (
            "El compilador vio un prototipo y una definición con firmas distintas "
            "(retorno o parámetros). En C eso es inválido: un solo símbolo `foo` "
            "debe tener una firma coherente en todo el programa."
        ),
        "regla": "El prototipo en el header y la definición en el .c deben coincidir exactamente.",
    },
    r"too few arguments to function": {
        "codigo_incorrecto": """void bar(int a, int b, int c);
void call(void) {
    bar(1, 2);  /* falta el tercer argumento */
}""",
        "codigo_correcto": """void bar(int a, int b, int c);
void call(void) {
    bar(1, 2, 3);
}""",
        "que_paso": (
            "La función está declarada con más parámetros de los que pasás en la llamada. "
            "Suele pasar tras cambiar la API y no actualizar todos los sitios que llaman."
        ),
        "regla": "Contá argumentos en la llamada y compará con el prototipo (orden y cantidad).",
    },
    r"too many arguments to function": {
        "codigo_incorrecto": """void baz(int x);
void call(void) {
    baz(1, 2);
}""",
        "codigo_correcto": """void baz(int x);
void call(void) {
    baz(1);
}""",
        "que_paso": "Pasás más expresiones de las que la función declara; el compilador las rechaza.",
        "regla": "Alineá la llamada con la firma: ni más ni menos argumentos (salvo variádicas).",
    },
    r"makes integer from pointer without a cast|makes pointer from integer without a cast": {
        "codigo_incorrecto": """/* llamada asume tipos que no coinciden con la firma real */
extern void f(int *p, int n);
void g(void) {
    int x = 0;
    f(&x, (char *)0);  /* mezcla puntero/entero según la firma real */
}""",
        "codigo_correcto": """#include <stdint.h>
void f(int *p, int n);
void g(void) {
    int x = 0;
    f(&x, 0);
}""",
        "que_paso": (
            "GCC advierte que un argumento mezcla puntero y entero respecto de lo que espera la función. "
            "Casi siempre indica que el prototipo y el uso no coinciden (o falta un cast explícito deliberado)."
        ),
        "regla": "Corregí primero conflicting types / too few arguments; usá uintptr_t si mezclás direcciones y enteros a propósito.",
    },
}

from explain.capsules.asm_lang import CAPSULES_ASM_HANDWRITTEN
from explain.capsules.c_capsules_extended import CAPSULES_C_EXTENDED
from explain.capsules.cpp_capsules import CAPSULES_CPP_HANDWRITTEN

CAPSULES_HANDWRITTEN_C_FAMILY: dict[str, dict[str, Any]] = {
    **_CAPSULES_C_MANUAL_CORE,
    **CAPSULES_C_EXTENDED,
    **CAPSULES_ASM_HANDWRITTEN,
    **CAPSULES_CPP_HANDWRITTEN,
}

# Compat: nombre histórico
CAPSULES_C = CAPSULES_HANDWRITTEN_C_FAMILY
