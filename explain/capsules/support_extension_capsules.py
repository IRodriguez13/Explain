# Cápsulas --man para el lote support_extension (patrones añadidos en 0.6.8).
# Claves = regex exactas en explain/patterns/*.py.

from __future__ import annotations

from typing import Any


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


CAPSULES_SUPPORT_C: dict[str, dict[str, Any]] = {
    r"fatal error: (out of memory|memory exhausted)|cannot allocate memory": _(
        "/* un solo .c incluye miles de headers con inline masivo */",
        "/* particionar TU, menos -O3/LTO en desarrollo, más RAM o swap */",
        "El compilador pidió memoria y el SO la negó o agotó el proceso.",
        "Reducí el coste por unidad de traducción; perfilá con `time`/`usr/bin/time -v`.",
    ),
    r"fatal error: (error writing to|could not write)": _(
        "gcc -c huge.c -o /solo_lectura/out.o",
        "gcc -c huge.c -o $TMPDIR/out.o  # o directorio con cuota y permisos",
        "No se pudo escribir el objeto o un temporal intermedio.",
        "Comprobá espacio (`df`), permisos y que `TMPDIR` sea válido.",
    ),
    r"redeclaration of enumerator|enumerator .* redefined": _(
        "enum E { A, A };",
        "enum E { A, B };",
        "El mismo identificador aparece dos veces como enumerador.",
        "Un nombre por caso; revisá headers duplicados.",
    ),
    r"variable has incomplete type 'void'|variable of type void": _(
        "void x;",
        "char buf[1];  /* u otro tipo concreto */",
        "`void` no tiene tamaño: no podés tener variables `void`.",
        "Usá `void*` u otro tipo objeto.",
    ),
    r"invalid application of 'sizeof' to void|sizeof\(void\)": _(
        "sizeof(void)",
        "sizeof(char)  /* o el tipo real */",
        "`sizeof` no está definido para `void` en C estándar.",
        "Aplicá `sizeof` a un tipo completo o a `*ptr` con tipo conocido.",
    ),
}

CAPSULES_SUPPORT_C_WARN: dict[str, dict[str, Any]] = {
    r"warning:.*\[-Wshadow\]": _(
        "int x = 1; if (1) { int x = 2; (void)x; }",
        "int x = 1; if (1) { int y = 2; (void)y; }",
        "Un nombre interno oculta uno del ámbito exterior.",
        "Renombrá o desactivá `-Wshadow` solo con criterio documentado.",
    ),
    r"warning:.*\[-Wstrict-aliasing\]": _(
        "float f; *(int*)&f = 1;",
        "memcpy(&i, &f, sizeof i);  /* o std-compatible alias */",
        "Acceso al mismo almacenamiento vía tipos no permitidos para aliasing.",
        "Respetá strict aliasing o usá `char`/memcpy según el estándar.",
    ),
    r"warning:.*\[-Wjump-misses-init\]": _(
        "goto l;\n{ int a = 1; l: (void)a; }",
        "{ int a; goto l; a = 1; l: (void)a; }  /* o reestructurar */",
        "El control salta por encima de la inicialización de un automático.",
        "Reordená bloques o usá `goto` solo hacia etiquetas que no crucen init.",
    ),
}

CAPSULES_SUPPORT_CPP: dict[str, dict[str, Any]] = {
    r"destructor of .* is protected|destructor of .* is private": _(
        "struct B { protected: ~B(); }; B x;",
        "struct B { public: ~B(); };  // o unique_ptr con deleter friend",
        "No podés destruir el objeto donde estás: destructor no público.",
        "Factory, `friend` o puntero con deleter que tenga acceso.",
    ),
    r"constructor of .* is (private|protected) within this context": _(
        "class S { S(); }; S s;",
        "class S { public: S(); }; S s;",
        "El constructor no es invocable desde este contexto (encapsulación).",
        "API estática `create()`, o hacé el ctor accesible al uso previsto.",
    ),
    r"std::bad_function_call|bad_function_call": _(
        "std::function<void()> f; f();",
        "std::function<void()> f = []{}; f();",
        "Llamaste `std::function` vacío.",
        "Comprobá `if (f)` o asigná un target antes de invocar.",
    ),
}

CAPSULES_SUPPORT_PYTHON: dict[str, dict[str, Any]] = {
    r"pickle\.(UnpicklingError|PicklingError)": _(
        "pickle.loads(b\"basura\")",
        "pickle.loads(trusted_bytes)  # mismo código y versión de clases",
        "Pickle inválido o clases que no coinciden con el stream.",
        "No unpicklear datos no confiables; versioná esquema y módulos.",
    ),
    r"ssl\.SSLError|SSL: CERTIFICATE_VERIFY_FAILED|certificate verify failed": _(
        "urllib.request.urlopen('https://expired.badssl.com')",
        "Actualizá CA, reloj del sistema y hostname del certificado.",
        "Falló la verificación TLS (cadena, fecha, nombre).",
        "`certifi`/`update-ca-certificates`; evitá `verify=False` en producción.",
    ),
    r"queue\.(Full|Empty):": _(
        "import queue\nq=queue.Queue(1)\nq.put(1); q.put(2, block=False)",
        "q.put(2, timeout=1)  # o consumidor en paralelo",
        "Cola llena o vacía con `block=False` (o timeout cero).",
        "Backpressure, `maxsize`, o bloqueo con timeout explícito.",
    ),
    r"zlib\.error:|CompressionError:.*zlib": _(
        "import zlib\nzlib.decompress(b\"no es gzip\")",
        "zlib.decompress(data, wbits=15)  # según formato real",
        "Flujo comprimido corrupto o parámetro `wbits` incorrecto.",
        "Validá integridad y formato (raw deflate vs zlib vs gzip).",
    ),
}

CAPSULES_SUPPORT_JS: dict[str, dict[str, Any]] = {
    r"TypeError: Failed to fetch|TypeError: Load failed|fetch failed": _(
        "await fetch('http://api')  // desde https página",
        "// Mismo origen, proxy CORS, o URL correcta",
        "Red, CORS, TLS o URL inválida impidieron la petición.",
        "Inspeccioná Network; arreglá cabeceras CORS en el servidor.",
    ),
    r"TS2589:.*(excessively deep|too complex|infinite)": _(
        "type R<T> = { x: R<T> };  // tipo recursivo sin base",
        "Introducí un tipo nominal de corte o simplificá mapped types.",
        "El checker de tipos excedió profundidad o detectó recursión infinita en tipos.",
        "Refactor genéricos; a veces ayuda subir de versión de TypeScript.",
    ),
    r"ERR_DLOPEN_FAILED|Error loading shared library|dlopen": _(
        "require('./addon.node')  // compilado para otra libc/CPU",
        "npm rebuild / instalar binario correcto para tu plataforma",
        "El addon nativo no pudo cargarse (libc, ruta, arquitectura).",
        "`ldd`/`otool -L`; recompilá para tu Node y SO.",
    ),
    r"SyntaxError: Unexpected token 'export'|Unexpected token 'import'": _(
        "export const x = 1  // en script sin type module",
        '"type": "module" en package.json o renombrá a .mjs',
        "El runtime interpretó el archivo como script clásico.",
        "Marcá módulo ESM o pasá por bundler/transpilador.",
    ),
}

CAPSULES_SUPPORT_RUST: dict[str, dict[str, Any]] = {
    r"error\[E0584\]: file for module `.*` found at both": _(
        "// foo.rs y foo/mod.rs coexisten",
        "dejá solo foo.rs o solo foo/mod.rs según convención",
        "Dos rutas resuelven el mismo módulo.",
        "Un archivo por módulo: elegí layout `mod.rs` o `foo.rs`.",
    ),
    r"error\[E0728\]: `await` is only allowed inside `async`": _(
        "fn main() { futures::executor::block_on(async { () }); }",
        "async fn main() { ... }  // o tokio::main",
        "`.await` fuera de contexto async.",
        "Marcá la función `async` o usá runtime `block_on` en el borde sync.",
    ),
    r"error\[E0794\]:": _(
        "const X: u32 = { let mut a = 1; a };",
        "const X: u32 = 1;  // solo operaciones permitidas en const",
        "Uso inválido en contexto `const` o restricción de feature asociada.",
        "Consultá `rustc --explain E0794` para tu versión exacta.",
    ),
}

CAPSULES_SUPPORT_CSHARP: dict[str, dict[str, Any]] = {
    r"CS0171:.*fully assign": _(
        "struct S { public int A; public int B; public S(int a) { A = a; } }",
        "public S(int a, int b) { A = a; B = b; }",
        "Falta asignar un campo del struct en el constructor.",
        "Constructor primario o asignación explícita a todos los campos.",
    ),
    r"CS8410:": _(
        "// ref struct en heap o regla de init incumplida",
        "// Ajustá readonly, ref struct y reglas de C# según el mensaje",
        "Violación de reglas de `readonly` o `ref struct` (mensaje largo).",
        "Leé el diagnóstico completo; alinea inicialización y restricciones del tipo.",
    ),
}

CAPSULES_SUPPORT_CSHARP_FW: dict[str, dict[str, Any]] = {
    r"MediatR\.|IRequestHandler": _(
        "services.AddMediatR(); // sin assembly de handlers",
        "services.AddMediatR(cfg => cfg.RegisterServicesFromAssembly(...));",
        "MediatR no encontró handler o falló el pipeline.",
        "Registrá ensamblados; verificá `IRequest`/`IRequestHandler` genéricos.",
    ),
    r"MassTransit\.|RabbitMqConnectionException|ConsumeContext": _(
        "// host RabbitMQ inalcanzable o credencial mala",
        "// cfg.Host(...); retry; virtual host correcto",
        "Broker o transporte rechazó conexión o consumo.",
        "URI, TLS, usuario/clave y política de reintentos; revisá dead-letter.",
    ),
}

CAPSULES_SUPPORT_ASM: dict[str, dict[str, Any]] = {
    r"avr-as:|AVR Assembler|\.arch avr": _(
        "ldi r16, 256  // inmediato fuera de rango",
        "ldi r16, 42  // 0-255 para muchas instrucciones",
        "Instrucción o inmediato inválido para el MCU AVR elegido.",
        "`-mmcu=` coherente con el datasheet; manual de instrucciones.",
    ),
    r"xtensa-as:|Xtensa assembler|ERROR at .*xtensa": _(
        ".align 5  // valor no soportado en esa variante",
        ".align 4  // potencia de 2 permitida",
        "Directiva o mnemónico no válido para el core Xtensa configurado.",
        "Alineá triple, flags y versión de toolchain (p. ej. ESP-IDF).",
    ),
}

__all__ = [
    "CAPSULES_SUPPORT_ASM",
    "CAPSULES_SUPPORT_C",
    "CAPSULES_SUPPORT_C_WARN",
    "CAPSULES_SUPPORT_CPP",
    "CAPSULES_SUPPORT_CSHARP",
    "CAPSULES_SUPPORT_CSHARP_FW",
    "CAPSULES_SUPPORT_JS",
    "CAPSULES_SUPPORT_PYTHON",
    "CAPSULES_SUPPORT_RUST",
]
