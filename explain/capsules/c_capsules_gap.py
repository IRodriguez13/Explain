# Fichas --man para patrones C/Assembly que aún no tenían cápsula manual (huecos vs la base).

from __future__ import annotations

from typing import Any


def _(
    mal: str,
    bien: str,
    que: str,
    regla: str,
) -> dict[str, Any]:
    return {
        "codigo_incorrecto": mal,
        "codigo_correcto": bien,
        "que_paso": que,
        "regla": regla,
    }


CAPSULES_C_GAP: dict[str, dict[str, Any]] = {
    r"expected [\)\}] before|expected declaration|expected expression": _(
        "int f() { if (1) return 0 /* falta ; o bloque */",
        "if (1) { return 0; }",
        "El parser esperaba otro token: suele ser `;`, `)`, `}` o hay error en la línea anterior.",
        "Revisá la línea previa; balanceá `()` y `{}`; completá expresiones.",
    ),
    r"segmentation fault|SIGSEGV": _(
        "int *p = NULL; *p = 1;",
        "if (p) *p = 1;  // o no desreferenciar nullptr",
        "El proceso accedió a memoria inválida (nullptr, use-after-free, buffer overflow).",
        "GDB/AddressSanitizer; Valgrind; revisá punteros y límites de arrays.",
    ),
    r"UndefinedBehaviorSanitizer|\bUBSan\b|SUMMARY: UndefinedBehaviorSanitizer": _(
        "// compilado con -fsanitize=undefined",
        "Corregí el patrón que UBSan señala (shift, null, alignment)",
        "UBSan detectó comportamiento indefinido en runtime.",
        "Leé el tipo de informe UBSan y el backtrace; alineá con el estándar C.",
    ),
    r"ERROR: AddressSanitizer|AddressSanitizer:|SUMMARY: AddressSanitizer|\bASAN\b": _(
        "heap-use-after-free o buffer overflow",
        "Corregí lifetime y tamaños; -fsanitize=address en debug",
        "ASan detectó corrupción de memoria o uso ilegal.",
        "Stack trace y «READ/WRITE of size» indican el sitio aproximado.",
    ),
    r"\d+:\d+:\s*runtime error:": _(
        "UBSan: null pointer passed to …",
        "Eliminá la condición UB que el runtime reporta",
        "Runtime check (típico UBSan) falló con mensaje en archivo:línea.",
        "Mismo flujo que UBSan: corregí la operación inválida.",
    ),
    r"heap-buffer-overflow|stack-buffer-overflow|global-buffer-overflow|heap-use-after-free|stack-use-after-return|use-after-poison": _(
        "char b[4]; strcpy(b, \"demasiado\");",
        "Bounds checking; strncpy_s / snprintf según entorno",
        "Sanitizer: acceso fuera del buffer o uso tras liberación.",
        "Tamaños correctos, APIs seguras, ownership claro.",
    ),
    r"invalid type argument of|invalid operands to binary": _(
        "int *p; int x = *p + p;",
        "Operaciones con tipos compatibles y conversiones explícitas",
        "Operador aplicado a tipos que no lo soportan (sizeof mal usado, aritmética de punteros ilegal).",
        "Revisá tipos en la expresión señalada.",
    ),
    r"missing braces around initializer": _(
        "int a[2][2] = { 1, 2, 3, 4 };  // -Wmissing-braces",
        "int a[2][2] = { {1,2}, {3,4} };",
        "Inicializador de agregado ambiguo sin llaves internas.",
        "Anidá `{ }` para cada sub-agregado.",
    ),
    r"variable-sized object may not be initialized": _(
        "int n=3; int a[n] = {0};",
        "VLA sin inicializador agregado o usa malloc",
        "VLA en C no puede tener inicializador como array fijo.",
        "Inicializá en bucle o usá memoria dinámica.",
    ),
    r"continue statement not within a loop": _(
        "void f(void) { continue; }",
        "continue solo dentro de for/while/do",
        "`continue` fuera de bucle.",
        "Revisá llaves: a veces el `}` cerró el bucle antes del `continue`.",
    ),
    r"label.*referenced outside of any function": _(
        "goto fin;\nint main(void) { fin: return 0; }",
        "goto y label dentro de la misma función",
        "Etiqueta o `goto` mal anidados respecto de funciones.",
        "Labels solo dentro de una función; no cruces de función.",
    ),
    r"pointer from integer may be truncated": _(
        "void *p = (void *)0xFFFFFFFF;  // 32 vs 64 bit",
        "uintptr_t intermedio si es dirección entera deliberada",
        "Conversión entero→puntero puede perder bits en el target.",
        "`uintptr_t` y casts explícitos documentados.",
    ),
    r"discards? qualifiers? from pointer target type|passing argument.*discards": _(
        "void f(char *s); const char *c=\"x\"; f(c);",
        "void f(const char *s); o cast solo si quitás const con criterio",
        "Pasás `const T*` donde se espera `T*` (se pierde const).",
        "Firma con `const` o copia mutable.",
    ),
    r"array subscript has type char": _(
        "char i = 2; int a[10]; a[i] = 0;",
        "size_t o int sin signo para índices",
        "`char` como subíndice puede ser negativo al promoverse.",
        "Usá tipo entero sin signo o `size_t` para índices.",
    ),
    r"overflow in constant expression": _(
        "enum { A = INT_MAX, B = A + 1 };",
        "Valores dentro del rango representable",
        "Desbordamiento en expresión constante (enum, static assert implícito).",
        "Rangos de `int`; `unsigned` o valores más pequeños.",
    ),
    r"division by zero": _(
        "int x = 1/0;",
        "Guarda if (d != 0) antes de dividir",
        "División o módulo por cero en tiempo de compilación o constante.",
        "Evitá divisor cero; en runtime comprobá antes.",
    ),
    r"unreachable code|will never be executed": _(
        "return 0; printf(\"x\");",
        "Eliminá código muerto",
        "Código tras `return`/`exit`/bucle infinito.",
        "Limpieza o corregí el flujo lógico.",
    ),
    r"unused variable|set but not used|defined but not used": _(
        "int x = 1; (void)x;",
        "(void)x; o eliminá x; o (void) cast en parámetro",
        "Variable o parámetro no usado (warning).",
        "Eliminá, prefijo omitido con `(void)`, o `__attribute__((unused))` si aplica.",
    ),
    r"nested redefinition|error in included file": _(
        "#include \"bad.h\"  /* error dentro */",
        "Corregí el header o el orden de includes",
        "El error real está en un archivo incluido (anidado).",
        "Mirá la pila de includes en el mensaje del compilador.",
    ),
    r"fatal error: no input files|fatal error:": _(
        "gcc -o a.out",
        "gcc -o a.out main.c",
        "gcc/clang sin fuentes o error fatal de driver.",
        "Pasá `.c` o revisá la línea de comando generada por make.",
    ),
    r"cannot specify -o with -c, -S or -E with multiple files": _(
        "gcc -c a.c b.c -o out.o",
        "gcc -c a.c -o a.o && gcc -c b.c -o b.o",
        "Un solo `-o` no puede nombrar varias salidas con `-c`.",
        "Compilá por archivo o sin `-o` múltiple incompatible.",
    ),
    r"case label not within a switch statement|default label not within a switch": _(
        "case 1: break;",
        "switch (x) { case 1: break; }",
        "`case`/`default` fuera de `switch` (llaves mal puestas).",
        "Envolvé los `case` dentro de `switch { }`.",
    ),
    r"break statement not within loop or switch|continue statement not within a loop": _(
        "void f(void) { break; }",
        "break dentro de switch o loop correspondiente",
        "`break`/`continue` sin contenedor válido.",
        "Revisá dónde cerró el `switch`/`for`/`while`.",
    ),
    r"lvalue required as unary '&' operand|lvalue required as left operand of assignment": _(
        "&(a+b)",
        "Guardá en variable y tomá su dirección",
        "No podés tomar dirección o asignar a un rvalue.",
        "Usá variable nombrada o puntero ya existente.",
    ),
    r"warning:.*unused function": _(
        "static void helper(void) {}",
        "Eliminá, usá, o static inline en header con criterio",
        "Función estática nunca llamada.",
        "Código muerto o falta integrar la llamada.",
    ),
    r"warning:.*unused but set variable|warning:.*set but not used": _(
        "int x = 1; x = 2;",
        "int x = 2;",
        "Asignación cuyo valor anterior no se leyó.",
        "Simplificá o leé el valor intermedio si era necesario.",
    ),
    r"warning:.*ignored-qualifiers": _(
        "const int f(void);  // const en tipo de retorno void/int",
        "Quita const meaningless en el retorno",
        "Calificador sin efecto en ese contexto (p. ej. const en valor retornado por copia trivial).",
        "Ajustá la firma según el compilador indica.",
    ),
    r"ld: warning:.*cannot find entry symbol": _(
        "ld … sin _start o main según el tipo de enlace",
        "Proveé crt0/main o flags de enlace correctos para hosted/freestanding",
        "El enlazador no encuentra símbolo de entrada (entry point).",
        "Objetos de arranque (`crt`), `-nostdlib` vs programa con `main`.",
    ),
    r"warning:.*discarded-qualifiers": _(
        "const char *p; char *q = p;",
        "char const * coherente o cast explícito documentado",
        "Se descarta `const` u otro calificador en la conversión implícita.",
        "Propagá `const` o copia a buffer mutable.",
    ),
}

__all__ = ["CAPSULES_C_GAP"]
