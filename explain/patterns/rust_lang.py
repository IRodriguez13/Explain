"""Errores frecuentes del compilador Rust (rustc)."""

ERRORES_RUST = {
    r"error\[E0382\]: borrow of moved value": {
        "titulo": "E0382 — valor movido",
        "explicacion": "Usás el valor después de moverlo.",
        "soluciones": ["& / &mut", ".clone()", "reestructurar ownership"],
    },
    r"error\[E0599\]: no method named": {
        "titulo": "E0599 — método inexistente",
        "explicacion": "El tipo no tiene ese método o falta trait en scope.",
        "soluciones": ["use Trait", "Deref a tipo que sí lo tiene"],
    },
    r"error\[E0277\]:.*trait bound.*not satisfied": {
        "titulo": "E0277 — trait bound",
        "explicacion": "Falta impl de trait para los tipos genéricos.",
        "soluciones": ["impl Trait for T", "where clause"],
    },
    r"error\[E0308\]: mismatched types": {
        "titulo": "E0308 — tipos no coinciden",
        "explicacion": "Se esperaba otro tipo.",
        "soluciones": ["Revisá anotaciones", "into() / as_ref()"],
    },
    r"error\[E0425\]: cannot find value": {
        "titulo": "E0425 — valor no encontrado",
        "explicacion": "Nombre no existe en scope.",
        "soluciones": ["import use", "typo", "orden de declaración"],
    },
    r"error\[E0433\]: failed to resolve: use of undeclared": {
        "titulo": "E0433 — no resuelto",
        "explicacion": "Path de módulo o crate incorrecto.",
        "soluciones": ["use crate::", "Cargo.toml dependency"],
    },
    r"error\[E0502\]: cannot borrow.*as mutable because it is also borrowed": {
        "titulo": "E0502 — borrow conflictivo",
        "explicacion": "Prestámutable y prestá inmutable solapan en lifetime.",
        "soluciones": ["Scope más corto", "clonar", "índices en vez de refs mixtas"],
    },
    r"error\[E0499\]: cannot borrow.*as mutable more than once": {
        "titulo": "E0499 — dos &mut",
        "explicacion": "Dos préstamos mutables simultáneos al mismo dato.",
        "soluciones": ["split_at_mut", "reordenar", "Mutex/Rc<RefCell> con cuidado"],
    },
    r"error\[E0373\]:.*closure may outlive": {
        "titulo": "E0373 — closure lifetime",
        "explicacion": "Closure captura referencia que no vive lo suficiente.",
        "soluciones": ["move closure", "owned data"],
    },
    r"error\[E0106\]: missing lifetime specifier": {
        "titulo": "E0106 — lifetime faltante",
        "explicacion": "El compilador no puede inferir 'a en referencias.",
        "soluciones": ["Anotá &'a", "elision rules en funciones"],
    },
    r"error\[E0716\]: temporary value dropped while borrowed": {
        "titulo": "E0716 — temporal en préstamo",
        "explicacion": "Referencia a valor temporal.",
        "soluciones": ["Guardá en let propio", "to_owned()"],
    },
    r"error\[E0596\]: cannot borrow.*as mutable, as it is not declared as mutable": {
        "titulo": "E0596 — no mut",
        "explicacion": "Variable no es mut.",
        "soluciones": ["let mut", "interior mutability"],
    },
    r"error\[E0507\]: cannot move out of.*which is behind a shared reference": {
        "titulo": "E0507 — move desde &",
        "explicacion": "Mover valor detrás de referencia compartida.",
        "soluciones": ["clone()", "replace/take en Option"],
    },
    r"error\[E0621\]: explicit lifetime required": {
        "titulo": "E0621 — lifetime explícito",
        "explicacion": "Relación entre referencias de retorno y args requiere 'a.",
        "soluciones": ["fn foo<'a>(x: &'a str) -> &'a str"],
    },
    r"error\[E0252\]:.*is defined multiple times": {
        "titulo": "E0252 — nombre duplicado",
        "explicacion": "use duplicado o conflicto de nombres.",
        "soluciones": ["as alias", "quitar use redundante"],
    },
    r"error\[E0560\]:.*has no field named": {
        "titulo": "E0560 — campo struct",
        "explicacion": "Struct literal con campo inexistente.",
        "soluciones": ["Nombre correcto", "actualización de struct"],
    },
    r"error\[E0004\]: non-exhaustive patterns": {
        "titulo": "E0004 — match no exhaustivo",
        "explicacion": "Faltan variantes en match.",
        "soluciones": ["_", "todos los enum variants"],
    },
    r"error\[E0271\]: type mismatch resolving": {
        "titulo": "E0271 — asociated type",
        "explicacion": "Tipo asociado de trait no coincide.",
        "soluciones": ["Revisá impl del trait"],
    },
    r"error\[E0282\]: type annotations needed": {
        "titulo": "E0282 — falta anotación",
        "explicacion": "Inferencia ambigua.",
        "soluciones": ["Tipo explícito: let x: T = ...", "turbofish ::<T>"],
    },
    r"error\[E0283\]: type annotations required": {
        "titulo": "E0283 — anotación requerida",
        "explicacion": "Similar 0282.",
        "soluciones": ["Especificá genéricos"],
    },
    r"error\[E0369\]: binary operation.*cannot be applied": {
        "titulo": "E0369 — operador binario",
        "explicacion": "Trait no implementado (Add, Eq, etc.).",
        "soluciones": ["impl Trait", "derive"],
    },
    r"error\[E0119\]: conflicting implementations": {
        "titulo": "E0119 — impl conflictivo",
        "explicacion": "Dos impl que se solapan.",
        "soluciones": ["Especialización con criterio", "newtype"],
    },
    r"error\[E0117\]: only traits defined in the current crate can be implemented for types": {
        "titulo": "E0117 — orphan rule",
        "explicacion": "No podés impl trait externo para tipo externo.",
        "soluciones": ["newtype wrapper", "trait en tu crate"],
    },
    r"error\[E0733\]: recursion in an async fn": {
        "titulo": "E0733 — async recursivo",
        "explicacion": "async fn recursiva requiere boxing.",
        "soluciones": ["async_recursion crate", "loop en vez de recursión"],
    },
    r"linker `cc` not found|linker.*not found": {
        "titulo": "Linker faltante",
        "explicacion": "Falta gcc/clang para enlazar (linux-gnu).",
        "soluciones": ["build-essential", "sudo apt install gcc"],
    },
    r"could not compile.*due to previous error": {
        "titulo": "Compilación abortada",
        "explicacion": "Errores previos impiden seguir.",
        "soluciones": ["Arreglá el primer error listado"],
    },
    r"error\[E0063\]: missing fields": {
        "titulo": "E0063 — campos faltantes en struct",
        "explicacion": "Falta inicializar campos en struct (no todos tienen default).",
        "soluciones": ["Completá el inicializador", "..Default::default()", "derive Default"],
    },
    r"error\[E0062\]: field.*specified more than once": {
        "titulo": "E0062 — campo duplicado",
        "explicacion": "El mismo campo aparece dos veces en struct literal.",
        "soluciones": ["Eliminá la duplicación"],
    },
    r"error\[E0255\]:.*name.*defined multiple times": {
        "titulo": "E0255 — nombre definido dos veces",
        "explicacion": "Import o definición duplicada en el mismo módulo.",
        "soluciones": ["as en use", "Quitar use redundante"],
    },
    r"error\[E0432\]: unresolved import": {
        "titulo": "E0432 — import no resuelto",
        "explicacion": "use crate::... o extern crate incorrecto.",
        "soluciones": ["Ruta del módulo", "Cargo.toml [dependencies]", "pub mod"],
    },
    r"error\[E0603\]:.*private": {
        "titulo": "E0603 — elemento privado",
        "explicacion": "Accedés a struct, campo o función no pública de otro módulo.",
        "soluciones": ["pub / pub(crate)", "Reexportación en lib.rs"],
    },
    r"error\[E0384\]: cannot assign twice to immutable variable": {
        "titulo": "E0384 — asignación a inmutable",
        "explicacion": "Reasignás a let sin mut.",
        "soluciones": ["let mut", "Nueva variable"],
    },
    r"error\[E0521\]: borrowed data escapes outside of": {
        "titulo": "E0521 — datos prestados escapan",
        "explicacion": "Closure o hilo intenta llevarse referencias que no viven lo suficiente.",
        "soluciones": ["'static + Arc", "owned data en move closure"],
    },
    r"error\[E0658\]:.*feature.*is unstable": {
        "titulo": "E0658 — feature inestable",
        "explicacion": "Usás API nightly sin #![feature(...)].",
        "soluciones": ["#![feature]", "O esperá estabilización", "toolchain nightly"],
    },
    r"error\[E0505\]: cannot move out of": {
        "titulo": "E0505 — move desde valor prestado",
        "explicacion": "Movés un valor que todavía está prestado en otro sitio.",
        "soluciones": ["Terminá el préstamo antes del move", "clone()", "reordená el código"],
    },
    r"error\[E0597\]:.*does not live long enough": {
        "titulo": "E0597 — vida insuficiente",
        "explicacion": "Una referencia viviría más que el dato al que apunta.",
        "soluciones": ["Owned (String, Vec) en lugar de &str interno", "Acortá el scope del prestador"],
    },
    r"error\[E0609\]: no field.*on type": {
        "titulo": "E0609 — campo inexistente",
        "explicacion": "El tipo no tiene ese campo (typo o tipo equivocado).",
        "soluciones": ["Revisá el nombre del campo", "Deref hasta el struct correcto"],
    },
    r"error\[E0616\]: field.*of.*is private": {
        "titulo": "E0616 — campo privado",
        "explicacion": "Accedés a un campo no público de otro módulo.",
        "soluciones": ["pub field", "getter público en el tipo"],
    },
    r"error\[E0515\]: cannot return (reference to|value referencing)": {
        "titulo": "E0515 — referencia a valor local",
        "explicacion": "Retornás una referencia a datos que no sobreviven a la función.",
        "soluciones": ["Tipo de retorno owned (String, Vec)", "Parámetro con lifetime de entrada"],
    },
    r"error: could not find `Cargo\.toml`|error: manifest path .* does not exist": {
        "titulo": "Cargo — sin manifest",
        "explicacion": "cargo se ejecutó en un directorio sin Cargo.toml o la ruta `--manifest-path` es incorrecta.",
        "soluciones": ["cd al crate raíz", "--manifest-path correcto"],
    },
    r"error: linking with `.*` failed:": {
        "titulo": "Enlazado Rust falló",
        "explicacion": "rustc/cargo no pudo enlazar (símbolo faltante, librería del sistema, etc.).",
        "soluciones": ["pkg-config / -l en build.rs", "Instalá dev libs (openssl, sqlite)", "target correcto"],
    },
    r"error: package.*depends on package.*with multiple features": {
        "titulo": "Cargo — features incompatibles",
        "explicacion": "Dos dependencias piden el mismo crate con conjuntos de features que no se pueden unificar.",
        "soluciones": ["[dependencies] features explícitos", "patch o versión única del crate"],
    },
    r"error\[E0583\]: file not found for module": {
        "titulo": "E0583 — archivo de módulo",
        "explicacion": "mod foo; esperaba foo.rs o foo/mod.rs y no existe.",
        "soluciones": ["Creá el archivo", "Renombrá el módulo", "pub mod path"],
    },
    r"error\[E0592\]:.*duplicate definitions": {
        "titulo": "E0592 — definición duplicada",
        "explicacion": "Dos items con el mismo nombre en el mismo ámbito (p. ej. fn repetida).",
        "soluciones": ["Eliminá la copia", "Renombrá o usá módulos distintos"],
    },
    r"error\[E0508\]: cannot move out of": {
        "titulo": "E0508 — move y Drop",
        "explicacion": "Movés parte de un valor cuyo tipo implementa Drop (p. ej. campo de array/tuple); no se puede dejar parcialmente sin ejecutar drop.",
        "soluciones": ["replace / take con Option", "clone()", "Reestructurá para owned completo"],
    },
    r"error\[E0381\]:.*(possibly uninitialized|used binding)": {
        "titulo": "E0381 — uso sin inicializar",
        "explicacion": "Leés una variable que el compilador no garantiza inicializada en ese camino.",
        "soluciones": ["Inicializá en todas las ramas", "if let / match que asigna antes de usar"],
    },
    r"error\[E0594\]: cannot assign to": {
        "titulo": "E0594 — asignación detrás de &",
        "explicacion": "Intentás mutar un campo a través de referencia compartida (&) sin interior mutability.",
        "soluciones": ["&mut en la API", "Cell/RefCell/Mutex con criterio", "Copia owned y reasigná"],
    },
    r"error\[E0428\]:.*defined multiple times": {
        "titulo": "E0428 — definición duplicada (módulo)",
        "explicacion": "El mismo item (fn, static, mod) está definido dos veces en el mismo módulo.",
        "soluciones": ["Eliminá una definición", "Unificá en un solo archivo o mod"],
    },
    r"error\[E0752\]:|`await` is only allowed in `async`": {
        "titulo": "E0752 — await fuera de async",
        "explicacion": "await solo dentro de async fn o bloque async.",
        "soluciones": ["async fn / async { }", "block_on / runtime adecuado en sync"],
    },
    r"error\[E0495\]: cannot infer an appropriate lifetime": {
        "titulo": "E0495 — lifetime ambiguo en params",
        "explicacion": "Varias referencias de entrada y el retorno no encajan en una relación de vida inferible.",
        "soluciones": ["Anotá 'a explícita en args y retorno", "Una sola referencia de entrada si aplica"],
    },
    r"error\[E0312\]: lifetime of reference outlives": {
        "titulo": "E0312 — lifetime de referencia",
        "explicacion": "La referencia viviría más que lo permitido por el borrow checker.",
        "soluciones": ["Acortá el scope", "Datos owned en el struct"],
    },
    r"error\[E0618\]: expected function, found": {
        "titulo": "E0618 — no es función",
        "explicacion": "Llamás () sobre un valor que no es fn, Fn o puntero a función.",
        "soluciones": ["Revisá si es campo vs método", "Deref con * o paréntesis"],
    },
    r"error\[E0623\]: lifetime mismatch": {
        "titulo": "E0623 — desajuste de lifetime",
        "explicacion": "Anotaciones de 'a en impl/trait no coinciden con el uso.",
        "soluciones": ["Alineá lifetimes del trait y del tipo", "Elision en métodos simples"],
    },
    r"cannot be sent between threads safely|cannot be shared between threads safely": {
        "titulo": "Send / Sync",
        "explicacion": "rustc: el tipo no implementa Send o Sync donde se exige (spawn, static, etc.).",
        "soluciones": ["Arc<Mutex<T>>", "Owned data en el closure", "rayon/channels"],
    },
    r"error: couldn't read .*\.rs|couldn't read.*Cargo\.lock": {
        "titulo": "rustc — archivo de fuente",
        "explicacion": "El compilador no pudo leer un archivo del crate (ruta, permisos, include_str!).",
        "soluciones": ["Ruta correcta en include!", "Archivo en el repo y no ignorado por error"],
    },
    r"error\[E0593\]: closure is expected to take": {
        "titulo": "E0593 — closure args",
        "explicacion": "La closure no tiene la aridad que espera Fn/FnMut/FnOnce en ese contexto.",
        "soluciones": ["Ajustá |a, b| vs |_|", "move closure"],
    },
    r"error\[E0614\]: type `.*` cannot be dereferenced": {
        "titulo": "E0614 — no desreferenciable",
        "explicacion": "Usás * sobre un tipo que no implementa Deref o no es puntero.",
        "soluciones": ["& vs *", "Implementá Deref o usá .as_ref()"],
    },
    r"error\[E0624\]: method.*is private": {
        "titulo": "E0624 — método privado",
        "explicacion": "Llamás método privado de otro módulo o tipo.",
        "soluciones": ["pub fn", "API pública en impl"],
    },
    r"error\[E0635\]: unknown feature": {
        "titulo": "E0635 — feature desconocida",
        "explicacion": "#![feature(x)] no existe en esta toolchain.",
        "soluciones": ["Quita feature o usá nightly correcta", "Renombre si fue renombrada"],
    },
    r"error\[E0689\]: can't call method.*on ambiguous numeric type": {
        "titulo": "E0689 — numérico ambiguo",
        "explicacion": "Literal o expresión sin tipo; método numérico ambiguo.",
        "soluciones": ["Sufijo 1i32, 1.0f64", "Anotación de tipo explícita"],
    },
    r"error\[E0714\]:.*pro macro panicked": {
        "titulo": "E0714 — proc macro panic",
        "explicacion": "Un procedural macro hizo panic! durante la expansión.",
        "soluciones": ["Versión del macro", "Input al macro válido"],
    },
    r"error\[E0724\]: `await` is only allowed inside `async` functions and blocks": {
        "titulo": "E0724 — await",
        "explicacion": "await en contexto no async (similar E0752 según versión).",
        "soluciones": ["async fn o bloque async", "block_on"],
    },
    r"error\[E0774\]: `derive` may only be applied to": {
        "titulo": "E0774 — derive inválido",
        "explicacion": "#[derive] en item que no lo admite.",
        "soluciones": ["Solo struct/enum/union", "Quita derive del item incorrecto"],
    },
    r"error\[E0782\]: expected a type, found": {
        "titulo": "E0782 — tipo esperado",
        "explicacion": "Sintaxis de tipo incorrecta (genéricos, turbofish mal formado).",
        "soluciones": ["::<T> en posición correcta", "Revisá use<> en impl"],
    },
    r"error\[E0793\]:.*reference to mutable static": {
        "titulo": "E0793 — static mut",
        "explicacion": "Acceso a static mut requiere unsafe y es fácil data race.",
        "soluciones": ["Mutex<LazyLock>", "Evitá static mut"],
    },
    r"error: the crate `.*` is compiled with the panic strategy": {
        "titulo": "Panic strategy incompatible",
        "explicacion": "Mezcla de crates panic=abort vs unwind en el enlace.",
        "soluciones": ["profile.* panic en Cargo.toml unificado", "Misma strategy en deps"],
    },
    r"error: failed to run custom build command for": {
        "titulo": "build.rs falló",
        "explicacion": "build script del crate devolvió error o no encontró lib del sistema.",
        "soluciones": ["pkg-config", "VPKG_CONFIG_PATH", "README del crate nativo"],
    },
    r"error: linking with `cc` failed:.*undefined reference to `_Unwind_Resume`": {
        "titulo": "Enlace — unwinding / libgcc",
        "explicacion": "Mezcla de objetos C++/Rust y runtime de excepciones faltante.",
        "soluciones": ["-C link-arg", "Mismo stdlib", "panic=abort coherente"],
    },
    r"error: environment variable `.*` not defined": {
        "titulo": "Variable de entorno en compile-time",
        "explicacion": "env!(...) o option_env en build sin la variable.",
        "soluciones": ["export VAR", ".env en tooling de build"],
    },
    r"error: couldn't load codegen backend|cannot find.*librustc_codegen": {
        "titulo": "Backend de codegen",
        "explicacion": "Instalación de Rust corrupta o mezcla de toolchain.",
        "soluciones": ["rustup component add", "rustup reinstall"],
    },
    r"error: the name `.*` is defined multiple times `use`": {
        "titulo": "use duplicado o conflicto",
        "explicacion": "Dos imports con el mismo nombre en scope.",
        "soluciones": ["as alias", "Prelude y use explícito"],
    },
    r"error\[E0253\]: `.*` is not a module": {
        "titulo": "E0253 — no es módulo",
        "explicacion": "use path::foo asume módulo pero foo es otro item.",
        "soluciones": ["Ruta use correcta", "pub mod"],
    },
    r"error\[E0401\]: can't use generic parameters from outer function": {
        "titulo": "E0401 — genérico externo",
        "explicacion": "Fn interna o impl anidado intenta usar tipo genérico del padre mal.",
        "soluciones": ["Reestructurá en trait", "Tipo explícito en closure"],
    },
    r"error\[E0525\]: expected a closure that implements the `Fn` trait": {
        "titulo": "E0525 — Fn vs FnMut vs FnOnce",
        "explicacion": "La closure captura de forma que no satisface el bound requerido.",
        "soluciones": ["move", "clone antes de capturar", "Cambiar bound a FnMut"],
    },
    r"error\[E0559\]: variant `.*` does not have a field named": {
        "titulo": "E0559 — campo de enum",
        "explicacion": "Struct variant del enum no tiene ese campo.",
        "soluciones": ["Nombres de campos correctos", "Tuple vs struct variant"],
    },
    r"error\[E0569\]: bounds are not satisfied": {
        "titulo": "E0569 — bounds (objeto)",
        "explicacion": "Trait object o impl no cumple bounds adicionales.",
        "soluciones": ["dyn Trait + Send", "where clause"],
    },
    r"error\[E0584\]: file for module `.*` found at both": {
        "titulo": "E0584 — módulo duplicado",
        "explicacion": "rustc encontró dos archivos candidatos para el mismo módulo (foo.rs y foo/mod.rs).",
        "soluciones": ["Dejá solo una convención", "Renombrá o mové el archivo sobrante"],
    },
    r"error\[E0728\]: `await` is only allowed inside `async`": {
        "titulo": "E0728 — await fuera de async",
        "explicacion": "Usás .await en función no async o bloque incorrecto.",
        "soluciones": ["async fn", "block_on en main sync", "spawn_blocking"],
    },
    r"error\[E0794\]:": {
        "titulo": "E0794 — restricción const / feature",
        "explicacion": "rustc rechaza una operación en contexto const o una feature asociada (mensaje depende de la versión).",
        "soluciones": ["rustc --explain E0794", "Sacá const donde no aplica", "Canal nightly estable"],
    },
}
