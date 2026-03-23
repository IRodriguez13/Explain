"""JavaScript, TypeScript, Node y mensajes frecuentes de bundlers/tsc."""

ERRORES_JS = {
    r"TS2304:|Cannot find name": {
        "titulo": "TS2304 — nombre no encontrado",
        "explicacion": "Identificador no declarado o fuera de scope de tipos.",
        "soluciones": ["import/export", "declare global", "@types/*"],
    },
    r"TS2307:|Cannot find module": {
        "titulo": "TS2307 — módulo no resuelto",
        "explicacion": "Path o paquete inexistente.",
        "soluciones": ["npm i", "paths y baseUrl en tsconfig", "extensiones .js en ESM"],
    },
    r"TS2322:|not assignable to type": {
        "titulo": "TS2322 — no asignable",
        "explicacion": "Valor incompatible con el tipo anotado.",
        "soluciones": ["Narrowing", "Uniones", "as solo si es seguro"],
    },
    r"TS2345:|Argument of type": {
        "titulo": "TS2345 — argumento",
        "explicacion": "Args no encajan con la firma.",
        "soluciones": ["satisfies", "Genéricos explícitos", "sobrecargas"],
    },
    r"TS2339:|Property .* does not exist on type": {
        "titulo": "TS2339 — propiedad inexistente",
        "explicacion": "El tipo no declara esa propiedad.",
        "soluciones": ["Typo", "Optional chaining", "Ampliá interfaz"],
    },
    r"TS2532:|Object is possibly 'undefined'|Object is possibly 'null'": {
        "titulo": "TS2532/18048 — posible null/undefined",
        "explicacion": "strictNullChecks: valor opcional sin comprobar.",
        "soluciones": ["if (x)", "x?.", "x! con criterio"],
    },
    r"TS18046:|is of type 'unknown'": {
        "titulo": "TS18046 — unknown",
        "explicacion": "Usás valor unknown sin narrow.",
        "soluciones": ["typeof/instanceof", "Zod/io-ts"],
    },
    r"TS7006:|implicitly has an 'any' type": {
        "titulo": "TS7006 — any implícito",
        "explicacion": "noImplicitAny: parámetro sin tipo.",
        "soluciones": ["Anotá tipo", "inferencia desde default"],
    },
    r"TS7053:|element implicitly has an 'any' type": {
        "titulo": "TS7053 — index signature",
        "explicacion": "Indexación con string/number sin firma de índice.",
        "soluciones": ["Record<string, T>", "keyof typeof"],
    },
    r"TS2614:|Module .* has no exported member": {
        "titulo": "TS2614 — export faltante",
        "explicacion": "import nombrado que el módulo no exporta.",
        "soluciones": ["export { }", "import default", "module.exports vs ESM"],
    },
    r"TS1208:|compilable module": {
        "titulo": "TS1208 — archivo no es módulo",
        "explicacion": "Falta import/export top-level; global script.",
        "soluciones": ["export {}", "isolatedModules"],
    },
    r"TS1378:|Top-level await": {
        "titulo": "TS1378 — top-level await",
        "explicacion": "Target/module no soporta await en top-level.",
        "soluciones": ["module: esnext", "async wrapper IIFE"],
    },
    r"TS2786:|JSX element implicitly has type 'any'": {
        "titulo": "TS2786 — JSX",
        "explicacion": "Falta jsx factory o tipos de React.",
        "soluciones": ["jsx: react-jsx", "@types/react"],
    },
    r"TS2305:|Module .* has no exported member": {
        "titulo": "TS2305 — miembro export",
        "explicacion": "Similar 2614: nombre export incorrecto.",
        "soluciones": ["Revisá exports del paquete", "versiones de @types"],
    },
    r"TS2554:|Expected .* arguments, but got": {
        "titulo": "TS2554 — cantidad de args",
        "explicacion": "Menos o más argumentos de los esperados.",
        "soluciones": ["Parámetros opcionales", "overload matching"],
    },
    r"TS2769:|No overload matches this call": {
        "titulo": "TS2769 — sobrecarga",
        "explicacion": "Ninguna sobrecarga encaja.",
        "soluciones": ["Cast o genéricos explícitos", "Ajustá tipos de args"],
    },
    r"TS2352:|Conversion of type .* may be a mistake": {
        "titulo": "TS2352 — cast dudoso",
        "explicacion": "Los tipos no se solapan; as puede estar mal.",
        "soluciones": ["Revisá modelo de datos", "unknown intermedio"],
    },
    r"TS2415:|Class .* incorrectly extends": {
        "titulo": "TS2415 — extends inválido",
        "explicacion": "Clase base incompatible (props privadas, etc.).",
        "soluciones": ["implements vs extends", "visibilidad"],
    },
    r"TS2515:|Non-abstract class .* does not implement": {
        "titulo": "TS2515 — interfaz incompleta",
        "explicacion": "Falta implementar miembro.",
        "soluciones": ["Implementá método", "abstract class"],
    },
    r"TS2698:|Spread types may only be created from object types": {
        "titulo": "TS2698 — spread",
        "explicacion": "Spread sobre no-objeto.",
        "soluciones": ["Asegurá objeto", "Array spread vs object"],
    },
    r"TS2741:|Property .* is missing in type": {
        "titulo": "TS2741 — propiedad faltante",
        "explicacion": "Objeto literal no satisface tipo (excess property checks).",
        "soluciones": ["Agregá prop", "as const / satisfies"],
    },
    r"TS2320:|Interface .* cannot simultaneously extend": {
        "titulo": "TS2320 — extends conflictivo",
        "explicacion": "Dos interfaces base con propiedad incompatible.",
        "soluciones": ["Renombrá", "intersection type"],
    },
    r"ReferenceError:\s*": {
        "titulo": "ReferenceError",
        "explicacion": "Variable no definida en runtime.",
        "soluciones": ["let/const antes", "import", "typeof window"],
    },
    r"TypeError: Cannot read propert(y|ies) of (undefined|null)": {
        "titulo": "Lectura sobre null/undefined",
        "explicacion": "Encadenamiento sin valor intermedio.",
        "soluciones": ["?.", "guard clauses"],
    },
    r"TypeError:.*is not a function": {
        "titulo": "No es función",
        "explicacion": "Llamás () sobre no-función.",
        "soluciones": ["default import", "typeof check"],
    },
    r"TypeError:.*is not iterable": {
        "titulo": "No iterable",
        "explicacion": "for..of sobre no-iterable.",
        "soluciones": ["Array.from", "Symbol.iterator"],
    },
    r"SyntaxError: (Unexpected token|Invalid or unexpected token)": {
        "titulo": "SyntaxError",
        "explicacion": "Parser JS falla (JSON, JSX crudo, etc.).",
        "soluciones": ["JSON válido", "transpile JSX"],
    },
    r"MODULE_NOT_FOUND|Error: Cannot find module": {
        "titulo": "Módulo Node",
        "explicacion": "require/import no resuelve.",
        "soluciones": ["npm i", "type module", "paths"],
    },
    r"ERR_REQUIRE_ESM|Must use import to load ES Module": {
        "titulo": "ERR_REQUIRE_ESM",
        "explicacion": "require() a paquete solo ESM.",
        "soluciones": ["import()", "dynamic import", "versión CJS del paquete"],
    },
    r"ERR_MODULE_NOT_FOUND": {
        "titulo": "ERR_MODULE_NOT_FOUND",
        "explicacion": "Resolución ESM fallida.",
        "soluciones": ["extensiones .js en imports relativos", "exports field package.json"],
    },
    r"EADDRINUSE|address already in use": {
        "titulo": "Puerto en uso",
        "explicacion": "listen en puerto ocupado.",
        "soluciones": ["Otro puerto", "kill proceso"],
    },
    r"ENOTFOUND|getaddrinfo": {
        "titulo": "DNS / host",
        "explicacion": "Nombre no resuelve.",
        "soluciones": ["Conectividad", "typo hostname"],
    },
    r"ETIMEDOUT|timeout": {
        "titulo": "Timeout red",
        "explicacion": "Conexión o lectura expiró.",
        "soluciones": ["Firewall", "aumentar timeout"],
    },
    r"UnhandledPromiseRejection|unhandled rejection": {
        "titulo": "Promesa rechazada sin catch",
        "explicacion": "async sin await/catch propagó rechazo.",
        "soluciones": [".catch()", "try/await", "--unhandled-rejections"],
    },
    r"Maximum call stack size exceeded": {
        "titulo": "Stack overflow",
        "explicacion": "Recursión infinita o ciclo de llamadas.",
        "soluciones": ["Caso base", "iterativo"],
    },
    r"Unexpected end of JSON input|JSON\.parse": {
        "titulo": "JSON parse",
        "explicacion": "Cadena truncada o no JSON.",
        "soluciones": ["Validá payload", "try/catch"],
    },
    r"eslint|ESLint:": {
        "titulo": "ESLint",
        "explicacion": "Regla de estilo o calidad del linter.",
        "soluciones": ["Mensaje de la regla", "eslint --fix", "desactivá regla puntual con criterio"],
    },
    r"webpack|Module parse failed|Module not found: Error: Can't resolve": {
        "titulo": "Webpack / bundler",
        "explicacion": "Loader o resolución de módulo falló.",
        "soluciones": ["alias", "loader para extensión", "instalar dependencia"],
    },
    r"vite.*Failed to resolve|Rollup.*could not resolve": {
        "titulo": "Vite/Rollup resolve",
        "explicacion": "Import no encontrado en el grafo.",
        "soluciones": ["optimizeDeps", "alias en vite.config", "peer dependency"],
    },
    r"Jest:|jest.*Cannot find module": {
        "titulo": "Jest",
        "explicacion": "Mocks o moduleNameMapper incorrectos.",
        "soluciones": ["jest.config", "transformIgnorePatterns"],
    },
    r"pnpm ERR!|npm ERR!|yarn error": {
        "titulo": "Gestor de paquetes",
        "explicacion": "Instalación o script lifecycle falló.",
        "soluciones": ["Revisá log completo", "lockfile", "node version"],
    },
    r"ExperimentalWarning|DeprecationWarning": {
        "titulo": "Warning de Node",
        "explicacion": "API experimental u obsoleta.",
        "soluciones": ["Migrá a API estable", "NODE_OPTIONS"],
    },
    r"BigInt|Cannot mix BigInt and other types": {
        "titulo": "BigInt mezclado",
        "explicacion": "Operación entre BigInt y Number sin conversión.",
        "soluciones": ["Number() si cabe", "todo BigInt"],
    },
    r"RegExp.*out of range|Invalid regular expression": {
        "titulo": "Regex inválida",
        "explicacion": "Patrón mal formado o flag incompatible.",
        "soluciones": ["Escapá caracteres", "modo u/v"],
    },
    r"import assertions|Import attribute": {
        "titulo": "Import attributes",
        "explicacion": "JSON/CSS modules requieren type en import.",
        "soluciones": ['import x from "./f.json" with { type: "json" }'],
    },
    r"DOMException|SecurityError|NotAllowedError": {
        "titulo": "API web / permisos",
        "explicacion": "Navegador bloquea (CORS, clipboard, etc.).",
        "soluciones": ["HTTPS", "headers CORS", "user gesture"],
    },
    r"RangeError: Invalid array length": {
        "titulo": "RangeError array",
        "explicacion": "length ilegal.",
        "soluciones": ["Valor dentro de 2**32-1"],
    },
    r"AssertionError|Assertion failed": {
        "titulo": "Assert (Node/test)",
        "explicacion": "assert() o expect de test falló.",
        "soluciones": ["Revisá condición e inputs del test"],
    },
    r"TS2564:|Property.*has no initializer": {
        "titulo": "TS2564 — propiedad sin inicializar",
        "explicacion": "strictPropertyInitialization: campo de clase sin valor ni en ctor.",
        "soluciones": ["Inicializá en ctor", "prop!: con criterio", "strictPropertyInitialization false"],
    },
    r"TS2451:|Cannot redeclare block-scoped variable": {
        "titulo": "TS2451 — variable redeclarada",
        "explicacion": "let/const con el mismo nombre en el mismo bloque.",
        "soluciones": ["Renombrá", "Ámbitos distintos con bloques {}"],
    },
    r"TS2588:|Cannot assign to.*because it is a constant": {
        "titulo": "TS2588 — asignación a constante",
        "explicacion": "Reasignás a const o import inmutable.",
        "soluciones": ["Usá let", "No mutés bindings de import"],
    },
    r"TS2322:.*undefined is not assignable": {
        "titulo": "TS2322 — undefined vs tipo estricto",
        "explicacion": "strictNullChecks: undefined no entra en el tipo anotado.",
        "soluciones": ["T | undefined", "Valor por defecto", "Optional chaining"],
    },
    r"ERR_SOCKET_|ECONNRESET|EPIPE|ENOTCONN": {
        "titulo": "Error de socket (Node)",
        "explicacion": "Conexión TCP cerrada por el peer, pipe roto o socket no conectado.",
        "soluciones": ["Manejo en .on('error')", "Reintentos", "Verificá que el servidor siga vivo"],
    },
    r"ERR_INVALID_ARG_TYPE|ERR_INVALID_ARG_VALUE": {
        "titulo": "Argumento inválido (Node)",
        "explicacion": "API de Node rechazó tipo o valor de parámetro.",
        "soluciones": ["Revisá docs de la función", "typeof en depuración"],
    },
    r"SyntaxError: The requested module|does not provide an export named": {
        "titulo": "ESM — export faltante",
        "explicacion": "import { x } pero el módulo no exporta ese nombre (CJS vs ESM).",
        "soluciones": ["export { }", "import default", "module.exports vs named exports"],
    },
    r"ReferenceError: require is not defined": {
        "titulo": "require en ESM",
        "explicacion": "En módulo ESM no existe require(); usá import.",
        "soluciones": ["import/createRequire", '"type": "module" y sintaxis import'],
    },
    r"TS1005:|TS1003:|TS1127:": {
        "titulo": "TS1005/1003 — sintaxis TypeScript",
        "explicacion": "Falta o sobra un token (}, ;, ), etc.) o hay palabra clave mal ubicada.",
        "soluciones": ["Revisá la línea anterior", "Balanceá genéricos <> y JSX"],
    },
    r"TS1128:|TS1109:|TS1068:": {
        "titulo": "TS1128 — declaración esperada",
        "explicacion": "El parser encontró algo donde esperaba declaración o fin de bloque.",
        "soluciones": ["Llaves de más o de menos", "export/import al inicio de módulo"],
    },
    r"TS2551:.*Did you mean": {
        "titulo": "TS2551 — propiedad inexistente (sugerencia)",
        "explicacion": "tsc sugiere un nombre parecido; suele ser typo.",
        "soluciones": ["Usá el nombre sugerido", "Revisá el tipo del objeto"],
    },
    r"TS2349:|This expression is not callable": {
        "titulo": "TS2349 — no invocable",
        "explicacion": "Tratás de llamar () algo que TypeScript no considera función.",
        "soluciones": ["Union con función vs objeto", "typeof guard", "import default vs named"],
    },
    r"TS2538:.*cannot be used as an index type": {
        "titulo": "TS2538 — índice inválido",
        "explicacion": "Tipo usado como clave de índice no es válido (p. ej. object sin firma).",
        "soluciones": ["Record<K,V>", "keyof", "as const + satisfies"],
    },
    r"ERR_PNPM_|pnpm:.*ERR_|ERR_SOCKET_TIMEOUT|ECONNREFUSED": {
        "titulo": "Red / pnpm / conexión",
        "explicacion": "pnpm o el runtime no pudo resolver red, registry o socket.",
        "soluciones": ["Proxy y registry en .npmrc", "Firewall", "Verificá URL del registry"],
    },
    r"OutOfMemoryError|JavaScript heap out of memory|FATAL ERROR: Reached heap limit": {
        "titulo": "Memoria heap (Node/V8)",
        "explicacion": "El proceso se quedó sin memoria para el heap de JS.",
        "soluciones": ["NODE_OPTIONS=--max-old-space-size=", "Revisá fugas o datasets enormes"],
    },
    r"Playwright|Error: browserType\.|Executable doesn't exist": {
        "titulo": "Playwright / navegador",
        "explicacion": "Falta instalar browsers de Playwright o la ruta del ejecutable es incorrecta.",
        "soluciones": ["npx playwright install", "PLAYWRIGHT_BROWSERS_PATH"],
    },
    r"TS18048:": {
        "titulo": "TS18048 — posible undefined",
        "explicacion": "strictNullChecks: el valor puede ser undefined y se usa sin comprobar (código distinto a TS2532 en versiones recientes).",
        "soluciones": ["if (x !== undefined)", "x?.", "valor por defecto con ??"],
    },
    r"TS18047:": {
        "titulo": "TS18047 — posible null",
        "explicacion": "strictNullChecks: puede ser null y se accede sin narrow.",
        "soluciones": ["if (x != null)", "Optional chaining", "Non-null assertion solo con invariante"],
    },
    r"TS2353:|Object literal may only specify known properties": {
        "titulo": "TS2353 — propiedad extra en literal",
        "explicacion": "El objeto literal tiene claves que el tipo destino no declara (excess property check).",
        "soluciones": ["Eliminá la propiedad", "Ampliá el tipo o usá índice con firma", "as const + satisfies con criterio"],
    },
    r"TS2344:|does not satisfy the constraint": {
        "titulo": "TS2344 — restricción genérica",
        "explicacion": "El argumento de tipo no cumple el `extends` / `where` del parámetro genérico.",
        "soluciones": ["Pasá un tipo que implemente la restricción", "Aflojá la restricción si es correcto"],
    },
    r"TS2300:|Duplicate identifier": {
        "titulo": "TS2300 — identificador duplicado",
        "explicacion": "Dos declaraciones con el mismo nombre en el mismo ámbito (import, let, type, etc.).",
        "soluciones": ["Renombrá uno", "Revisá imports duplicados o merge mal resuelto"],
    },
    r"TS2739:|Type .* is missing the following properties": {
        "titulo": "TS2739 — faltan propiedades",
        "explicacion": "El objeto no incluye todas las propiedades requeridas del tipo.",
        "soluciones": ["Completá el literal", "Hacé opcionales con ?", "Partial<T> si aplica"],
    },
    r"TS2740:": {
        "titulo": "TS2740 — tipo vacío vs requerido",
        "explicacion": "Asignás {} o un tipo sin miembros donde se esperan muchas propiedades.",
        "soluciones": ["Construí el objeto con todas las keys", "Record o tipo más laxo"],
    },
    r"TS7016:|Could not find a declaration file": {
        "titulo": "TS7016 — sin tipos (.d.ts)",
        "explicacion": "Paquete JS sin @types o sin types en package.json.",
        "soluciones": ["npm i -D @types/paquete", "declare module 'x'", "skipLibCheck temporal"],
    },
    r"TS7030:|Not all code paths return a value": {
        "titulo": "TS7030 — return faltante",
        "explicacion": "Función con tipo de retorno distinto de void/undefined y algún camino no retorna.",
        "soluciones": ["return en cada rama", "throw en imposibles", "cambiar retorno a void"],
    },
    r"TS2448:": {
        "titulo": "TS2448 — uso antes de declarar",
        "explicacion": "Referenciás let/const/class antes de su declaración (temporal dead zone).",
        "soluciones": ["Reordená el código", "function hoisting si aplica"],
    },
    r"TS2454:": {
        "titulo": "TS2454 — variable sin asignar",
        "explicacion": "Usás una variable antes de que TypeScript vea asignación en todos los caminos.",
        "soluciones": ["Inicializá al declarar", "asigná en todas las ramas"],
    },
    r"TS2571:|Object is of type 'unknown'": {
        "titulo": "TS2571 — unknown en operación",
        "explicacion": "Operás sobre unknown (distinto de TS18046 que marca el acceso directo).",
        "soluciones": ["typeof / instanceof", "Zod/schema", "as unknown as T solo con criterio"],
    },
    r"TS2326:|Types of property.*are incompatible": {
        "titulo": "TS2326 — propiedad incompatible",
        "explicacion": "Asignación entre objetos: una propiedad del mismo nombre tiene tipos incompatibles.",
        "soluciones": ["Alineá tipos de la propiedad", "Union o genérico más preciso"],
    },
    r"TS2367:|This comparison appears to be unintentional": {
        "titulo": "TS2367 — comparación inútil",
        "explicacion": "Comparás tipos que nunca pueden ser iguales (p. ej. literal distintos sin overlap).",
        "soluciones": ["Corregí la condición", "Unión de tipos coherente", "type guard real"],
    },
    r"TS2686:|React refers to a UMD global": {
        "titulo": "TS2686 — React UMD global",
        "explicacion": "jsx/react sin import explícito y tsconfig no usa la fábrica automática nueva.",
        "soluciones": ["import React from 'react' (jsx clásico)", "jsx: react-jsx y sin import React"],
    },
    r"TS6192:|All imports in import declaration are unused": {
        "titulo": "TS6192 — imports sin usar",
        "explicacion": "noUnusedLocals: todos los símbolos del import están sin referencia.",
        "soluciones": ["Eliminá el import", "Usá el símbolo", "prefijo _ si es intencional"],
    },
    r"TS6196:|declared but never used": {
        "titulo": "TS6196 — declarado sin usar",
        "explicacion": "Variable, parámetro o función no usada con noUnusedLocals/noUnusedParameters.",
        "soluciones": ["Eliminá o usá", "prefijo _ en parámetros", "ajustá tsconfig si es ruido"],
    },
    r"TS2591:|Cannot find name 'module'": {
        "titulo": "TS2591 — module en Node types",
        "explicacion": "Usás `module` o `require` sin tipos de Node (@types/node).",
        "soluciones": ["npm i -D @types/node", "types en tsconfig"],
    },
    r"TS1472:|catch or finally expected": {
        "titulo": "TS1472 — try incompleto",
        "explicacion": "Bloque try sin catch ni finally válido.",
        "soluciones": ["Agregá catch o finally", "Balanceá llaves"],
    },
    r"TS1484:|.*is a type and must be imported using a type-only import": {
        "titulo": "TS1484 — import type",
        "explicacion": "verbatimModuleSyntax o aislamiento: el símbolo es solo tipo y debe importarse con `import type`.",
        "soluciones": ["import type { T }", "export type"],
    },
    r"TS2209:|The project root is ambiguous": {
        "titulo": "TS2209 — raíz ambigua",
        "explicacion": "Varios tsconfig compiten; tsc no elige proyecto único.",
        "soluciones": ["-p tsconfig.json explícito", "references en solution style"],
    },
    r"TS5098:|Option .* can only be used when": {
        "titulo": "TS5098 — opción tsconfig incompatible",
        "explicacion": "Combinación moduleResolution / module / bundler no permitida en esa versión.",
        "soluciones": ["Alineá module y moduleResolution según doc de TS", "Subí versión de TypeScript"],
    },
    r"ERR_INVALID_URL|TypeError: Invalid URL": {
        "titulo": "URL inválida",
        "explicacion": "new URL() o fetch con string mal formado o esquema ausente.",
        "soluciones": ["Base URL en segundo arg", "encodeURIComponent en query"],
    },
    r"ERR_HTTP_HEADERS_SENT|Cannot set headers after they are sent": {
        "titulo": "Headers ya enviados",
        "explicacion": "En Express/Node intentás setHeader o send después de iniciar la respuesta.",
        "soluciones": ["Un solo res.send/end", "return tras error handler"],
    },
    r"Circular dependency detected|Cannot access .* before initialization": {
        "titulo": "Dependencia circular (módulos)",
        "explicacion": "Import circular deja bindings en temporal dead zone o undefined.",
        "soluciones": ["Extraé código común a tercer módulo", "import dinámico import()", "Refactor de capas"],
    },
    r"TypeError: Assignment to constant variable": {
        "titulo": "Asignación a constante",
        "explicacion": "Reasignás a const (o binding de import).",
        "soluciones": ["Usá let", "No reasignés imports"],
    },
    r"ReferenceError: Cannot access .* before initialization": {
        "titulo": "TDZ — acceso antes de inicializar",
        "explicacion": "Leés let/const/class antes de su línea de inicialización.",
        "soluciones": ["Reordená declaraciones", "evitá ciclos de inicialización"],
    },
    r"SyntaxError: Identifier .* has already been declared": {
        "titulo": "Identificador duplicado (JS)",
        "explicacion": "let/const/class con el mismo nombre dos veces en el mismo bloque.",
        "soluciones": ["Renombrá", "Fusioná declaraciones"],
    },
    r"TS4111:|Property comes from an index signature": {
        "titulo": "TS4111 — index signature estricta",
        "explicacion": "noPropertyAccessFromIndexSignature: no podés usar dot con claves de índice.",
        "soluciones": ["obj['key'] con corchetes", "Record<K,V> explícito"],
    },
    r"TS4114:|The member .* must be an object literal": {
        "titulo": "TS4114 — override literal",
        "explicacion": "override en campo de clase exige objeto literal en algunas configuraciones estrictas.",
        "soluciones": ["Objeto inline o ajustá la regla", "Revisá versión TS"],
    },
    r"TS7027:|Unreachable code detected": {
        "titulo": "TS7027 — código inalcanzable",
        "explicacion": "allowUnreachableCode off: código después de return/throw.",
        "soluciones": ["Eliminá código muerto", "Corregí la condición"],
    },
    r"TS7022:|.*implicitly has type 'any'": {
        "titulo": "TS7022 — any implícito (variable)",
        "explicacion": "Variable sin inicializador y sin anotación; inferencia cae en any.",
        "soluciones": ["Tipo explícito o inicializador", "noImplicitAny"],
    },
    r"TS7023:|.*implicitly has return type 'any'": {
        "titulo": "TS7023 — any en retorno de función",
        "explicacion": "Función sin tipo de retorno anotado y cuerpo no infiere bien.",
        "soluciones": ["Anotá : ReturnType", "return explícitos en todas las ramas"],
    },
    r"ERR_USE_AFTER_CLOSE|write after end": {
        "titulo": "Stream cerrado",
        "explicacion": "Escribís en stream o socket después de end/destroy.",
        "soluciones": ["Evento 'finish' antes de más writes", "Revisá piping"],
    },
    r"FATAL ERROR:.*Allocation failed|Ineffective mark-compacts": {
        "titulo": "V8 — compactación / memoria",
        "explicacion": "GC no pudo liberar suficiente; heap muy fragmentado o presión extrema.",
        "soluciones": ["--max-old-space-size", "Reducí retención de objetos grandes"],
    },
    r"TS1002:|TS1005:|TS1009:|TS1010:": {
        "titulo": "TS100x — carácter o token",
        "explicacion": "Lexer/parser: string sin cerrar, token inesperado o faltante.",
        "soluciones": ["Comillas y backticks balanceados", "JSX solo con jsx en tsconfig"],
    },
    r"TS1127:|TS1128:|TS1160:": {
        "titulo": "TS1127 — unterminated template",
        "explicacion": "Template literal sin cerrar o comentario sin fin.",
        "soluciones": ["Cerrá ` y ${}", "Anidar template con escape"],
    },
    r"TS17004:|TS17008:|TS2604:|JSX element": {
        "titulo": "TS17004 — JSX",
        "explicacion": "Archivo .ts con JSX o falta factory React.",
        "soluciones": ["Renombrá a .tsx", "jsx en tsconfig", "jsxImportSource"],
    },
    r"TS2515:|TS2654:|TS2656:": {
        "titulo": "TS25xx — abstract / super",
        "explicacion": "Instanciás clase abstracta o super() mal en derived.",
        "soluciones": ["Implementá métodos abstractos", "super() antes de this en ctor"],
    },
    r"TS2678:|TS1360:": {
        "titulo": "TS2678 — switch / equality",
        "explicacion": "Comparación en switch o === siempre false por tipos disjuntos.",
        "soluciones": ["Unificá tipos", "Discriminated union"],
    },
    r"TS2365:|TS2362:|TS2363:": {
        "titulo": "TS236x — operador aritmético",
        "explicacion": "Operador aritmético aplicado a tipos no numéricos o mezcla ilegal.",
        "soluciones": ["Number()", "Narrowing", "BigInt consistente"],
    },
    r"TS2347:|TS2556:": {
        "titulo": "TS2347/2556 — spread / rest",
        "explicacion": "Spread sobre no-iterable o demasiados args para rest.",
        "soluciones": ["Array.isArray", "Tupla con longitud fija"],
    },
    r"TS2578:|TS7028:": {
        "titulo": "TS2578 — label / unused",
        "explicacion": "Label sin uso o JSX spread booleano sospechoso.",
        "soluciones": ["Eliminá label muerto", "Revisá {...cond && x}"],
    },
    r"TS6307:|TS1470:": {
        "titulo": "TS6307 — archivo no es módulo",
        "explicacion": "Proyecto references / bundler espera módulo y el archivo es script global.",
        "soluciones": ["export {}", "isolatedModules", "include en tsconfig"],
    },
    r"TS2358:|TS1361:": {
        "titulo": "TS2358 — import type vs value",
        "explicacion": "Usás como valor algo importado solo como tipo (verbatimModuleSyntax).",
        "soluciones": ["import type separado", "import normal para valor"],
    },
    r"TS2790:|TS2792:": {
        "titulo": "TS279x — operand delete",
        "explicacion": "delete sobre propiedad no opcional o readonly.",
        "soluciones": ["Omit en tipo", "Rest object sin la key"],
    },
    r"ZodError|zod\.ZodError": {
        "titulo": "Zod",
        "explicacion": "Schema Zod rechazó el parse (coerce, refine, union).",
        "soluciones": ["error.flatten()", ".safeParse()", "Mensajes .issues"],
    },
    r"SyntaxError: await is only valid in async function": {
        "titulo": "await fuera de async (JS)",
        "explicacion": "await en función no async o en top-level sin soporte de módulo.",
        "soluciones": ["async function", "type module + engines que soporten TLA"],
    },
    r"TypeError: Converting circular structure to JSON": {
        "titulo": "JSON circular",
        "explicacion": "JSON.stringify encontró referencia circular.",
        "soluciones": ["Replacer con seen Set", "DTO sin ciclos"],
    },
    r"URIError:|decodeURI|encodeURI": {
        "titulo": "URIError",
        "explicacion": "decodeURIComponent con secuencia % inválida.",
        "soluciones": ["Validá input", "try/catch"],
    },
    r"ERR_UNKNOWN_FILE_EXTENSION|ERR_UNKNOWN_BUILTIN_MODULE": {
        "titulo": "Node — extensión o builtin",
        "explicacion": "Node no reconoce la extensión sin loader o builtin inexistente.",
        "soluciones": ["--experimental-loader", "Extensión .cjs/.mjs explícita"],
    },
    r"ERR_UNSUPPORTED_DIR_IMPORT|ERR_PACKAGE_PATH_NOT_EXPORTED": {
        "titulo": "Node — exports / directorio",
        "explicacion": "import de carpeta sin index resuelto o path no exportado en package.json.",
        "soluciones": ["exports field del paquete", "Import archivo concreto"],
    },
    r"ERR_WORKER_OUT_OF_MEMORY|ERR_WORKER_UNSERIALIZABLE": {
        "titulo": "worker_threads",
        "explicacion": "Worker sin memoria o postMessage con estructura no clonable.",
        "soluciones": ["Structured clone rules", "Transferable buffers", "Más heap al worker"],
    },
    r"ERR_INTERNAL_ASSERTION|Assertion failed:": {
        "titulo": "Node — aserción interna",
        "explicacion": "Bug o estado corrupto en Node/libuv (raro).",
        "soluciones": ["Actualizá Node LTS", "Repro mínima para issue"],
    },
    r"Transform failed with.*error|Parse error.*esbuild": {
        "titulo": "esbuild / transform",
        "explicacion": "Parse o transform falló en herramienta (sintaxis, target).",
        "soluciones": ["target es2020", "Sintaxis soportada por esbuild"],
    },
    r"WebAssembly\.(Compile|Link|Runtime)Error": {
        "titulo": "WebAssembly",
        "explicacion": "Wasm inválido, import faltante o trap en runtime.",
        "soluciones": ["wasm-validate", "Imports alinear con instancia"],
    },
    r"TransformStream|ReadableStream.*locked": {
        "titulo": "Streams (WHATWG)",
        "explicacion": "Stream ya tiene reader locked o tee mal usado.",
        "soluciones": ["Un reader a la vez", "Tee antes de consumir"],
    },
    r"DOMException.*QuotaExceededError": {
        "titulo": "QuotaExceededError",
        "explicacion": "localStorage/indexedDB superó cuota del origen.",
        "soluciones": ["Limpiá storage", "Pedir persistencia", "estimate()"],
    },
    r"AggregateError:|Promise any": {
        "titulo": "AggregateError",
        "explicacion": "Promise.any rechazó todas; varias razones en .errors.",
        "soluciones": ["Revisá errors[]", "Promise.allSettled para diagnóstico"],
    },
    r"TypeError: Failed to fetch|TypeError: Load failed|fetch failed": {
        "titulo": "fetch / red (runtime)",
        "explicacion": "El navegador o runtime rechazó la petición (CORS, red, certificado, URL inválida).",
        "soluciones": ["Consola red / Network tab", "CORS en servidor", "HTTPS y certificados"],
    },
    r"TS2589:.*(excessively deep|too complex|infinite)": {
        "titulo": "TS2589 — tipos demasiado profundos",
        "explicacion": "Instanciación recursiva de tipos (mapped types, inferencia) supera el límite del checker.",
        "soluciones": ["Simplificá genéricos", "Tipo intermedio nominal", "typescript@next vs estable"],
    },
    r"ERR_DLOPEN_FAILED|Error loading shared library|dlopen": {
        "titulo": "Módulo nativo (dlopen)",
        "explicacion": "addon .node o .so no carga: ruta, GLIBC, arquitectura o dependencia faltante.",
        "soluciones": ["ldd / otool", "Recompilar addon para tu Node/OS", "LD_LIBRARY_PATH"],
    },
    r"SyntaxError: Unexpected token 'export'|Unexpected token 'import'": {
        "titulo": "Sintaxis ESM en script",
        "explicacion": "import/export en archivo interpretado como script clásico (no module).",
        "soluciones": ["type module en package.json", "extensión .mjs", "Bundler que transpile"],
    },
}
