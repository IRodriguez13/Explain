"""Patrones GCC/Clang típicos de C (compartidos en parte con C++ y ensamblador vía driver)."""

ERRORES_C = {
    r"dereferencing pointer to incomplete type": {
        "titulo": "Puntero a tipo incompleto",
        "explicacion": "Accedés a miembros de un struct/union que solo fue declarado adelante (sin definición).",
        "soluciones": ["Incluí el .h con la definición completa", "Usá punteros en la API pública si ocultás el layout", "Revisá ciclos de includes"],
    },
    r"invalid use of undefined type|invalid use of incomplete type": {
        "titulo": "Uso de tipo incompleto",
        "explicacion": "El compilador no conoce el tamaño ni los miembros del tipo.",
        "soluciones": ["Incluí el header con la definición", "No instancies el struct completo si solo tenés forward declaration"],
    },
    r"implicit declaration of function": {
        "titulo": "Función no declarada",
        "explicacion": "Llamás a una función sin prototipo visible (C89 legacy o falta de #include).",
        "soluciones": ["#include del header correcto", "Declará el prototipo antes del uso", "Activá -Werror=implicit-function-declaration"],
    },
    r"conflicting types for": {
        "titulo": "Tipos en conflicto",
        "explicacion": "Prototipo (.h) y definición (.c) no coinciden en retorno o parámetros.",
        "soluciones": ["Unificá firma en header y .c", "Si agregaste parámetros, actualizá todas las llamadas", "Evitá prototipos duplicados contradictorios"],
    },
    r"too few arguments to function": {
        "titulo": "Faltan argumentos",
        "explicacion": "La llamada no pasa todos los parámetros que declara la función.",
        "soluciones": ["Contá argumentos vs prototipo", "Revisá orden y tipos tras un cambio de API"],
    },
    r"too many arguments to function": {
        "titulo": "Sobran argumentos",
        "explicacion": "Pasás más valores de los que la función declara.",
        "soluciones": ["Compará con el .h", "Revisá macros que inserten argumentos extra"],
    },
    r"makes integer from pointer without a cast|makes pointer from integer without a cast": {
        "titulo": "Tipos desalineados en argumentos",
        "explicacion": "A menudo es efecto secundario de firma incorrecta o argumentos en mal orden.",
        "soluciones": ["Arreglá primero conflicting types / too few arguments", "Verificá orden exacto de parámetros"],
    },
    r"expected ';' before": {
        "titulo": "Falta `;` o error previo",
        "explicacion": "El parser se perdió; el error suele señalarse en la línea siguiente.",
        "soluciones": ["Mirá la línea anterior", "Structs/enums suelen llevar `;` tras `}`"],
    },
    r"expected [\)\}] before|expected declaration|expected expression": {
        "titulo": "Token inesperado / falta cierre",
        "explicacion": "Falta `)`, `}` o hay una coma o expresión mal colocada.",
        "soluciones": ["Balanceá paréntesis y llaves", "Revisá macros multilínea"],
    },
    r"undefined reference to": {
        "titulo": "Símbolo sin definir (linker)",
        "explicacion": "El enlazador no encuentra la definición (función o variable global).",
        "soluciones": ["Linkeá todos los .o", "-l y -L para librerías", "Orden: muchas veces los -l van al final"],
    },
    r"multiple definition of|first defined here": {
        "titulo": "Definición múltiple",
        "explicacion": "El mismo símbolo global está definido en más de un .o.",
        "soluciones": ["Una sola definición; en headers usá static inline o declaración + definición en un .c", "Revisá #include de .c"],
    },
    r"storage size of .* isn't known": {
        "titulo": "Tamaño de tipo desconocido",
        "explicacion": "Instanciás un tipo incompleto.",
        "soluciones": ["Incluí la definición completa", "Usá puntero si solo necesitás opacidad"],
    },
    r"assignment .* makes pointer from integer": {
        "titulo": "Entero como puntero",
        "explicacion": "Asignás un entero donde va puntero o falta &.",
        "soluciones": ["Usá & para dirección", "Cast explícito solo si es deliberado"],
    },
    r"incompatible pointer type|incompatible types when": {
        "titulo": "Punteros o tipos incompatibles",
        "explicacion": "Mezclás punteros de distinto tipo sin conversión explícita.",
        "soluciones": ["Cast (Tipo*) si es válido", "Alineá char* vs unsigned char*", "void* requiere cast al usar"],
    },
    r"segmentation fault|SIGSEGV": {
        "titulo": "SIGSEGV",
        "explicacion": "Acceso a memoria inválida.",
        "soluciones": ["valgrind / ASan", "Punteros y límites de arrays", "gdb con -g"],
    },
    r"UndefinedBehaviorSanitizer|\bUBSan\b|SUMMARY: UndefinedBehaviorSanitizer": {
        "titulo": "UndefinedBehaviorSanitizer (UBSan)",
        "explicacion": "El binario se armó con -fsanitize=undefined (o grupo equivalente): en runtime se detectó una violación explícita del estándar C/C++.",
        "soluciones": [
            "Leé la línea archivo:columna y el tipo de UB (overflow, null, misalignment, etc.).",
            "Recompilá con -g para símbolos y corregí la expresión o el layout de datos.",
        ],
    },
    r"ERROR: AddressSanitizer|AddressSanitizer:|SUMMARY: AddressSanitizer|\bASAN\b": {
        "titulo": "AddressSanitizer (ASan)",
        "explicacion": "Instrumentación de memoria: heap-buffer-overflow, use-after-free, stack-overflow, etc. Muchos casos son UB o muy cercanos en la práctica.",
        "soluciones": ["Stack trace del informe", "Reproducí con el mismo binario ASan", "Revisá límites y tiempo de vida de punteros"],
    },
    r"\d+:\d+:\s*runtime error:": {
        "titulo": "Runtime error (típico de sanitizers Clang)",
        "explicacion": "Clang suele prefijar con archivo:línea:columna: un `runtime error:` cuando corre con UBSan u otros chequeos; indica UB o condición no permitida por el estándar.",
        "soluciones": ["Leé el resto del mensaje (overflow, shift, null, alignment)", "Corrige en el fuente o endurece con tipos seguros"],
    },
    r"heap-buffer-overflow|stack-buffer-overflow|global-buffer-overflow|heap-use-after-free|stack-use-after-return|use-after-poison": {
        "titulo": "AddressSanitizer — tipo de fallo (memoria)",
        "explicacion": "Detalle concreto del informe ASan: desbordamiento de heap/stack, uso tras liberar, retorno con puntero a frame, etc.",
        "soluciones": [
            "Leé la dirección y el stack trace del informe.",
            "Reproducí con el mismo binario -fsanitize=address y símbolos -g.",
        ],
    },
    r"request for member.*in something not a structure or union": {
        "titulo": "No es struct/union",
        "explicacion": "Usás `.` o `->` sobre algo que no es struct (ej. puntero mal o tipo equivocado).",
        "soluciones": ["Revisá * vs ->", "Tipo real del puntero"],
    },
    r"lvalue required as|lvalue required": {
        "titulo": "Falta un lvalue",
        "explicacion": "Asignás o tomás dirección de una expresión que no es modificable.",
        "soluciones": ["Usá variable intermedia", "No asignés a resultado de función o literal"],
    },
    r"called object .* is not a function or function pointer": {
        "titulo": "No es llamable",
        "explicacion": "Intentás llamar como función algo que no lo es (macro, variable, typo).",
        "soluciones": ["Revisá nombre y #define", "Declará puntero a función con typedef claro"],
    },
    r"subscripted value is neither array nor pointer": {
        "titulo": "No es array ni puntero",
        "explicacion": "Usás `[i]` sobre un valor que no admite subíndice.",
        "soluciones": ["Revisá tipo y desreferencia", "Arrays decay a puntero; structs no"],
    },
    r"invalid type argument of|invalid operands to binary": {
        "titulo": "Operación inválida entre tipos",
        "explicacion": "El operador no aplica a esos tipos (ej. % con float).",
        "soluciones": ["Convertí tipos explícitamente", "Revisá macros que oculten tipos"],
    },
    r"void value not ignored as it ought to be": {
        "titulo": "Función void usada como valor",
        "explicacion": "Usás el resultado de una función void en una expresión.",
        "soluciones": ["Llamá la función como sentencia sola", "Si necesitás valor, la API debe retornar tipo distinto"],
    },
    r"comparison of distinct pointer types|comparison between pointer and integer": {
        "titulo": "Comparación puntero/entero",
        "explicacion": "Comparás punteros de tipos distintos o puntero con entero sin cast.",
        "soluciones": ["Cast a void* o uintptr_t si es portátil", "Unificá el tipo del puntero"],
    },
    r"initialization makes pointer from integer without a cast": {
        "titulo": "Inicialización puntero desde entero",
        "explicacion": "Asignás un literal entero a puntero (a veces direcciones embebidas).",
        "soluciones": ["Usá cast (void*) o uintptr_t según contexto", "En userspace suele ser error de lógica"],
    },
    r"excess elements in struct initializer": {
        "titulo": "Demasiados valores en inicializador",
        "explicacion": "El inicializador del struct tiene más campos de los declarados.",
        "soluciones": ["Contá campos del struct", "Revisá designators `.campo =`"],
    },
    r"missing braces around initializer": {
        "titulo": "Faltan llaves en inicializador",
        "explicacion": "Inicializador de struct/array anidado necesita llaves extra.",
        "soluciones": ["Anidá `{ { ... } }` correctamente"],
    },
    r"redefinition of|redeclared": {
        "titulo": "Redefinición",
        "explicacion": "El mismo identificador se define dos veces en el mismo ámbito o se contradice.",
        "soluciones": ["static en .c para símbolos internos", "Include guards / #pragma once en headers"],
    },
    r"unknown type name": {
        "titulo": "Tipo desconocido",
        "explicacion": "Usás un nombre de tipo que el compilador no conoce (typo o falta include).",
        "soluciones": ["typedef struct X o include del header", "Revisá mayúsculas"],
    },
    r"variable-sized object may not be initialized": {
        "titulo": "VLA no inicializable",
        "explicacion": "Arrays de tamaño variable en C no pueden tener inicializador completo estándar.",
        "soluciones": ["Usá tamaño constante o malloc + asignación manual"],
    },
    r"case label not within a switch": {
        "titulo": "`case` fuera de switch",
        "explicacion": "Hay un `case`/`default` sin un `switch` envolvente válido (llave mal cerrada).",
        "soluciones": ["Revisá llaves del switch", "Indentá y formateá para ver el bloque"],
    },
    r"break statement not within loop or switch": {
        "titulo": "`break` fuera de lugar",
        "explicacion": "`break` solo válido en switch o bucle.",
        "soluciones": ["Revisá si querías return o goto etiquetado", "Llaves de más o de menos"],
    },
    r"continue statement not within a loop": {
        "titulo": "`continue` fuera de bucle",
        "explicacion": "`continue` solo dentro de for/while/do.",
        "soluciones": ["Revisá estructura de llaves"],
    },
    r"duplicate case value": {
        "titulo": "Valor de case duplicado",
        "explicacion": "Dos `case` con la misma constante.",
        "soluciones": ["Unificá casos o corregí el valor"],
    },
    r"label.*referenced outside of any function": {
        "titulo": "Etiqueta goto fuera de función",
        "explicacion": "goto a etiqueta en otro ámbito inválido.",
        "soluciones": ["goto solo dentro de la misma función"],
    },
    r"function returns address of local variable": {
        "titulo": "Retornás puntero a local",
        "explicacion": "La variable deja de existir al salir de la función.",
        "soluciones": ["static local", "malloc + documentar propietario", "buffer pasado por parámetro"],
    },
    r"pointer from integer may be truncated": {
        "titulo": "Conversión puntero/entero peligrosa",
        "explicacion": "Cast entre entero y puntero con distinto ancho.",
        "soluciones": ["uintptr_t/intptr_t", "Revisá arquitectura 32/64 bits"],
    },
    r"discards? qualifiers? from pointer target type|passing argument.*discards": {
        "titulo": "Se pierde const/volatile",
        "explicacion": "Pasás const char* donde esperan char* mutable.",
        "soluciones": ["Hacé la API const-correct", "Cast solo si garantizás no mutación"],
    },
    r"format .* expects argument|too many arguments for format": {
        "titulo": "printf/scanf formato vs argumentos",
        "explicacion": "Cantidad o tipos no coinciden con la cadena de formato.",
        "soluciones": ["Un % por argumento", "Usá %zu para size_t, PRId32, etc."],
    },
    r"array subscript has type char": {
        "titulo": "Índice tipo char",
        "explicacion": "En C char puede ser signed; índices deben ser enteros sin signo adecuados.",
        "soluciones": ["Cast a unsigned char o size_t"],
    },
    r"overflow in constant expression": {
        "titulo": "Desbordamiento en constante",
        "explicacion": "Operación en tiempo de compilación excede el rango del tipo.",
        "soluciones": ["Usá tipo más ancho o U suffix", "Revisá aritmética en macros"],
    },
    r"division by zero": {
        "titulo": "División por cero",
        "explicacion": "Divisor constante cero o optimizador detecta caso inválido.",
        "soluciones": ["Validá divisor en runtime", "Condicioná la división"],
    },
    r"unreachable code|will never be executed": {
        "titulo": "Código inalcanzable",
        "explicacion": "Hay return/break/exit antes o condición siempre falsa.",
        "soluciones": ["Eliminá código muerto o corregí la lógica"],
    },
    r"unused variable|set but not used|defined but not used": {
        "titulo": "Variable no usada",
        "explicacion": "Suele ser -Wunused; a veces indica olvido o typo.",
        "soluciones": ["Usá la variable, borrala, o (void)x;", "Prefijo _ si es intencional"],
    },
    r"control reaches end of non-void function": {
        "titulo": "Función no void sin return",
        "explicacion": "Algún camino de ejecución no retorna valor.",
        "soluciones": ["Agregá return en todos los caminos", "assert(0) en ramas imposibles"],
    },
    r"enumerator value for .* is not an integer constant": {
        "titulo": "Enum con valor no constante",
        "explicacion": "Los valores de enum en C deben ser constantes enteras en tiempo de compilación.",
        "soluciones": ["Usá #define o const solo en C++", "Expresión constante válida"],
    },
    r"flexible array member|invalid use of flexible array member": {
        "titulo": "Miembro array flexible",
        "explicacion": "Solo el último miembro del struct puede ser [] y tiene reglas estrictas.",
        "soluciones": ["Seguí el patrón struct header + malloc(size+len)", "No anides otro campo después"],
    },
    r"nested redefinition|error in included file": {
        "titulo": "Error en archivo incluido",
        "explicacion": "El error real está en un #include; el mensaje indica la cadena de includes.",
        "soluciones": ["Arreglá el header señalado", "Revisá orden de includes"],
    },
    r"fatal error: no input files|fatal error:": {
        "titulo": "Error fatal del compilador",
        "explicacion": "GCC aborta (archivo ausente, opción inválida, límite interno).",
        "soluciones": ["Revisá rutas y flags del comando", "Leé la línea siguiente del mensaje"],
    },
    r"cannot specify -o with -c, -S or -E with multiple files": {
        "titulo": "Opciones gcc incompatibles",
        "explicacion": "-o con múltiples unidades de compilación en ciertos modos no está permitido.",
        "soluciones": ["Compilá por separado o quitá -o en ese modo"],
    },
    r"incompatible pointer to integer conversion|incompatible integer to pointer conversion": {
        "titulo": "Conversión puntero / entero incompatible",
        "explicacion": "El compilador rechaza mezclar puntero y entero sin un cast explícito claro.",
        "soluciones": ["uintptr_t / intptr_t", "Cast explícito documentado", "Revisá APIs de bajo nivel"],
    },
    r"initializer element is not constant": {
        "titulo": "Inicializador no constante",
        "explicacion": "En C, static o duración de archivo exigen expresiones constantes en inicializadores.",
        "soluciones": ["Asignación en función al arrancar", "Macros o enum para constantes"],
    },
    r"case label not within a switch statement|default label not within a switch": {
        "titulo": "case/default fuera de switch",
        "explicacion": "Un case o default quedó fuera del switch (llave de más o de menos).",
        "soluciones": ["Revisá llaves alrededor del switch", "Indentación y bloques"],
    },
    r"break statement not within loop or switch|continue statement not within a loop": {
        "titulo": "break/continue mal ubicado",
        "explicacion": "Ese break o continue no tiene un switch/loop que lo contenga.",
        "soluciones": ["Revisá anidamiento de if/for/switch", "Estructura del algoritmo"],
    },
    r"request for member.*in something not a structure or union": {
        "titulo": "Operador . en no struct/union",
        "explicacion": "Usás . donde el operando no es struct/union (a veces falta -> en puntero).",
        "soluciones": ["-> si es puntero", "Corregí el tipo de la expresión"],
    },
    r"lvalue required as unary '&' operand|lvalue required as left operand of assignment": {
        "titulo": "Se esperaba un lvalue",
        "explicacion": "No podés tomar & ni asignar al resultado de una expresión que no es modificable.",
        "soluciones": ["Variable intermedia", "Paréntesis y precedencia de operadores"],
    },
    r"linker command failed|collect2: error: ld returned \d+ exit status": {
        "titulo": "Enlazado falló (ld / collect2)",
        "explicacion": "La fase de enlace terminó mal; el motivo concreto suele estar unas líneas arriba.",
        "soluciones": ["undefined reference / multiple definition", "Orden y flags -l", "LDFLAGS y rpath"],
    },
    r"cannot compute sizeof|invalid application of 'sizeof'": {
        "titulo": "sizeof inválido",
        "explicacion": "sizeof sobre tipo incompleto o uso no permitido por el estándar.",
        "soluciones": ["Incluí el header con la definición completa", "sizeof(*p) si p es puntero opaco"],
    },
    r"variable has incomplete type|field has incomplete type": {
        "titulo": "Tipo incompleto en variable o campo",
        "explicacion": "Declarás un struct/union/enum que solo fue declarado adelante.",
        "soluciones": ["Incluí el .h con la definición completa", "Puntero en lugar de valor embebido"],
    },
}
