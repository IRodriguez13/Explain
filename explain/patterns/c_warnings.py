# Patrones de advertencia (GCC/Clang, enlazador, estilo C). Español fijo.

WARNINGS_C = {
    r"warning:.*implicit declaration of function": {
        "titulo": "Declaración implícita de función (obsoleta en C99+)",
        "explicacion": "Se usó una función sin prototipo visible. En C moderno es error; antes el compilador asumía int f(). Declara la función o incluye el header correcto.",
        "soluciones": ["Incluye el .h adecuado (stdio.h, string.h, etc.) o añade un prototipo antes del uso."],
    },
    r"warning:.*incompatible implicit conversion": {
        "titulo": "Conversión implícita incompatible",
        "explicacion": "Se asigna o se pasa un valor a un tipo distinto sin cast explícito y el compilador advierte de posible pérdida o comportamiento raro.",
        "soluciones": ["Usa un cast explícito si es intencional, o corrige el tipo de la variable/parámetro."],
    },
    r"warning:.*unused variable": {
        "titulo": "Variable no usada",
        "explicacion": "Se declaró una variable que no se lee en ningún sitio. Suele ser código muerto o un olvido.",
        "soluciones": ["Elimínala, úsala, o marca intencionalmente con (void)x o __attribute__((unused))."],
    },
    r"warning:.*unused parameter": {
        "titulo": "Parámetro no usado",
        "explicacion": "Un parámetro de función no se utiliza en el cuerpo. Común en callbacks con firma fija.",
        "soluciones": ["Prefija con _ (p. ej. _ctx) o usa (void)param; en C++ puedes omitir el nombre."],
    },
    r"warning:.*unused function": {
        "titulo": "Función estática no usada",
        "explicacion": "Una función static no tiene referencias. Puede ser código muerto.",
        "soluciones": ["Elimínala si sobra, o expónla si debía usarse en otro .c."],
    },
    r"warning:.*sign-compare": {
        "titulo": "Comparación entre signed y unsigned",
        "explicacion": "Comparas int con size_t (u otro unsigned). Los valores negativos se convierten a unsigned grandes y el bucle o la condición pueden fallar.",
        "soluciones": ["Usa el mismo tipo en ambos lados, cast explícito documentado, o tipos con signo coherentes."],
    },
    r"warning:.*sign-conversion|warning:.*may change the sign of the result": {
        "titulo": "Conversión signed/unsigned con posible cambio de signo (-Wsign-conversion)",
        "explicacion": "Mezclas tipos con y sin signo; un negativo puede interpretarse como un valor enorme en unsigned y romper comparaciones o bucles.",
        "soluciones": [
            "Unificá signo en la expresión (p. ej. size_t con índices y longitudes).",
            "static_cast / cast explícito documentado si la conversión es intencional.",
        ],
    },
    r"warning:.*unused but set variable|warning:.*set but not used": {
        "titulo": "Variable asignada y nunca leída",
        "explicacion": "Se escribe en la variable pero ninguna lectura la usa; suele ser olvido o código muerto tras un refactor.",
        "soluciones": ["Eliminá la variable o usala", "Si era para depuración, marcala con (void)x o __attribute__((unused))"],
    },
    r"warning:.*ignored-qualifiers": {
        "titulo": "Calificadores ignorados (const/volatile) en tipo",
        "explicacion": "El compilador ignora const/volatile en un contexto donde no aplican (p. ej. typedef o valor por copia mal declarado).",
        "soluciones": ["Revisá la firma: const en puntero vs en valor", "Alineá el tipo con el uso real"],
    },
    r"warning:.*format .* expects": {
        "titulo": "printf/scanf: formato no coincide con los argumentos",
        "explicacion": "El especificador de formato (%d, %s, %zu…) no encaja con el tipo real del argumento → UB o salida basura.",
        "soluciones": ["Alinea cada % con el tipo (p. ej. size_t → %zu con el header correcto)."],
    },
    r"warning:.*fallthrough": {
        "titulo": "Fall-through en switch",
        "explicacion": "El control cae de un case al siguiente sin break. A veces intencional, a menudo bug.",
        "soluciones": ["Añade break o [[fallthrough]] / comentario explícito según el compilador."],
    },
    r"warning:.*pointer.*integer": {
        "titulo": "Mezcla puntero / entero",
        "explicacion": "Conviertes entre puntero y entero de forma dudosa; puede romper en 64 bits o con ASan.",
        "soluciones": ["Usa uintptr_t/intptr_t y conversiones explícitas documentadas."],
    },
    r"warning:.*deprecated": {
        "titulo": "Uso de API obsoleta",
        "explicacion": "La función o tipo está marcado como deprecated; en futuras versiones puede desaparecer.",
        "soluciones": ["Migra a la API recomendada en la documentación o en el mensaje del compilador."],
    },
    r"warning:.*may be used uninitialized": {
        "titulo": "Variable posiblemente sin inicializar",
        "explicacion": "Hay un camino de ejecución donde se lee la variable antes de asignarle valor.",
        "soluciones": ["Inicializa al declarar o asigna en todas las ramas antes del uso."],
    },
    r"warning:.*strict-aliasing": {
        "titulo": "Violación de strict aliasing",
        "explicacion": "Accedes a la misma memoria con tipos puntero incompatibles; el optimizador puede asumir que no ocurre.",
        "soluciones": ["Usa memcpy para reinterpretar bytes, o union con cuidado y documentación."],
    },
    r"warning:.*\[-Wsequence-point\]|warning:.*operation on .*may be undefined|warning:.*unsequenced|warning:.*multiple unsequenced": {
        "titulo": "Posible UB: orden de evaluación (sequence points)",
        "explicacion": "Dos efectos secundarios sobre la misma variable sin sequence point intermedio, o lecturas/escrituras sin orden definido: el estándar no define el resultado.",
        "soluciones": [
            "Separá en sentencias (variables temporales).",
            "Evitá i++ en la misma expresión que otra modificación de i.",
        ],
    },
    r"warning:.*undefined behavior|note:.*undefined behavior": {
        "titulo": "Comportamiento indefinido (diagnóstico del compilador)",
        "explicacion": "GCC/Clang marcan explícitamente un patrón que el estándar C no define; el programa puede hacer cualquier cosa en optimización.",
        "soluciones": [
            "Leé el mensaje completo y el estándar o cppreference para ese caso.",
            "Simplificá la expresión; usá APIs seguras (memcpy, comprobaciones de rango).",
        ],
    },
    r"warning:.*left shift of negative|warning:.*right shift of negative|warning:.*shift count >=|warning:.*shift count.*width|warning:.*negative.*shift": {
        "titulo": "Desplazamiento inválido (UB en C)",
        "explicacion": "Desplazar un signed negativo, o un recuento fuera de rango / ≥ ancho del tipo, es comportamiento indefinido en C.",
        "soluciones": ["Usá unsigned para bits", "Acotá el shift con comprobación", "Evitá shifts en valores negativos"],
    },
    r"warning:.*dereferencing.*type-punned|type-punned pointer will break strict-aliasing": {
        "titulo": "Type-punning y strict aliasing (riesgo de UB)",
        "explicacion": "Se accede al mismo almacenamiento vía punteros de tipo distinto sin reglas permitidas; con optimización puede ser UB.",
        "soluciones": ["memcpy entre representaciones", "char* para bytes", "union con cautela y compilador/documentación"],
    },
    r"warning:.*overflow": {
        "titulo": "Posible desbordamiento aritmético",
        "explicacion": "Una operación puede desbordar el rango del tipo (signed overflow es UB en C).",
        "soluciones": ["Comprueba rangos, usa tipos más grandes o funciones seguras (built-ins o bibliotecas)."],
    },
    r"ld: warning:.*cannot find entry symbol": {
        "titulo": "Enlazador: símbolo de entrada no encontrado",
        "explicacion": "Se esperaba _start u otra entrada por defecto y no está definida (linker script o CRT).",
        "soluciones": ["Para bare-metal define el punto de entrada; para hosted, enlaza con crt0/crtbegin correctos."],
    },
    r"warning:.*return-type": {
        "titulo": "Tipo de retorno inconsistente",
        "explicacion": "El compilador detecta que el valor devuelto no encaja con el tipo declarado de la función.",
        "soluciones": ["Corrige el tipo de retorno o el valor que devuelves."],
    },
    r"warning:.*shadow": {
        "titulo": "Variable que oculta otra (shadowing)",
        "explicacion": "Un nombre local coincide con uno de un ámbito exterior y puede confundir lecturas del código.",
        "soluciones": ["Renombra la variable interna para que el significado sea claro."],
    },
    r"warning:.*discarded-qualifiers": {
        "titulo": "Se descalifican const/volatile",
        "explicacion": "Asignas un puntero const a puntero no const, perdiendo la promesa de no modificar.",
        "soluciones": ["Propaga const en la API o haz una copia mutable si es necesario."],
    },
    r"warning:.*array-bounds": {
        "titulo": "Posible acceso fuera de límites de array",
        "explicacion": "El compilador infiere un índice o longitud que puede pasarse del tamaño del array.",
        "soluciones": ["Ajusta el bucle o el tamaño; usa herramientas como ASan en depuración."],
    },
    r"warning:.*null-dereference": {
        "titulo": "Posible desreferencia de NULL",
        "explicacion": "Hay un camino donde un puntero puede ser NULL y se usa sin comprobar.",
        "soluciones": ["Comprueba punteros tras malloc/APIs que pueden fallar."],
    },
    r"warning:.*switch.*enumeration value not handled": {
        "titulo": "switch incompleto sobre enum",
        "explicacion": "No todos los valores del enum tienen case; si añades valores al enum, falta cubrirlos.",
        "soluciones": ["Añade los case faltantes o un default explícito (y -Wswitch-enum si quieres exhaustividad)."],
    },
    r"warning:.*pointer.*integer conversion|warning:.*integer.*pointer.*without a cast": {
        "titulo": "Conversión puntero/entero (warning)",
        "explicacion": "Se mezcla puntero y entero sin cast; puede romper en otra arquitectura o con ASan.",
        "soluciones": ["uintptr_t", "Cast explícito y comentario si es hardware embebido"],
    },
    r"warning:.*missing prototype|warning:.*no previous prototype": {
        "titulo": "Prototipo ausente (-Wmissing-prototypes)",
        "explicacion": "Función global sin prototipo antes de la definición.",
        "soluciones": ["Declaración en .h", "static si es interna al .c"],
    },
    r"warning:.*tautological|warning:.*self-comparison|warning:.*always true|warning:.*always false": {
        "titulo": "Comparación tautológica",
        "explicacion": "La condición es siempre verdadera o siempre falsa (typo o variable equivocada).",
        "soluciones": ["Revisá == vs =", "Variable correcta en ambos lados"],
    },
    r"warning:.*implicit conversion.*precision|warning:.*conversion.*may change value|warning:.*conversion from.*may alter its value": {
        "titulo": "Conversión con pérdida o cambio de valor",
        "explicacion": "Se convierte a un tipo más estrecho o incompatible y el valor puede truncarse o interpretarse distinto.",
        "soluciones": ["Cast explícito", "Tipo intermedio más ancho", "-Wconversion con criterio"],
    },
    r"warning:.*enum.*conversion|warning:.*enumeral.*mismatch": {
        "titulo": "Conversión entre enums",
        "explicacion": "Mezcla de tipos enum distintos o enum con entero sin intención clara.",
        "soluciones": ["Cast al enum correcto", "Evitá mezclar enums de distintos orígenes"],
    },
    r"warning:.*unused label": {
        "titulo": "Etiqueta no usada",
        "explicacion": "Un label de goto o case residual no tiene referencias.",
        "soluciones": ["Elimínala", "O usala / documentá si es para depuración"],
    },
    r"warning:.*typedef.*redefinition|warning:.*redefinition of typedef": {
        "titulo": "typedef redefinido",
        "explicacion": "Dos typedef del mismo nombre o conflicto entre headers.",
        "soluciones": ["Include guards", "Un solo typedef canónico", "Prefijos en nombres"],
    },
    r"warning:.*\[-Wundef\]": {
        "titulo": "Macro no definida en #if (-Wundef)",
        "explicacion": "El preprocesador evalúa #if con un identificador que no está definido; con -Wundef es advertencia explícita.",
        "soluciones": ["Usá defined(FEATURE)", "O #define antes del #if", "Documentá flags de configuración"],
    },
    r"warning:.*\[-Wconversion\]|warning:.*\[-Wfloat-conversion\]": {
        "titulo": "Conversión que puede cambiar el valor (-Wconversion)",
        "explicacion": "Pérdida de rango o cambio signed/unsigned implícito; en fronteras numéricas puede acabar en valores imposibles o UB indirecto.",
        "soluciones": ["Cast explícito documentado", "Tipos intermedios más anchos", "Comprobá límites antes de convertir"],
    },
    r"warning:.*\[-Wshadow\]": {
        "titulo": "Sombreado de variable (-Wshadow)",
        "explicacion": "Un nombre local u oculta otro de un ámbito exterior; puede confundir lectura y depuración.",
        "soluciones": ["Renombrá el interno", "static en file scope si aplica", "Desactivá -Wshadow solo con criterio"],
    },
    r"warning:.*\[-Wstrict-aliasing\]": {
        "titulo": "Strict aliasing (-Wstrict-aliasing)",
        "explicacion": "Se accede al mismo almacenamiento por punteros de tipos incompatibles; el optimizador puede asumir alias ilegales.",
        "soluciones": ["memcpy / union con cuidado", "char* para bytes", "fstrict-aliasing=0 solo si es inevitable"],
    },
    r"warning:.*\[-Wjump-misses-init\]": {
        "titulo": "Salto salta inicialización (-Wjump-misses-init)",
        "explicacion": "goto o switch entra en un bloque saltando la inicialización de una variable automática.",
        "soluciones": ["Envolvé en { } el init", "Evitá goto hacia declaraciones", "Inicializá antes del salto"],
    },
}
