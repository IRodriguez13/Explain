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
        "soluciones": ["Elimínalo o permite dead_code solo si es macro/generated."],
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
}
