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
}
