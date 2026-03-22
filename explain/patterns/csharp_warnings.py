# Advertencias del compilador C# (código CS, nivel warning). Español fijo.

WARNINGS_CSHARP = {
    r"warning CS0168:.*is declared but never used": {
        "titulo": "CS0168: variable declarada pero no usada",
        "explicacion": "La variable existe pero no se lee; a menudo restos de refactor.",
        "soluciones": ["Elimínala o usa discard _ si solo necesitas efecto lateral."],
    },
    r"warning CS0219:.*assigned but its value is never used": {
        "titulo": "CS0219: valor asignado y nunca usado",
        "explicacion": "Se asigna pero no se consume; posible error lógico.",
        "soluciones": ["Elimina la asignación o usa el valor."],
    },
    r"warning CS0414:.*assigned but its value is never read": {
        "titulo": "CS0414: campo asignado pero nunca leído",
        "explicacion": "Campo de instancia que solo se escribe.",
        "soluciones": ["Elimina el campo o léelo en algún sitio."],
    },
    r"warning CS0649:.*never assigned to": {
        "titulo": "CS0649: campo nunca asignado",
        "explicacion": "Campo no inicializado y no readonly puede quedar en default.",
        "soluciones": ["Inicializa en constructor o haz readonly con valor."],
    },
    r"warning CS1998:.*async.*no await": {
        "titulo": "CS1998: método async sin await",
        "explicacion": "async sin await compila pero no es asíncrono de verdad.",
        "soluciones": ["Quita async o añade await a operaciones asíncronas."],
    },
    r"warning CS4014:.*not awaited": {
        "titulo": "CS4014: llamada no esperada (Task)",
        "explicacion": "Se invoca un método async/Task sin await; la tarea puede quedar huérfana.",
        "soluciones": ["await la llamada o asigna y gestiona la Task explícitamente."],
    },
    r"warning CS8600:": {
        "titulo": "CS8600: posible null a tipo que no acepta null",
        "explicacion": "Nullable reference types: conversión de posible null.",
        "soluciones": ["Comprueba null, usa ! solo si garantizas invariante, o ajusta tipos."],
    },
    r"warning CS8602:": {
        "titulo": "CS8602: desreferencia de posible referencia null",
        "explicacion": "Accedes a miembro o índice sin comprobar null.",
        "soluciones": ["if (x is not null), ?., patrón de null-check."],
    },
    r"warning CS8618:": {
        "titulo": "CS8618: campo/propiedad no nullable sin inicializar",
        "explicacion": "En NRT, el constructor no asigna un valor no-null.",
        "soluciones": ["Inicializa, haz nullable (string?), o usa = null! con cuidado."],
    },
    r"warning CS8625:": {
        "titulo": "CS8625: literal null a tipo no nullable",
        "explicacion": "Pasas null donde el tipo dice que no puede ser null.",
        "soluciones": ["Cambia el parámetro a tipo nullable o evita null."],
    },
}
