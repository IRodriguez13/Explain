# Fichas --man para Rust: errores rustc + warnings. Claves = explain/patterns/rust_*.py

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


CAPSULES_RUST_HANDWRITTEN: dict[str, dict[str, Any]] = {
    r"error\[E0382\]: borrow of moved value": {
        "codigo_incorrecto": """fn main() {
    let s = String::from("hola");
    let t = s;
    println!("{}", s);
}""",
        "codigo_correcto": """fn main() {
    let s = String::from("hola");
    let t = s.clone();
    println!("{}", s);
}""",
        "que_paso": (
            "`String` no es `Copy`: al asignar a `t` movés la propiedad. "
            "Después `s` ya no es válido hasta que no lo reasignes."
        ),
        "regla": "Usá `.clone()`, referencias `&s`, o reestructurá para un solo dueño del valor.",
    },
    r"error\[E0308\]: mismatched types": {
        "codigo_incorrecto": """fn main() {
    let x: u32 = -1_i32 as u32;  // sorpresa si esperabas i32
}""",
        "codigo_correcto": """fn main() {
    let x: i32 = -1;
}""",
        "que_paso": (
            "El compilador esperaba un tipo distinto al de la expresión (argumentos, `return`, campos de struct)."
        ),
        "regla": "Leé el mensaje `expected … found …`; usá `into()`, `as` solo donde sea seguro, o anotá tipos intermedios.",
    },
    r"error\[E0425\]: cannot find value": {
        "codigo_incorrecto": """fn main() {
    println!("{}", desconocido);
}""",
        "codigo_correcto": """fn main() {
    let desconocido = 1;
    println!("{}", desconocido);
}""",
        "que_paso": (
            "El nombre no está en scope: falta `let`, typo, o módulo/crate no importado con `use`."
        ),
        "regla": "Verificá `use crate::…`, `pub`, y que la variable exista antes de la línea que falla.",
    },
    r"error\[E0599\]: no method named": {
        "codigo_incorrecto": """fn main() {
    let n = 3_i32;
    n.absolve();  // typo o método de otro tipo
}""",
        "codigo_correcto": """fn main() {
    let n = 3_i32;
    let _ = n.abs();
}""",
        "que_paso": "El tipo no implementa ese método o el trait que lo provee no está en scope (`use`).",
        "regla": "`use TraitAsRef` / `Deref`; revisá si necesitás `.iter()`, `AsRef`, o un trait del prelude.",
    },
    r"error\[E0277\]:.*trait bound.*not satisfied": {
        "codigo_incorrecto": """fn p<T: std::fmt::Display>(x: T) {}
fn main() { p(std::fs::File::open("/dev/null").unwrap()); }""",
        "codigo_correcto": """fn p<T: std::fmt::Display>(x: T) {}
fn main() { p(42); }""",
        "que_paso": "Falta una implementación de trait para los tipos genéricos concretos (Display, Serialize, etc.).",
        "regla": "Implementá el trait, añadí `where T: Trait`, o usá un tipo que ya cumpla el bound.",
    },
    r"error\[E0502\]: cannot borrow.*as mutable because it is also borrowed": {
        "codigo_incorrecto": """fn main() {
    let mut v = vec![1, 2, 3];
    let a = &v[0];
    v.push(4);
    println!("{}", a);
}""",
        "codigo_correcto": """fn main() {
    let mut v = vec![1, 2, 3];
    let a = v[0];
    v.push(4);
    println!("{}", a);
}""",
        "que_paso": "Tenés un préstamo inmutable activo y el compilador no permite mutar (p. ej. realloc del Vec) hasta que termine.",
        "regla": "Acortá el scope del `&`, copiá el valor (`Copy`/clone), o reordená las operaciones.",
    },
    r"error\[E0432\]: unresolved import": {
        "codigo_incorrecto": """use crate::modulo_inexistente::X;""",
        "codigo_correcto": """use crate::mi_modulo::X;  // y pub mod mi_modulo en lib/main""",
        "que_paso": "La ruta `use` no coincide con la jerarquía de módulos o falta `pub mod`.",
        "regla": "Verificá `mod foo;` / `pub use`, `Cargo.toml` [lib] path, y nombres de carpetas (`mod.rs` o `foo.rs`).",
    },
    r"error\[E0433\]: failed to resolve: use of undeclared": {
        "codigo_incorrecto": """fn main() {
    let _ = Foo;
}""",
        "codigo_correcto": """struct Foo;
fn main() {
    let _ = Foo;
}""",
        "que_paso": "Tipo, crate o macro no encontrado en scope (typo o dependencia no declarada).",
        "regla": "Añadí la dependencia en `Cargo.toml` y `use nombre_crate::…`; para macros, `use …::macro_name`.",
    },
    r"error\[E0004\]: non-exhaustive patterns": {
        "codigo_incorrecto": """enum E { A, B }
fn main() {
    let e = E::A;
    match e {
        E::A => {}
    }
}""",
        "codigo_correcto": """enum E { A, B }
fn main() {
    let e = E::A;
    match e {
        E::A => {}
        E::B => {}
    }
}""",
        "que_paso": "El `match` no cubre todas las variantes del enum (o patrones posibles).",
        "regla": "Añadí brazos para cada variante o `_ =>` si es consciente y seguro.",
    },
    r"error\[E0063\]: missing fields": {
        "codigo_incorrecto": """struct S { a: i32, b: i32 }
fn main() {
    let _ = S { a: 1 };
}""",
        "codigo_correcto": """struct S { a: i32, b: i32 }
fn main() {
    let _ = S { a: 1, b: 2 };
}""",
        "que_paso": "El literal del struct no inicializa todos los campos obligatorios.",
        "regla": "Completá campos, usá `..Default::default()` si aplica, o `#[derive(Default)]` con criterio.",
    },
    r"error\[E0384\]: cannot assign twice to immutable variable": {
        "codigo_incorrecto": """fn main() {
    let x = 1;
    x = 2;
}""",
        "codigo_correcto": """fn main() {
    let mut x = 1;
    x = 2;
}""",
        "que_paso": "Reasignás a una variable declarada con `let` sin `mut`.",
        "regla": "Usá `let mut` si el valor debe cambiar; en bucles `for` usá shadowing con nuevo `let` si aplica.",
    },
    r"error\[E0499\]: cannot borrow.*as mutable more than once": _(
        "let mut v = &mut x;\nlet a = &mut x;",
        "split_at_mut, reordenar scopes, o un solo &mut a la vez",
        "Dos préstamos mutables simultáneos al mismo dato.",
        "`split_at_mut`, índices, o tipos con interior mutability con criterio.",
    ),
    r"error\[E0373\]:.*closure may outlive": _(
        "thread::spawn(|| println!(\"{}\", s));  // s no 'static",
        "move || … con datos owned o Arc",
        "La closure captura referencias que no viven lo suficiente.",
        "`move` + owned data; lifetime `'static` para threads.",
    ),
    r"error\[E0106\]: missing lifetime specifier": _(
        "fn first_word(s: &str) -> &str { &s[0..1] }",
        "fn first_word<'a>(s: &'a str) -> &'a str",
        "El compilador no puede inferir la relación de vidas entre referencias.",
        "Anotá `<'a>` en función y tipos que referencian datos prestados.",
    ),
    r"error\[E0716\]: temporary value dropped while borrowed": _(
        "let r = &vec![1,2,3][0];",
        "let v = vec![1,2,3]; let r = &v[0];",
        "Referencia a un valor temporal que se destruye al final de la expresión.",
        "Guardá el dueño en `let` y luego prestá.",
    ),
    r"error\[E0596\]: cannot borrow.*as mutable, as it is not declared as mutable": _(
        "let v = vec![1]; v.push(2);",
        "let mut v = vec![1];",
        "Intentás mutar algo declarado sin `mut`.",
        "`let mut` o interior mutability (`RefCell`, `Mutex`) donde corresponda.",
    ),
    r"error\[E0507\]: cannot move out of.*which is behind a shared reference": _(
        "let x = &Some(String::new());\nlet y = x.take();",
        "clone() o replace con valor owned",
        "Movés valor detrás de `&` compartido.",
        "`clone`, `Option::as_ref`, APIs que devuelven copia.",
    ),
    r"error\[E0621\]: explicit lifetime required": _(
        "fn f(x: &str, y: &str) -> &str { if true { x } else { y } }",
        "fn f<'a>(x: &'a str, y: &'a str) -> &'a str",
        "El retorno debe expresar la misma vida que uno o más argumentos.",
        "Lifetime explícita que una las referencias relacionadas.",
    ),
    r"error\[E0252\]:.*is defined multiple times": _(
        "use std::fmt::Result;\nuse std::io::Result;",
        "use std::fmt::Result as FmtResult;",
        "Dos `use` traen el mismo nombre al scope.",
        "`as` alias o calificación con path completo.",
    ),
    r"error\[E0560\]:.*has no field named": _(
        "struct S { a: i32 }\nlet _ = S { a: 1, b: 2 };",
        "Solo campos que existen en el struct",
        "Campo inexistente en el literal del struct.",
        "Nombre correcto o actualizá la definición del struct.",
    ),
    r"error\[E0271\]: type mismatch resolving": _(
        "// tipo asociado del trait no coincide con el esperado",
        "Revisá el impl del trait y los type Item = …",
        "Asociated type del trait no resuelve como el caller espera.",
        "Ajustá el `impl Trait for T` o los bounds del caller.",
    ),
    r"error\[E0282\]: type annotations needed": _(
        "let x = Default::default();",
        "let x: u32 = Default::default();",
        "Inferencia ambigua: varios tipos posibles.",
        "Anotación `let x: T` o turbofish `collect::<Vec<_>>()`.",
    ),
    r"error\[E0283\]: type annotations required": _(
        "let v = Vec::new();",
        "let v: Vec<i32> = Vec::new();",
        "Similar a E0282: falta información de tipo.",
        "Tipos explícitos o argumentos genéricos suficientes.",
    ),
    r"error\[E0369\]: binary operation.*cannot be applied": _(
        "struct P;\nlet _ = P + P;",
        "impl std::ops::Add for P o derive donde aplique",
        "Falta trait para el operador (`Add`, `PartialEq`, …).",
        "`impl` manual o `#[derive]` para traits estándar.",
    ),
    r"error\[E0119\]: conflicting implementations": _(
        "impl Trait for T {}\nimpl Trait for T {}",
        "Un solo impl por (Trait, T) en el crate",
        "Dos implementaciones del mismo trait para el mismo tipo.",
        "Eliminá duplicado; `newtype` si necesitás dos semánticas.",
    ),
    r"error\[E0117\]: only traits defined in the current crate can be implemented for types": _(
        "impl ForeignTrait for ForeignType {}",
        "newtype: struct W(ForeignType); impl ForeignTrait for W",
        "Regla huérfana: no impl trait externo para tipo externo.",
        "Wrapper en tu crate o trait en tu crate.",
    ),
    r"error\[E0733\]: recursion in an async fn": _(
        "async fn fact(n: u32) -> u32 { if n<=1 {1} else { n * fact(n-1).await } }",
        "async_recursion crate o bucle + stack manual",
        "`async fn` recursiva sin boxing del futuro.",
        "Crate `async_recursion` o patrón iterativo.",
    ),
    r"linker `cc` not found|linker.*not found": _(
        "cargo build  // sin gcc",
        "sudo apt install build-essential  // o clang",
        "No hay enlazador C (gcc/clang) en PATH.",
        "Instalá toolchain de sistema; en Windows MSVC o GNU toolchain.",
    ),
    r"could not compile.*due to previous error": _(
        "// muchos errores en cascada",
        "Corregí el **primer** error que listó rustc",
        "Errores posteriores suelen ser consecuencia del primero.",
        "Arreglá de arriba hacia abajo en la salida.",
    ),
    r"error\[E0062\]: field.*specified more than once": _(
        "S { a: 1, a: 2 }",
        "Una sola vez cada campo en el literal",
        "Campo repetido en inicialización de struct.",
        "Eliminá la entrada duplicada.",
    ),
    r"error\[E0255\]:.*name.*defined multiple times": _(
        "use foo::Bar;\nstruct Bar;",
        "Renombrá import o tipo",
        "Nombre de tipo/import choca en el mismo módulo.",
        "`as` en `use` o renombrá el item local.",
    ),
    r"error\[E0603\]:.*private": _(
        "other_mod::Secret",
        "pub use o API pública del módulo",
        "Accedés a ítem no `pub` de otro módulo.",
        "`pub(crate)`, reexportación, o encapsulá acceso.",
    ),
    r"error\[E0521\]: borrowed data escapes outside of": _(
        "thread::spawn(|| println!(\"{}\", &local));",
        "move + owned o scope del thread contenido",
        "Referencia capturada no vive lo suficiente para el hilo/closure.",
        "Datos owned (`String`), `Arc`, o `'static`.",
    ),
    r"error\[E0658\]:.*feature.*is unstable": _(
        "#![feature(…)]",
        "Nightly toolchain o esperá estabilización",
        "Usás API nightly sin activar feature o sin nightly.",
        "`rustup default nightly` + `#![feature]` o evitá la API.",
    ),
    r"error\[E0505\]: cannot move out of": _(
        "// move mientras un & sigue vivo",
        "Terminá el borrow antes del move o clone",
        "Movés valor que aún está prestado.",
        "Acortá scopes; `clone` si hace falta.",
    ),
    r"error\[E0597\]:.*does not live long enough": _(
        "fn bad() -> &str { let s = String::from(\"x\"); &s }",
        "fn ok() -> String { String::from(\"x\") }",
        "Referencia sobreviviría al dato dueño.",
        "Retorná tipo owned o parámetro `&str` con lifetime de entrada.",
    ),
    r"error\[E0609\]: no field.*on type": _(
        "s.typo",
        "Nombre de campo correcto o Deref hasta el struct adecuado",
        "Typo o tipo equivocado en acceso a campo.",
        "Revisá definición del struct y `Deref`.",
    ),
    r"error\[E0616\]: field.*of.*is private": _(
        "x.secret",
        "Getter `pub` o haz el campo `pub` con criterio",
        "Campo privado de otro módulo.",
        "API pública del tipo que exponga acceso controlado.",
    ),
    r"error\[E0515\]: cannot return reference to": _(
        "fn f() -> &i32 { &42 }",
        "Retorná i32 o tomá &i32 como argumento con lifetime",
        "Referencia a local o temporal de la función.",
        "Owned o lifetime `'a` ligado a parámetro.",
    ),
    r"error: could not find `Cargo\.toml`|error: manifest path .* does not exist": _(
        "cargo build  // directorio equivocado",
        "cd al crate o --manifest-path ./cr/foo/Cargo.toml",
        "No hay `Cargo.toml` donde corre cargo.",
        "Raíz del workspace o ruta explícita al manifest.",
    ),
    r"error: linking with `.*` failed:": _(
        "undefined reference to `foo` en enlace",
        "pkg-config, -l en build.rs, instalar -dev del SO",
        "Fallo del enlazador (símbolo nativo, lib del sistema).",
        "Dependencias nativas documentadas del crate; `LD_LIBRARY_PATH` si aplica.",
    ),
    r"error: package.*depends on package.*with multiple features": _(
        "// dos deps piden features incompatibles del mismo crate",
        "Unifica features en [dependencies] o [patch]",
        "Cargo no puede resolver un único conjunto de features.",
        "Alineá `features` en Cargo.toml del workspace.",
    ),
    r"error\[E0583\]: file not found for module": _(
        "mod foo;  // sin foo.rs ni foo/mod.rs",
        "Creá el archivo o corregí el nombre del módulo",
        "`mod foo;` requiere archivo coherente con la convención.",
        "`src/foo.rs` o `src/foo/mod.rs`.",
    ),
    r"error\[E0592\]:.*duplicate definitions": _(
        "fn f() {}\nfn f() {}",
        "Una sola definición o módulos distintos",
        "Dos items con el mismo nombre en el mismo ámbito.",
        "Eliminá duplicado; usá módulos para namespaces.",
    ),
    r"warning: unused variable:": _(
        "fn main() { let x = 1; }",
        "let _x = 1; o usar x",
        "Binding declarado y nunca leído.",
        "Prefijo `_` o eliminá; `#[allow(unused_variables)]` puntual.",
    ),
    r"warning: unused import:": _(
        "use std::collections::HashMap;",
        "Quitar el use o usar el tipo",
        "Import innecesario.",
        "Limpieza; allow solo en código generado.",
    ),
    r"warning: unused.*must be used": _(
        "File::open(\"x\");",
        "let _ = File::open(\"x\")?; o manejar Result",
        "Ignorás valor `#[must_use]` (típico `Result`).",
        "Propagá `?` o manejá el error explícitamente.",
    ),
    r"warning: unreachable": _(
        "return;\nprintln!(\"nunca\");",
        "Eliminá código muerto",
        "Código después de `return`/`break`/divergencia.",
        "Flujo coherente o borrá líneas inalcanzables.",
    ),
    r"warning: variable does not need to be mutable": _(
        "let mut x = 1; println!(\"{}\", x);",
        "let x = 1;",
        "`mut` innecesario.",
        "Quitá `mut` para claridad.",
    ),
    r"warning: irrefutable.*pattern": _(
        "if let x = 5 {}",
        "if x == 5 {} o let x = 5;",
        "Patrón que siempre coincide donde sobra `if let`.",
        "Simplificá a asignación o `match` útil.",
    ),
    r"warning: hiding.*lifetime": _(
        "fn f<'a, 'a>(x: &'a str) {}",
        "Renombrá lifetimes: 'a y 'b",
        "Dos lifetimes con el mismo nombre en scope distinto.",
        "Nombres distintos para claridad del compilador.",
    ),
    r"warning: trait objects without an explicit `dyn`": _(
        "fn take(t: Box<Trait>) {}",
        "fn take(t: Box<dyn Trait>) {}",
        "Rust 2018+ exige `dyn Trait` en objetos trait.",
        "Añadí `dyn` delante del trait.",
    ),
    r"warning: unreachable pattern": _(
        "match e { E::A => {}, E::A => {}, _ => {} }",
        "Un solo arm por patrón; reordená",
        "Brazo de match cubierto por uno anterior.",
        "Eliminá duplicado o reordená patrones.",
    ),
    r"warning:.*dead_code": _(
        "fn nunca_llamada() {}",
        "Eliminá, `pub`, o #[allow(dead_code)]",
        "Función/constante/módulo no usado.",
        "API pública o limpieza; allow con criterio.",
    ),
    r"warning: unused assignment": _(
        "let mut x = 1; x = 2; x = 3;",
        "Asigná directo el valor final o usá x",
        "Asignación intermedia no leída.",
        "Simplificá lógica.",
    ),
}

__all__ = ["CAPSULES_RUST_HANDWRITTEN"]
