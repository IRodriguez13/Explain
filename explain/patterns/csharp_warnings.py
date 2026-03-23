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
    r"warning CS8601:": {
        "titulo": "CS8601: posible asignación null a no-nullable",
        "explicacion": "Asignás un posible null a un tipo referencia no marcado como nullable.",
        "soluciones": ["Comprobá null antes", "Tipo destino nullable", "operador ! solo si hay garantía"],
    },
    r"warning CS8619:": {
        "titulo": "CS8619: nullability en valores de tupla/tipos genéricos",
        "explicacion": "Los null states de los componentes no coinciden con el tipo declarado.",
        "soluciones": ["Ajustá ? en la firma", "Desempaquetá y validá cada componente"],
    },
    r"warning CS8765:": {
        "titulo": "CS8765: nullability del parámetro en override",
        "explicacion": "El override no coincide en nullability con el miembro base.",
        "soluciones": ["Alineá ? en parámetros y retorno con la clase base"],
    },
    r"warning CS1998:": {
        "titulo": "CS1998: método async sin await",
        "explicacion": "El compilador avisa: async sin await no es asíncrono de verdad (corre síncrono).",
        "soluciones": [
            "Quita async o añade await a operaciones asíncronas.",
            "Si solo devolvés un valor ya listo, usa Task.FromResult.",
        ],
    },
    r"warning CS0162:.*Unreachable code": {
        "titulo": "CS0162: código inalcanzable",
        "explicacion": "Hay código después de return/throw que nunca se ejecuta.",
        "soluciones": ["Eliminá el bloque muerto", "Corregí la condición del if"],
    },
    r"warning CS8321:": {
        "titulo": "CS8321: función local no usada",
        "explicacion": "Declaraste una función local que nunca se referencia.",
        "soluciones": ["Eliminá la función o usala", "static local si aplica en versiones nuevas"],
    },
    r"\bwarning MSB\d{3,5}:": {
        "titulo": "Advertencia MSBuild",
        "explicacion": "MSBuild avisa de referencias, rutas, caché o tareas.",
        "soluciones": ["Leé el código MSBxxxx en docs de Microsoft", "Revisá csproj y Directory.Build.props"],
    },
}
