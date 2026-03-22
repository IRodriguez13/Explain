"""Base de patrones (regex -> explicación en español). Solo biblioteca estándar."""

ERRORES_C = {
    r"dereferencing pointer to incomplete type": {
        "titulo": "Puntero a tipo incompleto",
        "explicacion": """Estás intentando acceder a un miembro de un struct/union que el compilador
no conoce completamente. Suele pasar con forward declaration (struct foo;) sin el header
que define los campos.""",
        "soluciones": [
            "Incluí el .h con la definición completa del struct",
            "Si usás forward declaration, asegurate de tener la definición antes de dereferenciar",
            "Revisá dependencias circulares entre headers",
        ],
    },
    r"invalid use of undefined type|invalid use of incomplete type": {
        "titulo": "Uso de tipo incompleto o no definido",
        "explicacion": """Usás un struct/union/class del que el compilador solo vio una declaración
adelantada (sin campos/miembros). No puede acceder a miembros ni conocer el tamaño.""",
        "soluciones": [
            "Incluí el header con la definición completa antes de usar miembros",
            "Si es a propósito (encapsulamiento), exponé funciones en el .c y no toques los campos desde fuera",
            "Revisá includes y ciclos entre headers",
        ],
    },
    r"implicit declaration of function": {
        "titulo": "Función no declarada",
        "explicacion": """Llamás a una función que el compilador no conoce: falta prototipo o #include.""",
        "soluciones": [
            "Incluí el header correcto (ej. #include <string.h> para strcpy)",
            "Declará el prototipo antes de usarla si es tuya",
            "Verificá typos en el nombre de la función",
        ],
    },
    r"conflicting types for": {
        "titulo": "Tipos en conflicto",
        "explicacion": """El prototipo y la definición (o dos declaraciones) no coinciden en tipos.""",
        "soluciones": [
            "Igualá prototipo y definición byte a byte en tipos y calificadores",
            "Buscá declaraciones duplicadas contradictorias",
            "Compartí un solo header entre .c que usan la función",
        ],
    },
    r"expected ';' before": {
        "titulo": "Falta punto y coma o hay un error antes",
        "explicacion": """Falta ; o el parser se perdió antes: el error a veces se reporta en la línea siguiente.""",
        "soluciones": [
            "Mirá la línea anterior a la marcada",
            "Structs/enums/typedefs suelen necesitar ; después de }",
            "Revisá paréntesis/llaves sin cerrar",
        ],
    },
    r"undefined reference to": {
        "titulo": "Referencia indefinida (enlazado)",
        "explicacion": """Compiló, pero el linker no encuentra la definición del símbolo (función/variable global).""",
        "soluciones": [
            "Linkeá todos los .o/.a necesarios en el comando final",
            "Librerías externas: -lnombre (y a veces -Lruta)",
            "En muchos linkers el orden importa: poné -l al final",
            "Revisá Makefile: objetos y dependencias completas",
        ],
    },
    r"storage size of .* isn't known": {
        "titulo": "Tamaño del tipo desconocido",
        "explicacion": """Instanciás un struct incompleto: el compilador no sabe su tamaño (solo forward declaration).""",
        "soluciones": [
            "Incluí el header con la definición completa",
            "Si querés ocultar el layout, usá punteros (struct foo*) en la API pública",
        ],
    },
    r"assignment .* makes pointer from integer": {
        "titulo": "Entero tratado como puntero",
        "explicacion": """Asignás un entero donde va un puntero, o falta & o hay mezcla de tipos.""",
        "soluciones": [
            "Para dirección de variable: &variable",
            "Si el cast es intencional, hacelo explícito: (Tipo*)valor",
            "Revisá * vs &",
        ],
    },
    r"incompatible pointer type": {
        "titulo": "Punteros incompatibles",
        "explicacion": """Mezclás tipos de puntero sin conversión explícita donde C lo exige.""",
        "soluciones": [
            "Cast explícito si es deliberado: (TipoDestino*)ptr",
            "Alineá los tipos reales (char* vs unsigned char*, etc.)",
            "Desde void* hacé cast al usar",
        ],
    },
    r"segmentation fault|SIGSEGV": {
        "titulo": "Violación de segmento (SIGSEGV)",
        "explicacion": """Acceso a memoria inválida: NULL, fuera de límites, use-after-free, stack overflow, etc.""",
        "soluciones": [
            "valgrind ./programa o ASan (-fsanitize=address)",
            "Inicializá punteros antes de usar",
            "Revisá índices y tamaños de buffers",
            "No uses memoria después de free; compilá con -g y depurá con gdb",
        ],
    },
}

ERRORES_CSHARP = {
    r"CS0103:.*does not exist in the current context": {
        "titulo": "Nombre inexistente en el contexto",
        "explicacion": """Usás un identificador que no está visible: falta using, typo o scope incorrecto.""",
        "soluciones": [
            "Agregá using al namespace correcto",
            "C# distingue mayúsculas: revisá el nombre",
            "Instalá el paquete NuGet si es de terceros",
            "Declará la variable o importá el tipo",
        ],
    },
    r"CS0246:.*type or namespace name .* could not be found": {
        "titulo": "Tipo o namespace no encontrado",
        "explicacion": """El compilador no resuelve el tipo: falta referencia, using o el nombre no existe en el TF.""",
        "soluciones": [
            "using NombreEspacio;",
            "Referencia al proyecto/assembly",
            "dotnet add package ... si aplica",
            "Verificá TargetFramework vs APIs disponibles",
        ],
    },
    r"CS1061:.*does not contain a definition for": {
        "titulo": "Miembro inexistente en el tipo",
        "explicacion": """Ese tipo no expone el método/propiedad (typo, API distinta o extensión sin using).""",
        "soluciones": [
            "Revisá nombre y sobrecargas",
            "Mirá la versión de la librería / documentación",
            "Métodos de extensión: falta using del namespace de extensiones",
        ],
    },
    r"CS0029:.*Cannot implicitly convert type": {
        "titulo": "Conversión implícita inválida",
        "explicacion": """Asignás o pasás un valor a un tipo sin conversión implícita permitida.""",
        "soluciones": [
            "Cast explícito: (TipoDestino)x",
            "Métodos de conversión: .ToString(), int.Parse, etc.",
            "Para referencias: as / patrón is",
        ],
    },
}

ERRORES_PYTHON = {
    r"NameError: name '.*' is not defined": {
        "titulo": "Nombre no definido",
        "explicacion": """Usás un nombre que no existe en ese scope o no importaste el módulo.""",
        "soluciones": [
            "Definí la variable antes de usarla",
            "Revisá typos y mayúsculas",
            "import módulo o from módulo import ...",
            "Si es global en función, declará global si corresponde",
        ],
    },
    r"IndentationError:": {
        "titulo": "Indentación inválida",
        "explicacion": """Los bloques en Python dependen de la indentación; hay mezcla tabs/espacios o niveles rotos.""",
        "soluciones": [
            "Usá solo espacios (PEP 8: 4 por nivel)",
            "No mezcles tabs y espacios",
            "Mostrá caracteres invisibles en el editor",
        ],
    },
    r"TabError:": {
        "titulo": "Tabs y espacios mezclados",
        "explicacion": """En la misma línea o bloque mezclaste tabulaciones y espacios de forma inconsistente.""",
        "soluciones": [
            "Convertí el archivo a solo espacios",
            "Configurá el editor para insertar espacios al indentar",
        ],
    },
    r"SyntaxError: invalid syntax": {
        "titulo": "Sintaxis inválida",
        "explicacion": """El parser no puede interpretar la construcción (símbolos, palabras clave o : faltantes).""",
        "soluciones": [
            "Revisá la línea señalada y la anterior",
            "Cerrá (), [], {}",
            "No uses palabras reservadas como nombres",
            "if/for/def/class terminan con :",
        ],
    },
    r"TypeError: unsupported operand type": {
        "titulo": "Operación entre tipos no soportada",
        "explicacion": """Aplicás un operador a tipos que no lo implementan juntos (ej. str + int).""",
        "soluciones": [
            "Convertí explícitamente: str(), int(), float()",
            "Verificá tipos con type() o isinstance()",
        ],
    },
    r"TypeError:.*takes .* positional argument": {
        "titulo": "Cantidad de argumentos incorrecta",
        "explicacion": """Llamaste a la función con más o menos argumentos de los que acepta.""",
        "soluciones": [
            "Revisá la firma en help(func) o la definición",
            "Contá self en métodos de instancia",
        ],
    },
    r"AttributeError:.*has no attribute": {
        "titulo": "Atributo inexistente",
        "explicacion": """El objeto no tiene ese atributo (typo, tipo equivocado o None).""",
        "soluciones": [
            "dir(obj) o anotaciones/tipos para ver miembros",
            "Validá que no sea None antes de usar",
            "Revisá versión de la librería",
        ],
    },
    r"KeyError:": {
        "titulo": "Clave inexistente",
        "explicacion": """Accedés a dict[clave] y esa clave no está.""",
        "soluciones": [
            "Usá .get(clave, default)",
            "Verificá con in o .keys()",
            "Revisá typos en la clave",
        ],
    },
    r"ModuleNotFoundError: No module named": {
        "titulo": "Módulo no instalado o no en PYTHONPATH",
        "explicacion": """Python no encuentra el paquete al importar.""",
        "soluciones": [
            "pip install paquete (o pip install -e . en desarrollo)",
            "Activá el venv correcto",
            "Si es módulo local, revisá el path y __init__.py",
        ],
    },
    r"ImportError: cannot import name": {
        "titulo": "Import con nombre incorrecto",
        "explicacion": """El módulo existe pero no exporta ese nombre (typo o API cambió).""",
        "soluciones": [
            "Revisá el nombre en la documentación del módulo",
            "Probá import módulo y módulo.__dict__",
        ],
    },
    r"ZeroDivisionError:": {
        "titulo": "División por cero",
        "explicacion": """Dividís o hacés módulo con divisor cero.""",
        "soluciones": [
            "Validá el divisor antes de operar",
            "Revisá datos de entrada y casos borde",
        ],
    },
}

ERRORES_JS = {
    r"TS2304:|Cannot find name": {
        "titulo": "Nombre no encontrado (TypeScript)",
        "explicacion": """tsc no encuentra la variable, función o tipo. Falta declaración, import o el nombre está mal escrito.""",
        "soluciones": [
            "Importá lo que falta: import { x } from './mod'",
            "Declará la variable o parámetro con tipo si aplica",
            "Revisá mayúsculas/minúsculas y shadowing",
            "Si es global de librería, agregá tipos (@types/...) o declare module",
        ],
    },
    r"TS2307:|Cannot find module": {
        "titulo": "Módulo no resuelto (TypeScript/Node)",
        "explicacion": """El import apunta a un paquete o ruta que no existe en node_modules o el path relativo es incorrecto.""",
        "soluciones": [
            "npm install / pnpm add / yarn add el paquete",
            "Verificá la ruta relativa (./ ../) y la extensión si usás resolución estricta",
            "Revisá \"moduleResolution\" y \"paths\" en tsconfig",
            "En ESM vs CJS, el entry export del paquete puede diferir",
        ],
    },
    r"TS2322:|not assignable to type": {
        "titulo": "Tipos no asignables (TypeScript)",
        "explicacion": """Asignás o devolvés un valor que no encaja con el tipo anotado o inferido.""",
        "soluciones": [
            "Ajustá el tipo esperado o el valor (conversión explícita si es seguro)",
            "Usá uniones, genéricos o narrowing (if, switch, asserts)",
            "Revisá null/undefined con strictNullChecks",
        ],
    },
    r"TS2345:|Argument of type": {
        "titulo": "Argumento no compatible (TypeScript)",
        "explicacion": """Los argumentos de la llamada no coinciden con la firma (cantidad o tipos).""",
        "soluciones": [
            "Compará con la definición de la función/método",
            "Ajustá objetos literales con satisfies o tipos explícitos",
            "Revisá opcionales, valores por defecto y overloads",
        ],
    },
    r"ReferenceError:\s*": {
        "titulo": "Variable no definida (JavaScript)",
        "explicacion": """Usás un identificador que no existe en este scope en tiempo de ejecución (typo, let/const en otro bloque, falta de global).""",
        "soluciones": [
            "Declará con let/const/var antes de usar",
            "Revisá imports/exports en módulos ES",
            "En navegador: script order, type=\"module\", y globals (window)",
        ],
    },
    r"TypeError: Cannot read propert(y|ies) of (undefined|null)": {
        "titulo": "Acceso a undefined/null (JavaScript)",
        "explicacion": """Leés una propiedad o llamás algo sobre un valor undefined o null (datos async, API opcional, typo de clave).""",
        "soluciones": [
            "Validá con optional chaining: obj?.prop",
            "Comprobá antes: if (x != null)",
            "Revisá await/promesas y el shape de JSON",
        ],
    },
    r"TypeError:.*is not a function": {
        "titulo": "No es una función (JavaScript)",
        "explicacion": """Llamás como función algo que es otro tipo (undefined, objeto, número) o pisaste el nombre.""",
        "soluciones": [
            "console.log(typeof x) para ver qué es en runtime",
            "Revisá default export vs named import",
            "Cuidado con métodos extraídos que pierden this (usá .bind o arrow)",
        ],
    },
    r"SyntaxError: (Unexpected token|Invalid or unexpected token)": {
        "titulo": "Token inesperado (sintaxis JS)",
        "explicacion": """El parser encontró un símbolo que no encaja (falta coma/parentesis, JSON truncado, JSX sin transpilar, etc.).""",
        "soluciones": [
            "Revisá la línea y la anterior: llaves, paréntesis, comillas",
            "Si es JSON, validá con un linter o json.parse aislado",
            "Asegurate de que Babel/tsc estén configurados para la sintaxis que usás",
        ],
    },
    r"MODULE_NOT_FOUND|Error: Cannot find module": {
        "titulo": "Módulo no encontrado (Node)",
        "explicacion": """Node no pudo resolver el require/import: paquete no instalado, ruta errónea o resolución ESM/CJS.""",
        "soluciones": [
            "Instalá dependencias en el directorio del proyecto",
            "Verificá package.json \"type\": \"module\" vs require",
            "Para paths relativos, revisá cwd y extensiones (.js vs .ts compilado)",
        ],
    },
    r"EADDRINUSE|address already in use": {
        "titulo": "Puerto en uso (Node/servidor)",
        "explicacion": """Otro proceso ya escucha en ese puerto.""",
        "soluciones": [
            "Cambiá el puerto en configuración o variable de entorno",
            "Encontrá y cerrá el proceso: ss -tlnp / lsof -i :PUERTO",
        ],
    },
}

ERRORES_RUST = {
    r"error\[E0382\]: borrow of moved value": {
        "titulo": "Uso después de mover (ownership)",
        "explicacion": """Moviste el valor y luego intentás usarlo otra vez sin clonar/prestar correctamente.""",
        "soluciones": [
            "Usá referencias & o &mut según corresponda",
            ".clon() si necesitás duplicar (con costo)",
            "Reestructurá para no mover antes de tiempo",
        ],
    },
    r"error\[E0599\]: no method named": {
        "titulo": "Método no encontrado para el tipo",
        "explicacion": """El tipo no implementa ese método o falta trait en scope.""",
        "soluciones": [
            "use trait_correcto::Trait;",
            "Verificá que sea el tipo que creés (inferencia)",
            "Implementá el trait o usá el método correcto",
        ],
    },
    r"error\[E0277\]:.*trait bound.*not satisfied": {
        "titulo": "Límites de traits no satisfechos",
        "explicacion": """Falta una implementación de trait para los tipos que pasás (genéricos).""",
        "soluciones": [
            "Implementá el trait requerido para tu tipo",
            "Ajustá los genéricos con where",
            "Usá tipos que ya satisfagan el bound",
        ],
    },
}


def bases_por_lenguaje():
    return {
        "C": ERRORES_C,
        "C++": ERRORES_C,
        "C#": ERRORES_CSHARP,
        "Python": ERRORES_PYTHON,
        "JavaScript": ERRORES_JS,
        "Rust": ERRORES_RUST,
    }
