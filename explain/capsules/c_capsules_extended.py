# Fichas didácticas extra para C (y salida compartida C++/Assembly): claves = explain/patterns/c_lang.py y c_warnings.py.

from __future__ import annotations

from typing import Any

from explain.capsules.c_capsules_gap import CAPSULES_C_GAP
from explain.capsules.support_extension_capsules import (
    CAPSULES_SUPPORT_C,
    CAPSULES_SUPPORT_C_WARN,
)

CAPSULES_C_EXTENDED: dict[str, dict[str, Any]] = {
    r"dereferencing pointer to incomplete type": {
        "codigo_incorrecto": """/* foo.h */
struct Op; /* solo forward */
void use(struct Op *p);

/* foo.c */
void use(struct Op *p) {
    p->x = 1;  /* error: incompleto */
}""",
        "codigo_correcto": """/* foo.h */
struct Op { int x; };
void use(struct Op *p);""",
        "que_paso": "Solo conocés el struct por nombre; el compilador no sabe el layout ni los miembros.",
        "regla": "Incluí el header con la definición completa antes de usar `->` o `.`; o ocultá el layout con API opaca y funciones accessor.",
    },
    r"invalid use of undefined type|invalid use of incomplete type": {
        "codigo_incorrecto": """struct T; /* incompleto */
struct T a;  /* tamaño desconocido */""",
        "codigo_correcto": """struct T { int x; };
struct T a;""",
        "que_paso": "Instanciás o copiás un tipo del que solo existe declaración adelantada.",
        "regla": "Definí el struct/union completo o usá puntero `struct T *` hasta tener la definición.",
    },
    r"implicit declaration of function": {
        "codigo_incorrecto": """int main(void) {
    printf("hola\\n");
    return 0;
}""",
        "codigo_correcto": """#include <stdio.h>
int main(void) {
    printf("hola\\n");
    return 0;
}""",
        "que_paso": "Llamás a una función sin prototipo visible; en C moderno es error (antes asumía retorno int).",
        "regla": "Siempre `#include` del header correcto o prototipo `extern` antes del uso; activá `-Werror=implicit-function-declaration`.",
    },
    r"undefined reference to": {
        "codigo_incorrecto": """/* main.c llama foo(); foo.c no se enlaza */
gcc -o prog main.o""",
        "codigo_correcto": """gcc -o prog main.o foo.o
# o: gcc main.c foo.c -o prog""",
        "que_paso": "El enlazador no encuentra la definición del símbolo (función o variable global).",
        "regla": "Pasá todos los `.o`/`.a`; `-lfoo` al final en muchos linkers; verificá `static` que oculte el símbolo.",
    },
    r"multiple definition of|first defined here": {
        "codigo_incorrecto": """/* dos .c definen la misma función global no-static */
int add(int a, int b) { return a + b; }""",
        "codigo_correcto": """/* un solo .c con la definición; en .h: */
static inline int add(int a, int b) { return a + b; }
/* o declaración en .h y definición en un .c */""",
        "que_paso": "El mismo símbolo global está definido en más de una TU enlazada.",
        "regla": "Una definición; en headers usá `static inline`, `extern` + una definición, o include guards sin definir funciones dos veces.",
    },
    r"expected ';' before": {
        "codigo_incorrecto": """struct Point { int x int y; };""",
        "codigo_correcto": """struct Point { int x; int y; };""",
        "que_paso": "El parser se perdió; el mensaje a menudo apunta a la línea siguiente al error real.",
        "regla": "Revisá la línea anterior: `;` tras miembros de struct, `)`, `}`; macros multilínea.",
    },
    r"incompatible pointer type|incompatible types when": {
        "codigo_incorrecto": """int *p;
char *q = p;  /* sin cast explícito donde no es válido */""",
        "codigo_correcto": """void *vp = (void *)p;  /* si es deliberado */
/* o unificá el tipo real del puntero */""",
        "que_paso": "Mezclás punteros de tipos incompatibles sin conversión explícita permitida.",
        "regla": "Usá `void *` como intermedio solo donde el estándar lo permite; casteá con criterio y documentación.",
    },
    r"storage size of .* isn't known": {
        "codigo_incorrecto": """struct X; /* incompleto */
sizeof(struct X)""",
        "codigo_correcto": """struct X { char a; };
sizeof(struct X)""",
        "que_paso": "Aplicás `sizeof` o declarás variable de un tipo incompleto.",
        "regla": "Incluí la definición completa del tipo antes de medirlo o instanciarlo.",
    },
    r"lvalue required as|lvalue required": {
        "codigo_incorrecto": """int a = 1, b = 2;
(a + b) = 3;""",
        "codigo_correcto": """int a = 1, b = 2;
a = 3;""",
        "que_paso": "Asignás o tomás `&` de una expresión que no es un objeto modificable.",
        "regla": "Usá variable intermedia; no asignes al resultado de una función (salvo que retorne puntero asignable válido).",
    },
    r"called object .* is not a function or function pointer": {
        "codigo_incorrecto": """int x = 0;
x();""",
        "codigo_correcto": """void (*fp)(void) = mi_funcion;
fp();""",
        "que_paso": "El nombre entre `()` no es función ni puntero a función (macro, variable, typo).",
        "regla": "Revisá `#define`, typedef de puntero a función, y que no hayas pisado el identificador.",
    },
    r"subscripted value is neither array nor pointer": {
        "codigo_incorrecto": """struct S { int x; } s;
s[0] = 1;""",
        "codigo_correcto": """int a[10];
a[0] = 1;""",
        "que_paso": "Usás `[]` sobre algo que no es array ni puntero.",
        "regla": "Para struct usá `.`/`->`; el array decae a puntero solo en contextos adecuados.",
    },
    r"format .* expects argument|too many arguments for format": {
        "codigo_incorrecto": """printf("%d %d", 1);""",
        "codigo_correcto": """printf("%d %d", 1, 2);
/* size_t: %zu con <stddef.h> */""",
        "que_paso": "Cantidad o tipos de argumentos no coinciden con los especificadores de `printf`/`scanf` → UB.",
        "regla": "Un `%` por argumento; `size_t` → `%zu`; usá macros `PRI*` de `<inttypes.h>` para enteros fijos.",
    },
    r"void value not ignored as it ought to be": {
        "codigo_incorrecto": """int x = puts("hi");""",
        "codigo_correcto": """puts("hi");""",
        "que_paso": "Usás el valor de retorno de una función `void` en una expresión.",
        "regla": "Llamá funciones void como sentencia sola; si necesitás estado, cambiá la API.",
    },
    r"function returns address of local variable": {
        "codigo_incorrecto": """int *bad(void) {
    int x = 42;
    return &x;
}""",
        "codigo_correcto": """static int storage;
int *ok(void) {
    storage = 42;
    return &storage;
}""",
        "que_paso": "Devolvés puntero a automática que deja de existir al salir de la función → uso colgante.",
        "regla": "`static` local, `malloc` (documentando dueño), o buffer pasado por el llamador.",
    },
    r"control reaches end of non-void function": {
        "codigo_incorrecto": """int sign(int x) {
    if (x < 0) return -1;
    if (x > 0) return 1;
}""",
        "codigo_correcto": """int sign(int x) {
    if (x < 0) return -1;
    if (x > 0) return 1;
    return 0;
}""",
        "que_paso": "Algún camino de una función con valor de retorno no ejecuta `return`.",
        "regla": "Cubrí todos los caminos; `return` por defecto o `assert(0)` en ramos imposibles documentados.",
    },
    r"linker command failed|collect2: error: ld returned \d+ exit status": {
        "codigo_incorrecto": """# undefined reference / multiple definition arriba en el log""",
        "codigo_correcto": """# corregí símbolos; orden de -l; rutas -L""",
        "que_paso": "`collect2`/`ld` falló; el motivo concreto suele estar unas líneas antes.",
        "regla": "Buscá `undefined reference` y `multiple definition`; poné `-l` al final con gcc.",
    },
    r"unknown type name": {
        "codigo_incorrecto": """uint32_t x = 0;""",
        "codigo_correcto": """#include <stdint.h>
uint32_t x = 0;""",
        "que_paso": "El nombre de tipo no está definido (typo o falta de include/typedef).",
        "regla": "Incluí el header estándar o `typedef struct` antes del uso.",
    },
    r"redefinition of|redeclared": {
        "codigo_incorrecto": """int x = 1;
int x = 2;""",
        "codigo_correcto": """int x = 1;
x = 2;""",
        "que_paso": "Redefinición en el mismo ámbito o conflicto entre declaraciones.",
        "regla": "Include guards / `#pragma once`; `static` en `.c` para símbolos internos.",
    },
    r"initialization makes pointer from integer without a cast": {
        "codigo_incorrecto": """void *p = 0x1000;  /* en C requiere cast explícito desde entero */""",
        "codigo_correcto": """void *p = (void *)(uintptr_t)0x1000;""",
        "que_paso": "Inicializás puntero desde constante entera sin conversión explícita (C es estricto).",
        "regla": "Usá `(void *)(uintptr_t)` para direcciones numéricas en código embebido; en userspace suele ser señal de diseño dudoso.",
    },
    r"incompatible pointer to integer conversion|incompatible integer to pointer conversion": {
        "codigo_incorrecto": """uintptr_t u = (uintptr_t)"literal";  /* en algunos diagnósticos mezcla puntero/entero */""",
        "codigo_correcto": """const char *s = "literal";
uintptr_t u = (uintptr_t)(void *)s;""",
        "que_paso": "Clang/GCC rechazan mezcla puntero/entero sin el cast adecuado.",
        "regla": "Cadena de casts documentada vía `void *` y `uintptr_t`/`intptr_t`.",
    },
    r"request for member.*in something not a structure or union": {
        "codigo_incorrecto": """int x = 3;
x.y = 1;""",
        "codigo_correcto": """struct S { int y; } s;
s.y = 1;""",
        "que_paso": "Usás `.` o `->` sobre un valor que no es struct/union (o confundís `*` con `->`).",
        "regla": "Si es puntero usá `->`; verificá tipo real tras casts y typedefs.",
    },
    r"assignment .* makes pointer from integer": {
        "codigo_incorrecto": """int *p = 10;""",
        "codigo_correcto": """int x = 10;
int *p = &x;""",
        "que_paso": "Asignás entero a puntero sin cast intencional (casi siempre bug).",
        "regla": "Usá `&` o cast explícito solo en hardware/mapas de memoria con documentación.",
    },
    r"comparison of distinct pointer types|comparison between pointer and integer": {
        "codigo_incorrecto": """int *p;
if (p == 1) { }""",
        "codigo_correcto": """if (p == NULL) { }""",
        "que_paso": "Comparás puntero con entero o punteros de tipos incompatibles sin conversión clara.",
        "regla": "Compará con `NULL`; para direcciones numéricas usá `uintptr_t`.",
    },
    r"excess elements in struct initializer": {
        "codigo_incorrecto": """struct { int a; } s = {1, 2};""",
        "codigo_correcto": """struct { int a; } s = {1};""",
        "que_paso": "Más valores en el inicializador que campos en el struct.",
        "regla": "Contá campos; usá designadores `.campo =` en C99.",
    },
    r"case label not within a switch": {
        "codigo_incorrecto": """if (1) {
  case 0: break;
}""",
        "codigo_correcto": """switch (x) {
  case 0: break;
}""",
        "que_paso": "`case` quedó fuera de un `switch` (llaves mal balanceadas).",
        "regla": "Revisá dónde cerraste el `switch` y los `if` externos.",
    },
    r"break statement not within loop or switch": {
        "codigo_incorrecto": """void f(void) {
  break;
}""",
        "codigo_correcto": """void f(void) {
  return;
}""",
        "que_paso": "`break` solo es válido dentro de `for`/`while`/`do`/`switch`.",
        "regla": "Si querías salir de función usá `return`; revisá llaves extra.",
    },
    r"duplicate case value": {
        "codigo_incorrecto": """switch (x) {
  case 1: break;
  case 1: break;
}""",
        "codigo_correcto": """switch (x) {
  case 1:
  case 2: break;
}""",
        "que_paso": "Dos `case` con la misma constante.",
        "regla": "Fusioná casos o corregí valores duplicados por error.",
    },
    r"enumerator value for .* is not an integer constant": {
        "codigo_incorrecto": """int x = 1;
enum E { A = x };""",
        "codigo_correcto": """enum E { A = 1, B = 2 };""",
        "que_paso": "En C los valores de enum deben ser constantes enteras en tiempo de compilación.",
        "regla": "Usá literales o `#define`; en C++ las reglas difieren ligeramente.",
    },
    r"flexible array member|invalid use of flexible array member": {
        "codigo_incorrecto": """struct H {
    int n;
    int items[]; /* FAM */
    int tail; /* ilegal: nada después del FAM */
};""",
        "codigo_correcto": """struct H {
    int n;
    int items[]; /* último miembro */
};
/* malloc(sizeof(struct H) + n*sizeof(int)) */""",
        "que_paso": "El miembro flexible `[]` solo puede ser el último y tiene reglas estrictas.",
        "regla": "Patrón header + `malloc` del tamaño total; no pongas campos después del FAM.",
    },
    r"initializer element is not constant": {
        "codigo_incorrecto": """int f(void) { return 1; }
static int x = f();""",
        "codigo_correcto": """static int x = 42;
/* o inicializá en función al arranque */""",
        "que_paso": "Objetos con almacenamiento estático requieren inicializadores constantes en C.",
        "regla": "Asigná en `main`/constructor de arranque o usá solo expresiones constantes.",
    },
    r"cannot compute sizeof|invalid application of 'sizeof'": {
        "codigo_incorrecto": """struct Opaque;
sizeof(struct Opaque)""",
        "codigo_correcto": """/* incluí definición completa o sizeof sobre puntero */
sizeof(struct Opaque *)""",
        "que_paso": "`sizeof` de tipo incompleto o uso no permitido.",
        "regla": "Incluí el header completo o usá `sizeof *p` cuando `p` es puntero a incompleto (tamaño del puntero).",
    },
    r"variable has incomplete type|field has incomplete type": {
        "codigo_incorrecto": """struct A; /* incompleto */
struct B { struct A a; };""",
        "codigo_correcto": """struct A { int x; };
struct B { struct A a; };""",
        "que_paso": "Campo o variable de tipo cuya definición no está visible.",
        "regla": "Reordená includes o usá puntero `struct A *` en el struct contenedor.",
    },
    # --- Advertencias C (WARNINGS_C) ---
    r"warning:.*implicit declaration of function": {
        "codigo_incorrecto": """void g(void) {
    strlen("abc");
}""",
        "codigo_correcto": """#include <string.h>
void g(void) {
    strlen("abc");
}""",
        "que_paso": "Se usó una función sin prototipo; en compiladores modernos suele acabar en error.",
        "regla": "Incluí el `.h` estándar correspondiente o declará `extern` antes del uso.",
    },
    r"warning:.*incompatible implicit conversion": {
        "codigo_incorrecto": """double d = 3.7;
int x = d;  /* truncamiento implícito */""",
        "codigo_correcto": """double d = 3.7;
int x = (int)d;""",
        "que_paso": "Conversión implícita entre tipos que puede perder información o ser sorprendente.",
        "regla": "Cast explícito documentado o cambiá el tipo de la variable destino.",
    },
    r"warning:.*unused variable": {
        "codigo_incorrecto": """void f(void) {
    int tmp = 42;
}""",
        "codigo_correcto": """void f(void) {
    (void)0; /* o usá tmp, o eliminá */
}""",
        "que_paso": "Variable declarada y nunca leída (código muerto u olvido).",
        "regla": "Eliminá, usala, o `(void)tmp` / `__attribute__((unused))` si es intencional.",
    },
    r"warning:.*unused parameter": {
        "codigo_incorrecto": """void cb(void *ctx) { }""",
        "codigo_correcto": """void cb(void *ctx) { (void)ctx; }
/* o void cb(void *_ctx) con nombre omitido en C23 / patrón _ctx */""",
        "que_paso": "Parámetro de callback no usado pero la firma es fija.",
        "regla": "Prefijo `_` o `(void)param` para silenciar el warning con claridad.",
    },
    r"warning:.*sign-compare": {
        "codigo_incorrecto": """int i = -1;
size_t n = 10;
if (i < n) { } /* i se promueve a grande */""",
        "codigo_correcto": """int i = -1;
size_t n = 10;
if (i < 0 || (size_t)i < n) { }""",
        "que_paso": "`int` negativo comparado con `size_t` se convierte a un valor enorme.",
        "regla": "Unificá tipos o comprobá `i < 0` antes de comparar con unsigned.",
    },
    r"warning:.*sign-conversion|warning:.*may change the sign of the result": {
        "codigo_incorrecto": """unsigned u = 2;
int s = -1;
int x = u * s;""",
        "codigo_correcto": """/* forzá tipos explícitos o unsigned en toda la expresión coherente */""",
        "que_paso": "Mezcla signed/unsigned en aritmética o asignación puede cambiar signo o magnitud de forma no obvia.",
        "regla": "Unificá con `size_t`/signed explícito; casts documentados en fronteras.",
    },
    r"warning:.*format .* expects": {
        "codigo_incorrecto": """size_t z = 1;
printf("%d", z);""",
        "codigo_correcto": """#include <stddef.h>
size_t z = 1;
printf("%zu", z);""",
        "que_paso": "`printf` con especificador que no coincide con el tipo → UB o salida basura.",
        "regla": "Emparejá cada `%` con el tipo real (`%zu`, `%p`, `PRIu32`, etc.).",
    },
    r"warning:.*fallthrough": {
        "codigo_incorrecto": """switch (c) {
  case 'a':
    do_a();
  case 'b':
    do_b();
    break;
}""",
        "codigo_correcto": """switch (c) {
  case 'a':
    do_a();
    break;
  case 'b':
    do_b();
    break;
}""",
        "que_paso": "El control cae de un `case` al siguiente sin `break` (a veces intencional, a menudo bug).",
        "regla": "Añadí `break` o comentario/`[[fallthrough]]` explícito según compilador.",
    },
    r"warning:.*pointer.*integer": {
        "codigo_incorrecto": """void *p;
uintptr_t u = p;  /* en algunos flags sin conversión explícita */""",
        "codigo_correcto": """void *p;
uintptr_t u = (uintptr_t)p;""",
        "que_paso": "Conversión entre puntero y entero sin claridad (portabilidad y ASan).",
        "regla": "Usá `uintptr_t`/`intptr_t` y casts explícitos documentados.",
    },
    r"warning:.*deprecated": {
        "codigo_incorrecto": """/* gets(buf); — obsoleto y peligroso */""",
        "codigo_correcto": """/* fgets(buf, sizeof buf, stdin); */""",
        "que_paso": "API marcada obsoleta; puede eliminarse en futuras versiones.",
        "regla": "Migrá a la API recomendada en el mensaje o en la documentación.",
    },
    r"warning:.*may be used uninitialized": {
        "codigo_incorrecto": """int x;
if (cond) x = 1;
return x;""",
        "codigo_correcto": """int x = 0;
if (cond) x = 1;
return x;""",
        "que_paso": "Hay un camino donde se lee la variable sin asignar antes.",
        "regla": "Inicializá al declarar o asigná en todas las ramas antes del uso.",
    },
    r"warning:.*strict-aliasing": {
        "codigo_incorrecto": """float f;
*(int *)&f = 0x3f800000;""",
        "codigo_correcto": """#include <string.h>
float f;
uint32_t bits = 0x3f800000;
memcpy(&f, &bits, sizeof f);""",
        "que_paso": "Accedés a los mismos bytes como tipos distintos; el optimizador puede asumir que no pasa.",
        "regla": "`memcpy` para reinterpretar bits; `char*` para inspección byte a byte; union con cautela.",
    },
    r"warning:.*\[-Wsequence-point\]|warning:.*operation on .*may be undefined|warning:.*unsequenced|warning:.*multiple unsequenced": {
        "codigo_incorrecto": """int i = 0;
i = i++ + 1;""",
        "codigo_correcto": """int i = 0;
i += 1;
i += 1;""",
        "que_paso": "Dos efectos secundarios sin punto de secuencia definido entre ellos → UB en C.",
        "regla": "Separá en sentencias; no combines `++` con otra modificación del mismo objeto en una expresión.",
    },
    r"warning:.*undefined behavior|note:.*undefined behavior": {
        "codigo_incorrecto": """int a[10];
a[10] = 0;""",
        "codigo_correcto": """int a[10];
a[9] = 0;""",
        "que_paso": "El compilador detecta un patrón explícitamente indefinido según el estándar.",
        "regla": "Corregí índices y aritmética; usá ASan/UBSan en depuración.",
    },
    r"warning:.*left shift of negative|warning:.*right shift of negative|warning:.*shift count >=|warning:.*shift count.*width|warning:.*negative.*shift": {
        "codigo_incorrecto": """int x = -1;
int y = x << 1;""",
        "codigo_correcto": """unsigned x = 3;
unsigned y = x << 1;""",
        "que_paso": "Shift de signed negativo o recuento fuera de rango → UB en C.",
        "regla": "Usá unsigned para operaciones de bits; acotá el shift con comprobación.",
    },
    r"warning:.*dereferencing.*type-punned|type-punned pointer will break strict-aliasing": {
        "codigo_incorrecto": """float f = 1.0f;
int *ip = (int *)&f;
*ip = 0;""",
        "codigo_correcto": """/* memcpy entre float e uint32_t como arriba */""",
        "que_paso": "Type-punning con punteros de tipos incompatibles rompe strict-aliasing.",
        "regla": "`memcpy` o `char*` para bytes; no dos punteros activos a distinto tipo sobre el mismo objeto.",
    },
    r"warning:.*overflow": {
        "codigo_incorrecto": """int a = INT_MAX;
int b = a + 1;""",
        "codigo_correcto": """#include <limits.h>
if (a < INT_MAX) b = a + 1;""",
        "que_paso": "Operación que puede desbordar signed int (UB en C).",
        "regla": "Comprobá rangos; tipos más anchos; builtins seguros si el compilador los ofrece.",
    },
    r"warning:.*return-type": {
        "codigo_incorrecto": """int f(void) { return 3.14; }""",
        "codigo_correcto": """int f(void) { return 3; }
/* o cambiá el tipo de retorno a double */""",
        "que_paso": "El valor devuelto no encaja bien con el tipo declarado de la función.",
        "regla": "Unificá tipo de retorno y expresiones `return`.",
    },
    r"warning:.*shadow": {
        "codigo_incorrecto": """int x = 1;
void g(void) {
    int x = 2;
    (void)x;
}""",
        "codigo_correcto": """int x = 1;
void g(void) {
    int inner = 2;
    (void)inner;
}""",
        "que_paso": "Un nombre local oculta otro del ámbito exterior → confusiones.",
        "regla": "Renombrá la variable interna para claridad.",
    },
    r"warning:.*array-bounds": {
        "codigo_incorrecto": """int a[3] = {0};
int x = a[3];""",
        "codigo_correcto": """int a[3] = {0};
int x = a[2];""",
        "que_paso": "El compilador infiere un acceso fuera de límites.",
        "regla": "Ajustá índices y tamaños; confirmá con ASan.",
    },
    r"warning:.*null-dereference": {
        "codigo_incorrecto": """int *p = NULL;
*p = 1;""",
        "codigo_correcto": """int *p = NULL;
if (p) *p = 1;""",
        "que_paso": "Camino donde el puntero puede ser NULL y se desreferencia.",
        "regla": "Comprobá tras `malloc`/APIs que fallen; early return.",
    },
    r"warning:.*switch.*enumeration value not handled": {
        "codigo_incorrecto": """enum E { A, B, C };
void f(enum E e) {
  switch (e) { case A: break; }
}""",
        "codigo_correcto": """switch (e) {
  case A: break;
  case B: break;
  case C: break;
}""",
        "que_paso": "No todos los valores del enum tienen `case`.",
        "regla": "Cubrí todos los enumeradores o `default` consciente; `-Wswitch-enum` si querés exhaustividad.",
    },
    r"warning:.*pointer.*integer conversion|warning:.*integer.*pointer.*without a cast": {
        "codigo_incorrecto": """void *p = 0x1000;""",
        "codigo_correcto": """void *p = (void *)(uintptr_t)0x1000;""",
        "que_paso": "Mezcla puntero/entero sin cast donde el compilador exige claridad.",
        "regla": "`uintptr_t` y casts explícitos; documentá en código embebido.",
    },
    r"warning:.*missing prototype|warning:.*no previous prototype": {
        "codigo_incorrecto": """int add(int a, int b) { return a + b; } /* .c sin prototipo previo */""",
        "codigo_correcto": """/* math.h local */
int add(int a, int b);
int add(int a, int b) { return a + b; }""",
        "que_paso": "Función global definida sin prototipo visible antes (estilo antiguo).",
        "regla": "Prototipo en `.h` o `static` si es interna al `.c`.",
    },
    r"warning:.*tautological|warning:.*self-comparison|warning:.*always true|warning:.*always false": {
        "codigo_incorrecto": """unsigned x = 5;
if (x < 0) { }""",
        "codigo_correcto": """int x = 5;
if (x < 0) { }""",
        "que_paso": "Condición siempre verdadera o falsa (typo o tipo equivocado).",
        "regla": "Revisá `==` vs `=` y el tipo de la variable en la condición.",
    },
    r"warning:.*implicit conversion.*precision|warning:.*conversion.*may change value|warning:.*conversion from.*may alter its value": {
        "codigo_incorrecto": """double d = 1e100;
float f = d;""",
        "codigo_correcto": """double d = 1e100;
float f = (float)d; /* o detectá overflow */""",
        "que_paso": "Conversión a tipo más estrecho que puede truncar o cambiar el valor.",
        "regla": "Cast explícito o tipo intermedio más ancho; validá rango.",
    },
    r"warning:.*enum.*conversion|warning:.*enumeral.*mismatch": {
        "codigo_incorrecto": """enum A { AX = 1 }; enum B { BX = 1 };
enum A a = BX;""",
        "codigo_correcto": """enum A a = AX;""",
        "que_paso": "Mezcla de enums distintos o enum con int sin intención clara.",
        "regla": "Unificá el tipo enum o cast explícito documentado.",
    },
    r"warning:.*unused label": {
        "codigo_incorrecto": """void f(void) {
fin: return;
}""",
        "codigo_correcto": """void f(void) {
  return;
}""",
        "que_paso": "Etiqueta `goto` o residual sin referencias.",
        "regla": "Eliminá la etiqueta o usala; limpiá tras refactors.",
    },
    r"warning:.*typedef.*redefinition|warning:.*redefinition of typedef": {
        "codigo_incorrecto": """typedef int foo_t;
typedef long foo_t;""",
        "codigo_correcto": """typedef int foo_t;
/* un solo typedef canónico */""",
        "que_paso": "Dos `typedef` del mismo identificador o conflicto entre headers.",
        "regla": "Include guards; un solo lugar canónico para el typedef.",
    },
    r"warning:.*\[-Wundef\]": {
        "codigo_incorrecto": """#if FEATURE
#endif""",
        "codigo_correcto": """#if defined(FEATURE)
#endif""",
        "que_paso": "`#if FEATURE` con macro no definida puede advertir con `-Wundef`.",
        "regla": "Usá `defined(FEATURE)` o `#define` antes del `#if`.",
    },
    r"warning:.*\[-Wconversion\]|warning:.*\[-Wfloat-conversion\]": {
        "codigo_incorrecto": """float f(void) { return 3; }  /* int a float puede advertir */""",
        "codigo_correcto": """float f(void) { return 3.0f; }""",
        "que_paso": "Conversión implícita que puede cambiar valor o representación.",
        "regla": "Cast explícito o sufijos `f`/`u`/`L` adecuados; revisá fronteras numéricas.",
    },
    **CAPSULES_SUPPORT_C,
    **CAPSULES_SUPPORT_C_WARN,
    **CAPSULES_C_GAP,
}

__all__ = ["CAPSULES_C_EXTENDED"]
