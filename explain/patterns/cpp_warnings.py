# Advertencias típicas de C++ (GCC/Clang). Español fijo.

WARNINGS_CPP = {
    r"warning:.*unused.*\bthis\b": {
        "titulo": "this no usado en función miembro",
        "explicacion": "En C++11+ puedes marcar métodos estáticos en sentido lógico; a veces el compilador advierte de capturas o firmas.",
        "soluciones": ["Si el método no usa estado, hazlo static o libera de la clase."],
    },
    r"warning:.*order of initialization": {
        "titulo": "Orden de inicialización de globales/estáticos",
        "explicacion": "Los objetos estáticos en distintas unidades de traducción se inicializan en orden no especificado entre TUs.",
        "soluciones": ["Evita dependencias entre inicializadores estáticos; usa función local static (Meyers)."],
    },
    r"warning:.*catch.*by value": {
        "titulo": "catch por valor en lugar de referencia",
        "explicacion": "Capturar excepciones por valor puede rebanar (slicing) tipos derivados.",
        "soluciones": ["Usa catch (const std::exception& e) o referencia al tipo concreto."],
    },
    r"warning:.*virtual destructor": {
        "titulo": "Clase polimórfica sin destructor virtual",
        "explicacion": "Si borras por puntero a base, sin virtual ~Base() el destructor derivado no corre.",
        "soluciones": ["Añade virtual ~Clase() = default; en la base polimórfica."],
    },
    r"warning:.*overloaded-virtual": {
        "titulo": "virtual oculta sobrecargas de la base",
        "explicacion": "En C++, al sobrescribir un virtual se ocultan otras sobrecargas del mismo nombre en la base.",
        "soluciones": ["using Base::foo; en la derivada o renombra para claridad."],
    },
    r"warning:.*vla": {
        "titulo": "Array de longitud variable (VLA) en C++",
        "explicacion": "VLA es extensión de GCC, no C++ estándar.",
        "soluciones": ["Usa std::vector o std::array con tamaño fijo."],
    },
    r"warning:.*sign-conversion|warning:.*sign conversion": {
        "titulo": "Conversión con cambio de signo",
        "explicacion": "signed ↔ unsigned puede cambiar el valor representado.",
        "soluciones": ["static_cast explícito", "Mismo signo en ambos lados"],
    },
    r"warning:.*missing initializer|warning:.*missing field": {
        "titulo": "Inicializador de miembro faltante",
        "explicacion": "Agregado o struct con campos no listados en { }.",
        "soluciones": ["Lista completa de campos", "= default en miembros", "Designated initializers C++20"],
    },
    r"warning:.*old-style cast|warning:.*use of old-style cast": {
        "titulo": "C-style cast",
        "explicacion": "(T)x es más peligroso que static_cast/reinterpret_cast explícitos.",
        "soluciones": ["static_cast / reinterpret_cast / const_cast según intención"],
    },
    r"warning:.*polymorphic.*non-virtual destructor": {
        "titulo": "Destructor no virtual en clase polimórfica",
        "explicacion": "Clase con virtual methods pero ~Class no virtual → riesgo al borrar por base*.",
        "soluciones": ["virtual ~Base() = default;", "O prohibí polimorfismo por base"],
    },
    r"warning:.*returning address of local|warning:.*address of stack|warning:.*stack address returned|-Wreturn-stack-address": {
        "titulo": "Puntero a objeto de pila (UB al usarlo después)",
        "explicacion": "Se devuelve o se guarda la dirección de un automático; al salir del ámbito deja de ser válida.",
        "soluciones": ["std::string/std::vector en lugar de char[] local", "static thread_local si aplica", "asignación en heap con contrato claro"],
    },
    r"warning:.*null pointer dereference|warning:.*dereference of null": {
        "titulo": "Posible desreferencia de nullptr (UB si ocurre)",
        "explicacion": "El compilador infiere un camino donde se usa un puntero nulo; en C++ desreferenciar nullptr es UB.",
        "soluciones": ["Comprobaciones explícitas", "optional/expected", "Contratos en API"],
    },
}
