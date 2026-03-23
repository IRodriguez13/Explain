# Fichas --man para patrones solo C++ (cpp_extra + cpp_warnings). Claves = regex exactas en explain/patterns/.

from __future__ import annotations

from typing import Any

from explain.capsules.man_coverage_bulk import MAN_CPP_GAP_FILL
from explain.capsules.support_extension_capsules import CAPSULES_SUPPORT_CPP


def _(
    mal: str,
    bien: str,
    que: str,
    regla: str,
) -> dict[str, Any]:
    return {
        "codigo_incorrecto": mal,
        "codigo_correcto": bien,
        "que_paso": que,
        "regla": regla,
    }


CAPSULES_CPP_HANDWRITTEN: dict[str, dict[str, Any]] = {
    r"no matching function for call to|no matching constructor": _(
        "std::string s(3.14);  // ctor equivocado",
        "std::string s = std::to_string(3.14);",
        "Ninguna sobrecarga encaja con los argumentos (conversión, plantillas, cv-qualifiers).",
        "Revisá firmas en la doc; `static_cast`, argumentos explícitos en plantillas `f<int>(...)`.",
    ),
    r"undefined reference to.*vtable|undefined reference to typeinfo": _(
        "struct B { virtual void f(); }; // f sin definir en ningún .cpp",
        "void B::f() {}  // en un .cpp del enlace",
        "vtable/typeinfo: método virtual declarado pero no enlazado (definición ausente o TU no enlazada).",
        "Definí cada virtual; destructor virtual `= default` en .cpp si el tipo es polimórfico.",
    ),
    r"pure virtual.*called|abstract class": _(
        "Base* p = new Base();  // Base abstracta",
        "Base* p = new Derived();",
        "Instanciás o llamás método puro no implementado.",
        "Implementá en derivada; no instancies la interfaz abstracta directamente.",
    ),
    r"cannot declare.*to be of.*abstract type": _(
        "Abstract a;  // tipo con puros",
        "std::unique_ptr<Abstract> p = std::make_unique<Concrete>();",
        "Variable de tipo clase abstracta por valor.",
        "Usá puntero/smart pointer a implementación concreta.",
    ),
    r"private within this context|protected within this context": _(
        "obj.secret = 1;  // miembro private",
        "obj.set_secret(1);  // API pública",
        "Acceso a miembro no visible desde este contexto.",
        "`friend` con moderación, getters, o mové lógica dentro de la clase.",
    ),
    r"ambiguous overload|call of overloaded.*is ambiguous": _(
        "f(0);  // int vs long ambiguo",
        "f(static_cast<long>(0));",
        "Varias sobrecargas igual de buenas para los argumentos.",
        "Cast explícito o eliminá/rebautizá sobrecargas conflictivas.",
    ),
    r"template.*not declared|no template named|expected template-name": _(
        "T::type x;  // en plantilla, T dependiente",
        "typename T::type x;",
        "Falta `typename`/`template` en nombre dependiente de parámetro de plantilla.",
        "`typename` antes de tipos anidados; `t.template foo<>()` en llamadas.",
    ),
    r"specialization of.*after instantiation|explicit specialization": _(
        "// uso de foo<int> antes de template<> struct foo<int>",
        "Orden: plantilla primario, especializaciones, luego uso",
        "Especialización declarada después de primera instanciación o duplicada.",
        "Reordená headers; una especialización por conjunto de argumentos.",
    ),
    r"exception specification| noexcept": _(
        "void g() noexcept { throw 1; }",
        "void g();  // sin noexcept si puede lanzar",
        "`noexcept` no coincide con lo que la función puede lanzar.",
        "Alineá contrato `noexcept` con implementación real.",
    ),
    r"use of deleted function|call to deleted": _(
        "S a, b; S c = a + b;  // operator+ deleted",
        "Diseñá otra composición o habilitá la operación con criterio",
        "Llamás función marcada `= delete` (copia, conversión, etc.).",
        "Revisá reglas de cinco; `std::move` y ownership explícito.",
    ),
    r"use of defaulted function.*deleted implicitly": _(
        "struct S { std::mutex m; }; S a, b; a = b;",
        "Eliminá copia o definí move/copy manualmente",
        "El compilador no puede generar miembro por un miembro no copiable.",
        "`unique_ptr`, `= delete` explícitos, o implementación manual.",
    ),
    r"invalid initialization of reference|cannot bind non-const lvalue reference": _(
        "int& r = 42;",
        "const int& r = 42;",
        "Referencia no-const a temporal o binding ilegal.",
        "`const T&`, `T&&`, o variable nombrada intermedia.",
    ),
    r"not a member of 'std'": _(
        "std::println(...);  // sin header / estándar viejo",
        "#include <iostream> y API disponible en tu -std=",
        "Nombre no existe en namespace `std` o falta `#include`.",
        "Header correcto (`<memory>`, `<algorithm>`, …) y estándar C++ adecuado.",
    ),
    r"unique_ptr|shared_ptr|weak_ptr": _(
        "std::unique_ptr<Foo> p; p->bar();  // nullptr",
        "if (p) p->bar(); o make_unique",
        "Mensaje de error en torno a smart pointers (nullptr, tipo incompleto, etc.).",
        "`make_unique`/`make_shared`; destructor en .cpp si tipo incompleto.",
    ),
    r"dynamic_cast|bad_cast": _(
        "Derived& d = dynamic_cast<Derived&>(base);  // base no polimórfico o falla",
        "dynamic_cast<Derived*>(&base) y comprobá nullptr",
        "Conversión en jerarquía falla o tipo no polimórfico.",
        "Virtual en base; comprobar resultado con punteros.",
    ),
    r"constexpr|constant expression": _(
        "constexpr int x = std::rand();",
        "constexpr int x = 42;",
        "Se exige valor constante de compilación y la expresión no lo es.",
        "Simplificá o quitá `constexpr` si debe evaluarse en runtime.",
    ),
    r"lambda|closure type": _(
        "int a = 1; auto f = [&]() { return a; }; /* a muere antes */",
        "Capturá por valor [=] lo necesario o acortá lifetime",
        "Captura por referencia a objeto que no vive lo suficiente.",
        "Captura por valor o owned; cuidado con `this` en lambdas de miembro.",
    ),
    r"std::variant|std::optional|std::expected": _(
        "std::optional<int> o; int x = *o;",
        "if (o) x = *o;",
        "Acceso a `optional`/`variant` sin comprobar estado.",
        "`value_or`, `visit`, `holds_alternative`.",
    ),
    r"concept|requires clause|constraint": _(
        "void f(T x) requires Integral<T> {}",
        "Pasa un tipo que cumpla el concept o relajá la restricción",
        "Argumentos no satisfacen el `requires` del template.",
        "Leé el mensaje de sustitución fallida; ajustá tipos o el concepto.",
    ),
    r"coroutine|co_await|co_yield": _(
        "// co_await sin -std=c++20 / sin promesa",
        "Flags y tipos de retorno de corrutina según el compilador",
        "Corrutina C++20 mal configurada o tipos promise incorrectos.",
        "`-std=c++20`, includes y `co_return` coherentes con la promesa.",
    ),
    r"ODR|one definition rule|multiple definition": _(
        "inline int f() { return 1; } en .h incluido sin inline",
        "inline o una sola definición en .cpp",
        "Definición múltiple del mismo símbolo en el enlace.",
        "`inline` en header, o definición única en TU.",
    ),
    r"typename|dependent name": _(
        "typedef T::iterator It;  // T plantilla",
        "typedef typename T::iterator It;",
        "Nombre dependiente interpretado como valor en vez de tipo.",
        "`typename` y `template` donde el estándar lo exige.",
    ),
    r"incomplete type.*used in nested name specifier": _(
        "struct Opaque; void Opaque::f() {}",
        "Definí el struct antes del cuerpo de miembro",
        "Usás `Class::` antes de que la clase esté completa.",
        "Definición completa antes de métodos fuera de línea; puntero opaco + .cpp.",
    ),
    r"virtual function.*overrides|override error|did not override": _(
        "void f() override;  // firma distinta a la base",
        "Misma firma que el virtual de la base (const, noexcept)",
        "`override` no coincide con ningún virtual de la base.",
        "Copiá firma exacta; usá `override` para detectar desvíos.",
    ),
    r"std::move|use of moved-from": _(
        "auto v = std::move(a); use(a);",
        "Solo usar `a` tras reasignar o documentar estado válido no especificado",
        "Reutilizás un objeto tras `std::move` sin reasignar.",
        "No leas estado salvo contrato del tipo; reasigná antes de usar.",
    ),
    r"range-for|invalid range|no matching function for call to begin": _(
        "for (auto x : mystery) {}",
        "Tipo con begin/end ADL o contenedor estándar",
        "El tipo no tiene `begin`/`end` compatibles para range-for.",
        "Implementá begin/end en namespace del tipo o usá adaptador.",
    ),
    r"explicit constructor|could not convert": _(
        "void take(S s); take(1);  // S explicit S(int)",
        "take(S(1));",
        "`explicit` impide conversión implícita.",
        "Cast explícito o quita `explicit` si el diseño lo permite.",
    ),
    r"atomic|memory_order": _(
        "// data race o uso de atomic incorrecto",
        "Revisá orden de memoria y modelos de concurrencia",
        "Problema con `std::atomic` o carrera detectada por herramienta.",
        "`memory_order` coherente; `mutex` si el invariante es complejo.",
    ),
    r"nodiscard|ignoring return value": _(
        "std::remove(path);  // resultado ignorado",
        "if (!std::remove(path)) … o [[maybe_unused]] con criterio",
        "API `[[nodiscard]]` cuyo retorno ignorás.",
        "Comprobá `error_code`/`bool`/enum de retorno.",
    ),
    r"static assertion failed|static_assert failed|error: static assertion": _(
        "static_assert(sizeof(T) == 4);",
        "Corregí el invariante de plantilla o el tipo T",
        "Condición de `static_assert` falsa en tiempo de compilación.",
        "Mensaje del assert y tipos/tamaños esperados.",
    ),
    r"bad_optional_access|optional::value": _(
        "std::optional<int> o; o.value();",
        "if (o) *o o value_or(0)",
        "Acceso a `optional` vacío.",
        "`has_value`, `value_or`, o comprobación previa.",
    ),
    r"std::variant|std::get:.*bad_variant_access|bad_variant_access": _(
        "std::get<int>(v);  // activo es double",
        "std::holds_alternative<int>(v) o visit",
        "`get` con tipo índice incorrecto para el estado actual del variant.",
        "`visit` o comprobar alternativa activa.",
    ),
    r"std::filesystem|filesystem_error": _(
        "fs::copy(a, b);  // permiso o path",
        "ec explícito; comprobar exists/permisos",
        "Operación de filesystem falló a nivel de SO.",
        "`ec.message()`, existencia de path, permisos.",
    ),
    r"terminate called|std::terminate|~thread.*joinable|joinable.*std::thread": _(
        "std::thread t(f); }  // destructor sin join",
        "t.join(); o t.detach(); o std::jthread",
        "Hilo joinable destruido o excepción no manejada en `noexcept`.",
        "RAII con `jthread`; política join/detach clara.",
    ),
    r"resource deadlock would occur|deadlock would occur|mutex lock failed": _(
        "m1.lock(); m2.lock();  // otro hilo invierte orden",
        "std::scoped_lock lock(m1, m2);",
        "Orden de bloqueo inconsistente o `mutex` inválido.",
        "Mismo orden global de mutexes; `scoped_lock` para varios.",
    ),
    r"strict aliasing|break strict-aliasing|type-punning": _(
        "float f; *(int*)&f = 0x3f800000;",
        "std::memcpy o std::bit_cast (C++20)",
        "Punning de tipos viola strict aliasing.",
        " memcpy entre representaciones o APIs portables.",
    ),
    # --- cpp_warnings.py ---
    r"warning:.*unused.*\bthis\b": _(
        "void C::m() { /* no usa this */ }",
        "static void m() o [[maybe_unused]]",
        "Método de instancia que no usa estado (advertencia contextual).",
        "Hacé el método `static` si no necesita instancia.",
    ),
    r"warning:.*order of initialization": _(
        "// static en a.cpp depende de static en b.cpp",
        "Función local static (Meyers singleton) o init explícito",
        "Orden de init de estáticos entre TUs indefinido.",
        "Evitá dependencias entre globals; init lazy.",
    ),
    r"warning:.*catch.*by value": _(
        "catch (std::exception e) {}",
        "catch (const std::exception& e) {}",
        "catch por valor puede rebanar tipos derivados.",
        "Capturá por referencia const al tipo base o concreto.",
    ),
    r"warning:.*virtual destructor": _(
        "struct Base { virtual void f(); };  // sin virtual ~Base",
        "virtual ~Base() = default;",
        "Base polimórfica sin destructor virtual.",
        "`virtual ~Base()` en la base que se borra vía puntero a base.",
    ),
    r"warning:.*overloaded-virtual": _(
        "struct D : B { void f(int) override; };  // oculta B::f()",
        "using B::f;",
        "Nombre en derivada oculta sobrecargas homónimas de la base.",
        "`using Base::foo;` o renombrá para claridad.",
    ),
    r"warning:.*vla": _(
        "void g(int n) { int a[n]; }",
        "std::vector<int> a(n);",
        "VLA es extensión GCC, no C++ estándar.",
        "`std::vector` o `std::dynarray` / span según caso.",
    ),
    r"warning:.*sign-conversion|warning:.*sign conversion|warning:.*may change the sign of the result": _(
        "size_t u = -1;",
        "Compará y asigná con tipo coherente o cast explícito",
        "signed ↔ unsigned puede cambiar valor.",
        "`static_cast`, mismo signo en ambos lados, APIs `ssize_t` donde aplique.",
    ),
    r"warning:.*missing initializer|warning:.*missing field": _(
        "S s = { 1 };  // faltan campos",
        "Designated initializers C++20 o lista completa",
        "Agregado o struct con campos no inicializados en `{ }`.",
        "Inicialización completa o `= default` en miembros.",
    ),
    r"warning:.*old-style cast|warning:.*use of old-style cast": _(
        "int y = (int)p;",
        "reinterpret_cast / static_cast según intención",
        "C-cast oculta múltiples significados.",
        "Casts nombrados del estándar.",
    ),
    r"warning:.*polymorphic.*non-virtual destructor": _(
        "struct B { virtual void f(); ~B(); };",
        "virtual ~B() = default;",
        "Clase con virtual pero destructor no virtual.",
        "Destructor virtual en bases polimórficas.",
    ),
    r"warning:.*returning address of local|warning:.*address of stack|warning:.*stack address returned|-Wreturn-stack-address": _(
        "char* f() { char b[4]; return b; }",
        "std::string o static thread_local con contrato claro",
        "Retorno de puntero a automático.",
        "Valores owned (`std::string`, `std::vector`) o almacenamiento con lifetime válido.",
    ),
    r"warning:.*null pointer dereference|warning:.*dereference of null": _(
        "int* p = nullptr; *p = 1;",
        "if (p) *p = 1;",
        "Análisis estático infiere camino con nullptr.",
        "Comprobaciones, `optional`, contratos.",
    ),
    **CAPSULES_SUPPORT_CPP,
    **MAN_CPP_GAP_FILL,
}

__all__ = ["CAPSULES_CPP_HANDWRITTEN"]
