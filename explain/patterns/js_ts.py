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
}
