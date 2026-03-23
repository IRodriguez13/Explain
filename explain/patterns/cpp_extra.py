"""Patrones adicionales de g++/clang++ (se fusionan sobre la base C)."""

ERRORES_CPP = {
    r"no matching function for call to|no matching constructor": {
        "titulo": "No hay sobrecarga que encaje",
        "explicacion": "Ninguna firma de función/constructor coincide con los argumentos (tipos, conversión, plantillas).",
        "soluciones": ["Revisá tipos y conversiones implícitas", "Usá static_cast explícito", "Plantillas: deducción o <Tipos> explícitos"],
    },
    r"undefined reference to.*vtable|undefined reference to typeinfo": {
        "titulo": "vtable / RTTI sin definir",
        "explicacion": "Clase polimórfica sin definir virtual o destructor virtual fuera de línea.",
        "soluciones": ["Definí funciones virtuales puras o dale cuerpo", "Destructor virtual = default en .cpp"],
    },
    r"pure virtual.*called|abstract class": {
        "titulo": "Clase abstracta",
        "explicacion": "Instanciás o llamás método puro no implementado.",
        "soluciones": ["Implementá el virtual en una clase derivada", "No instancies la base abstracta"],
    },
    r"cannot declare.*to be of.*abstract type": {
        "titulo": "Tipo abstracto",
        "explicacion": "Variable de tipo clase con métodos virtuales puros sin implementar.",
        "soluciones": ["Usá puntero/referencia a tipo concreto derivado"],
    },
    r"private within this context|protected within this context": {
        "titulo": "Acceso privado/protegido",
        "explicacion": "Accedés a miembro no accesible desde este contexto.",
        "soluciones": ["friend (con moderación)", "Getter público", "Reubicá la lógica en la clase"],
    },
    r"ambiguous overload|call of overloaded.*is ambiguous": {
        "titulo": "Llamada ambigua",
        "explicacion": "Varias sobrecargas encajan igual de bien.",
        "soluciones": ["Cast explícito al tipo deseado", "Eliminá o renombrá sobrecargas conflictivas"],
    },
    r"template.*not declared|no template named|expected template-name": {
        "titulo": "Error de plantilla",
        "explicacion": "Nombre de plantilla mal escrito, falta typename o dependiente mal calificado.",
        "soluciones": ["typename antes de tipos dependientes de T", "template<> explícita correcta"],
    },
    r"specialization of.*after instantiation|explicit specialization": {
        "titulo": "Especialización de plantilla mal ordenada",
        "explicacion": "Usás la plantilla antes de especializar o duplicás especialización.",
        "soluciones": ["Orden: declaración, especialización, uso", "Un archivo de instanciación explícita"],
    },
    r"exception specification| noexcept": {
        "titulo": "Especificación de excepciones",
        "explicacion": "noexcept dinámico o noexcept(false) vs contrato real.",
        "soluciones": ["Alineá noexcept con lo que realmente puede lanzar", "Usá noexcept solo si es garantizable"],
    },
    r"use of deleted function|call to deleted": {
        "titulo": "Función borrada (= delete)",
        "explicacion": "Llamás un constructor/operador marcado = delete.",
        "soluciones": ["Otro API (move, puntero)", "Reconsiderá el diseño de copia"],
    },
    r"use of defaulted function.*deleted implicitly": {
        "titulo": "Default implícito = delete",
        "explicacion": "El compilador no puede generar ctor/assign por miembros no copiables.",
        "soluciones": ["Definí manualmente", "Usá std::unique_ptr en vez de miembro no copiable directo"],
    },
    r"invalid initialization of reference|cannot bind non-const lvalue reference": {
        "titulo": "Referencia inválida",
        "explicacion": "Referencia no-const a temporal o a const incorrecto.",
        "soluciones": ["const T& o T&& según semántica", "Extender vida del temporal con const&"],
    },
    r"not a member of 'std'": {
        "titulo": "No es miembro de std",
        "explicacion": "Nombre usado como si fuera de std pero no existe o falta #include.",
        "soluciones": ["#include correcto (<algorithm>, <memory>, …)", "std:: explícito"],
    },
    r"unique_ptr|shared_ptr|weak_ptr": {
        "titulo": "Smart pointer (mensaje relacionado)",
        "explicacion": "Error típico al mezclar raw pointer, ownership o tipo incompleto.",
        "soluciones": ["make_unique/make_shared", "Destructor default en .cpp si tipo incompleto"],
    },
    r"dynamic_cast|bad_cast": {
        "titulo": "dynamic_cast fallido",
        "explicacion": "La jerarquía o RTTI no permite la conversión en runtime.",
        "soluciones": ["Verificá herencia virtual/polimorfismo", "Usá puntero y comprobá nullptr"],
    },
    r"constexpr|constant expression": {
        "titulo": "constexpr inválido",
        "explicacion": "Expresión no evaluable en tiempo de compilación donde se exige.",
        "soluciones": ["Simplificá la expresión", "Sacá constexpr si debe ser runtime"],
    },
    r"lambda|closure type": {
        "titulo": "Lambda / captura",
        "explicacion": "Captura [=][&] incorrecta o lifetime de referencia capturada.",
        "soluciones": ["Capturá por valor lo que sobreviva al scope", "Evitá & a local que muere"],
    },
    r"std::variant|std::optional|std::expected": {
        "titulo": "Tipo suma / opcional (STL)",
        "explicacion": "Acceso sin comprobar estado o tipo mal visitado.",
        "soluciones": ["value() solo tras has_value()", "std::visit con variant"],
    },
    r"concept|requires clause|constraint": {
        "titulo": "Concepto C++20 no satisfecho",
        "explicacion": "Los argumentos no cumplen el requires del template.",
        "soluciones": ["Ajustá tipos o el concept", "Mensaje del compilador suele listar el fallo"],
    },
    r"coroutine|co_await|co_yield": {
        "titulo": "Corrutina C++20",
        "explicacion": "Promesa, awaiter o transformación del compilador mal configurada.",
        "soluciones": ["Flags -fcoroutines / estándar correcto", "Includes y tipos de retorno promise"],
    },
    r"ODR|one definition rule|multiple definition": {
        "titulo": "Violación ODR",
        "explicacion": "Definición múltiple en unidad de traducción o enlace.",
        "soluciones": ["inline en headers para funciones pequeñas", "Definición solo en un .cpp"],
    },
    r"typename|dependent name": {
        "titulo": "Nombre dependiente de plantilla",
        "explicacion": "Falta typename o template antes de un nombre dependiente de T.",
        "soluciones": ["typename T::nested", "t.template method<>()"],
    },
    r"incomplete type.*used in nested name specifier": {
        "titulo": "Tipo incompleto en nested name",
        "explicacion": "Usás Class:: antes de que Class esté completo.",
        "soluciones": ["Mové la definición después del cuerpo completo", "Puntero opaco + .cpp"],
    },
    r"virtual function.*overrides|override error|did not override": {
        "titulo": "override/final incorrecto",
        "explicacion": "La firma no coincide con el virtual de la base.",
        "soluciones": ["const, noexcept y tipos idénticos", "Usá override explícito para detectar"],
    },
    r"std::move|use of moved-from": {
        "titulo": "Objeto movido",
        "explicacion": "Usás un valor después de std::move (estado válido pero no especificado).",
        "soluciones": ["No reutilices salvo reasignar", "Clarificá ownership"],
    },
    r"range-for|invalid range|no matching function for call to begin": {
        "titulo": "Range-for inválido",
        "explicacion": "El tipo no tiene begin/end o son incompatibles.",
        "soluciones": ["ADL y begin/end en namespace del tipo", "Usá contenedor estándar"],
    },
    r"explicit constructor|could not convert": {
        "titulo": "Conversión explícita bloqueada",
        "explicacion": "Constructor explicit no participa en conversión implícita.",
        "soluciones": ["Cast explícito T(...)", "Quita explicit si el diseño lo permite"],
    },
    r"atomic|memory_order": {
        "titulo": "std::atomic / orden de memoria",
        "explicacion": "Uso incorrecto de atomic o data race detectado por sanitizers.",
        "soluciones": ["Revisá modelos de memoria", "mutex donde atomic es insuficiente"],
    },
    r"nodiscard|ignoring return value": {
        "titulo": "Valor de retorno ignorado [[nodiscard]]",
        "explicacion": "La API marca el retorno como obligatorio de observar.",
        "soluciones": ["Asigná o comprobá el resultado", "Si es intencional, documentá por qué"],
    },
    r"static assertion failed|static_assert failed|error: static assertion": {
        "titulo": "static_assert falló",
        "explicacion": "La condición de compilación es falsa; suele ser invariante de plantilla o tamaño.",
        "soluciones": ["Corregí tipos o tamaños", "Mensaje del static_assert para contexto"],
    },
    r"bad_optional_access|optional::value": {
        "titulo": "std::optional sin valor",
        "explicacion": "Llamaste value() o el operador * sin comprobar has_value().",
        "soluciones": ["value_or", "if (opt)", "try/catch bad_optional_access"],
    },
    r"std::variant|std::get:.*bad_variant_access|bad_variant_access": {
        "titulo": "std::variant — acceso inválido",
        "explicacion": "std::get<T> no coincide con el tipo activo del variant.",
        "soluciones": ["std::holds_alternative", "std::visit"],
    },
    r"std::filesystem|filesystem_error": {
        "titulo": "std::filesystem",
        "explicacion": "Operación de rutas (copy, remove, status) falló a nivel de SO.",
        "soluciones": ["ec.message()", "Permisos y existencia de path", "path genérico vs nativo"],
    },
    r"terminate called|std::terminate|~thread.*joinable|joinable.*std::thread": {
        "titulo": "std::thread — terminación / joinable",
        "explicacion": "Thread joinable destruido sin join/detach, o terminate por excepción no capturada.",
        "soluciones": ["join() o detach()", "std::jthread", "try/catch en el hilo"],
    },
    r"resource deadlock would occur|deadlock would occur|mutex lock failed": {
        "titulo": "Deadlock o error de mutex",
        "explicacion": "std::mutex/recursive_mutex reportó orden de bloqueo inválido o interbloqueo.",
        "soluciones": ["std::scoped_lock con varios mutex", "Mismo orden de adquisición en todo el código"],
    },
    r"strict aliasing|break strict-aliasing|type-punning": {
        "titulo": "Violación de strict aliasing",
        "explicacion": "El compilador asume que punteros de tipos distintos no apuntan al mismo objeto.",
        "soluciones": ["std::memcpy entre representaciones", "std::bit_cast C++20 donde aplique"],
    },
    r"covariant return type|incompatible covariant return": {
        "titulo": "Tipo de retorno covariante",
        "explicacion": "Override con tipo de retorno distinto debe ser covariante (punteros/refs a derivada).",
        "soluciones": ["Misma jerarquía de tipos de retorno", "std::unique_ptr con deleter"],
    },
    r"non-virtual thunk|undefined reference to vtable for __cxxabiv1": {
        "titulo": "ABI / thunk / vtable",
        "explicacion": "Enlace o herencia múltiple: thunk o RTTI de Itanium ABI sin resolver.",
        "soluciones": ["Linkeá todas las unidades que definen virtual", "Orden de librerías C++"],
    },
    r"reference to local variable|returning reference to local": {
        "titulo": "Referencia a local",
        "explicacion": "Retornás T& o const T& a variable automática de la función.",
        "soluciones": ["Retorná por valor", "std::string en lugar de const char* local"],
    },
    r"exception specification of overriding function is more lax than": {
        "titulo": "noexcept más laxo en override",
        "explicacion": "Override no puede relajar noexcept respecto al virtual base.",
        "soluciones": ["Marcá noexcept igual que la base", "noexcept(false) solo si la base lo permite"],
    },
    r"allocation of incomplete type|invalid application of 'sizeof' to incomplete type '": {
        "titulo": "Tipo incompleto en new/sizeof",
        "explicacion": "new o sizeof sobre clase declarada pero no definida.",
        "soluciones": ["Incluí el header con definición completa", "Destructor = default en .cpp"],
    },
    r"default argument given for parameter": {
        "titulo": "Argumento por defecto repetido",
        "explicacion": "Valor por defecto en declaración y definición o duplicado en overloads.",
        "soluciones": ["Default solo en la declaración en header", "Una firma con defaults"],
    },
    r"std::bad_alloc|std::bad_array_new_length": {
        "titulo": "std::bad_alloc",
        "explicacion": "new falló por falta de memoria o tamaño de array inválido.",
        "soluciones": ["Reservá menos", "nothrow new o try/catch", "vector::reserve con criterio"],
    },
    r"std::length_error|std::out_of_range": {
        "titulo": "length_error / out_of_range",
        "explicacion": "string::at, vector::at o resize excede max_size o índice.",
        "soluciones": ["Comprobar size()", "at() vs [] con límites"],
    },
    r"std::future_error|std::promise|std::packaged_task": {
        "titulo": "std::future / promise",
        "explicacion": "Promise rota, get() dos veces o estado inválido.",
        "soluciones": ["Un solo get()", "set_value una vez", "shared_future si varios lectores"],
    },
    r"std::system_error|std::error_code": {
        "titulo": "std::system_error",
        "explicacion": "Operación de filesystem, thread o iostream mapeó errno a system_error.",
        "soluciones": ["code().message()", "category correcto"],
    },
    r"std::regex_error": {
        "titulo": "std::regex",
        "explicacion": "Patrón regex ECMA inválido o flag incompatible.",
        "soluciones": ["Sintaxis regex C++", "Escapá correctamente"],
    },
    r"std::ios_base::failure|std::iostream": {
        "titulo": "iostream — fallo",
        "explicacion": "Stream en failbit/badbit (lectura/escritura o conversión).",
        "soluciones": ["good() y exceptions mask", "clear() con criterio"],
    },
    r"std::thread::|std::terminate|joinable\(\)|detach": {
        "titulo": "std::thread — join/detach",
        "explicacion": "Destructor de thread joinable o terminate por excepción no capturada en join.",
        "soluciones": ["join() o detach()", "std::jthread"],
    },
    r"mutex lock failed|resource deadlock would occur|std::mutex|std::timed_mutex": {
        "titulo": "Mutex C++",
        "explicacion": "std::mutex bloqueo inválido o deadlock detectado (recursive misuse).",
        "soluciones": ["scoped_lock múltiples mutex", "Orden de bloqueo uniforme"],
    },
    r"std::condition_variable|wait.*predicate": {
        "titulo": "condition_variable",
        "explicacion": "Spurious wakeup sin predicate o notify sin lock coherente.",
        "soluciones": ["while (!pred) wait", "unique_lock correcto"],
    },
    r"std::chrono|duration_cast|time_point": {
        "titulo": "std::chrono",
        "explicacion": "Mezcla de clocks, unidades o conversión que pierde precisión.",
        "soluciones": ["duration_cast explícito", "Mismo clock para compare"],
    },
    r"std::format_error|std::vformat": {
        "titulo": "std::format (C++20)",
        "explicacion": "Cadena de formato o argumentos no coinciden con std::format.",
        "soluciones": ["{} conteos", "Tipos formateables"],
    },
    r"std::source_location|std::stacktrace": {
        "titulo": "stacktrace / source_location",
        "explicacion": "Captura de stacktrace falló o linking sin -lstdc++_libbacktrace según toolchain.",
        "soluciones": ["Flags del compilador para stacktrace", "Fallback a manual logging"],
    },
    r"std::ranges::|std::views::|view_closure": {
        "titulo": "std::ranges / views",
        "explicacion": "Rango no common, iterator inválido tras invalidación, o pipe mal tipado.",
        "soluciones": ["Materializá con to<vector>", "Lifetime del contenedor base"],
    },
    r"std::barrier|std::latch|std::counting_semaphore": {
        "titulo": "Sincronización C++20",
        "explicacion": "Uso incorrecto de latch/barrier/semaphore (conteo, arrive).",
        "soluciones": ["Documentación cppreference", "Contador inicial coherente"],
    },
    r"std::expected|unexpected": {
        "titulo": "std::expected (C++23)",
        "explicacion": "Acceso a valor sin comprobar has_value o error mal construido.",
        "soluciones": ["value_or", "and_then", "Comprobar antes de value()"],
    },
    r"reinterpret_cast.*strict aliasing|accessing value through.*glvalue": {
        "titulo": "reinterpret_cast / aliasing",
        "explicacion": "Violación de strict aliasing al reinterpretar punteros.",
        "soluciones": ["std::bit_cast C++20", "memcpy byte a byte"],
    },
    r"virtual function.*final|cannot override.*final": {
        "titulo": "override y final",
        "explicacion": "Intentás override de método marcado final en la base.",
        "soluciones": ["Otro nombre de método", "Quita final si el diseño lo permite"],
    },
    r"abstract type.*is not allowed for variable|instantiation of incomplete": {
        "titulo": "Tipo abstracto o incompleto",
        "explicacion": "Instanciás clase abstracta o tipo incompleto en plantilla.",
        "soluciones": ["Tipo concreto derivado", "Completar definición antes de instanciar"],
    },
    r"destructor of .* is protected|destructor of .* is private": {
        "titulo": "Destructor no accesible",
        "explicacion": "La clase tiene destructor protected/private y se intenta destruir en contexto que no es friend o derivada.",
        "soluciones": ["Heredá y exponé política de destrucción", "friend", "std::unique_ptr con deleter custom"],
    },
    r"constructor of .* is (private|protected) within this context": {
        "titulo": "Constructor no accesible",
        "explicacion": "No podés construir el objeto: ctor privado/protected (singleton, factory, error de visibilidad).",
        "soluciones": ["Método estático create()", "friend", "Hacer ctor public si el diseño lo permite"],
    },
    r"std::bad_function_call|bad_function_call": {
        "titulo": "std::bad_function_call",
        "explicacion": "Invocaste std::function vacío (sin target asignado).",
        "soluciones": ["if (f)", "Asigná lambda o puntero antes de llamar", "optional<function>"],
    },
}
