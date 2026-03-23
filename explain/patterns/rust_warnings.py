# Advertencias de rustc (warning:, no error). Español fijo.

WARNINGS_RUST = {
    r"warning: unused variable:": {
        "titulo": "Variable no usada (Rust)",
        "explicacion": "rustc advierte de un binding que no se lee.",
        "soluciones": ["Prefija con _var o usa _ para ignorar intencionalmente."],
    },
    r"warning: unused import:": {
        "titulo": "Import no usado",
        "explicacion": "Un use está de más.",
        "soluciones": ["Elimínalo", "#[allow(unused_imports)] solo si macro/generated"],
    },
    r"warning: unused.*must be used": {
        "titulo": "Valor #[must_use] ignorado",
        "explicacion": "Ignoraste el valor de retorno de una API marcada como must_use.",
        "soluciones": ["Maneja el Result/Option o asigna a let _ = ... con conciencia."],
    },
    r"warning: unreachable": {
        "titulo": "Código inalcanzable",
        "explicacion": "Hay código después de return/break/! que nunca se ejecuta.",
        "soluciones": ["Elimina el bloque muerto o corrige el flujo."],
    },
    r"warning: variable does not need to be mutable": {
        "titulo": "mut innecesario",
        "explicacion": "Marcas let mut pero no hay asignación que requiera mutabilidad.",
        "soluciones": ["Quita mut."],
    },
    r"warning: irrefutable.*pattern": {
        "titulo": "Patrón irrefutable en if let / match",
        "explicacion": "El patrón siempre coincide; el compilador sugiere simplificar.",
        "soluciones": ["Usa asignación normal o reestructura el match."],
    },
    r"warning: hiding.*lifetime": {
        "titulo": "Nombre de lifetime oculto",
        "explicacion": "El parámetro de lifetime tiene el mismo nombre que otro ámbito.",
        "soluciones": ["Renombra lifetimes para claridad."],
    },
    r"warning: trait objects without an explicit `dyn`": {
        "titulo": "Trait object sin dyn (edición antigua)",
        "explicacion": "Rust 2018+ prefiere Box<dyn Trait> en lugar de Box<Trait>.",
        "soluciones": ["Añade dyn delante del trait."],
    },
    r"warning: unreachable pattern": {
        "titulo": "Patrón inalcanzable en match",
        "explicacion": "Un arm de match nunca se ejecuta porque otro lo cubre antes.",
        "soluciones": ["Reordená arms", "Eliminá el patrón muerto"],
    },
    r"warning:.*dead_code": {
        "titulo": "dead_code",
        "explicacion": "Función, variable o módulo no usado (o solo usado en tests).",
        "soluciones": ["Eliminá código muerto", "#[allow(dead_code)] con criterio", "pub(crate) si es API interna"],
    },
    r"warning: unused assignment": {
        "titulo": "Asignación no usada",
        "explicacion": "Se asigna un valor que luego se sobrescribe sin leerse.",
        "soluciones": ["Eliminá la asignación intermedia", "Revisá la lógica"],
    },
    r"warning: unused import: `std::": {
        "titulo": "Import std no usado",
        "explicacion": "use std::... redundante con el prelude o sin uso.",
        "soluciones": ["Eliminá el use", "allow si macro genera"],
    },
    r"warning: unused `.*` that must be used": {
        "titulo": "must_use no usado (warning)",
        "explicacion": "Result u otro tipo #[must_use] ignorado.",
        "soluciones": ["let _ = con comentario", "Manejá el error"],
    },
    r"warning:.*#\[deprecated\]": {
        "titulo": "API deprecada (Rust)",
        "explicacion": "Llamás función o trait marcado deprecated.",
        "soluciones": ["Migrá a la API sugerida en note = \"...\""],
    },
    r"warning: variable `.*` should have a snake case name": {
        "titulo": "non_snake_case",
        "explicacion": "Convención de nombres: funciones y variables en snake_case.",
        "soluciones": ["Renombrá", "#[allow(non_snake_case)] puntual"],
    },
    r"warning:.*should have an upper camel case name": {
        "titulo": "non_camel_case_types",
        "explicacion": "Tipos y traits esperan UpperCamelCase.",
        "soluciones": ["Renombrá el tipo"],
    },
    r"warning:.*static.*should have UPPER_SNAKE_CASE": {
        "titulo": "non_upper_case_globals",
        "explicacion": "Statics y constantes suelen ir en SCREAMING_SNAKE_CASE.",
        "soluciones": ["Renombrá o allow"],
    },
    r"warning: unreachable_pub": {
        "titulo": "unreachable_pub",
        "explicacion": "pub en item que no es alcanzable fuera del crate (dead API).",
        "soluciones": ["pub(crate) o quita pub", "Si es intencional, allow"],
    },
    r"warning: trivial_numeric_casts|unnecessary_cast": {
        "titulo": "Cast innecesario",
        "explicacion": "Clippy o rustc advierte cast redundante.",
        "soluciones": ["Eliminá el cast", "Dejá si clarifica tipos"],
    },
    r"warning:.*does not need to be mutable": {
        "titulo": "mut innecesario (variante)",
        "explicacion": "Similar a variable does not need to be mutable.",
        "soluciones": ["Quita mut"],
    },
    r"warning: hiding a lifetime that's elided": {
        "titulo": "Lifetime elidido oculto",
        "explicacion": "Nombre de lifetime en firma poco claro respecto a elisión.",
        "soluciones": ["Explícita 'a o dejá elidido sin nombre duplicado"],
    },
    r"warning: type could implement `Copy`": {
        "titulo": "derive Copy sugerido",
        "explicacion": "Clippy sugiere Copy para small POD.",
        "soluciones": ["#[derive(Copy, Clone)] si semántica lo permite"],
    },
    r"warning:.*clippy::": {
        "titulo": "Clippy (lint)",
        "explicacion": "Cargo clippy emitió advertencia con nombre clippy::lint.",
        "soluciones": ["Mensaje del lint", "#[allow(clippy::...)] con criterio"],
    },
}
