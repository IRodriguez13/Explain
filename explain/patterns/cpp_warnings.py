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
}
