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
}
