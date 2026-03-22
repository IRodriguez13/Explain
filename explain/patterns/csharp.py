"""Errores frecuentes del compilador C# (códigos CS)."""

ERRORES_CSHARP = {
    r"CS0103:.*does not exist in the current context": {
        "titulo": "CS0103 — nombre inexistente",
        "explicacion": "Identificador no visible: falta using, typo o scope.",
        "soluciones": ["using", "Nombre calificado", "NuGet si es externo"],
    },
    r"CS0246:.*type or namespace name .* could not be found": {
        "titulo": "CS0246 — tipo/namespace",
        "explicacion": "No resuelve el tipo.",
        "soluciones": ["using", "Referencia de proyecto", "dotnet add package"],
    },
    r"CS1061:.*does not contain a definition for": {
        "titulo": "CS1061 — miembro inexistente",
        "explicacion": "No hay método/propiedad con ese nombre.",
        "soluciones": ["Typo", "Extensión: falta using", "Versión del paquete"],
    },
    r"CS0029:.*Cannot implicitly convert type": {
        "titulo": "CS0029 — conversión implícita",
        "explicacion": "Tipos incompatibles sin cast permitido.",
        "soluciones": ["Cast explícito", ".ToString(), Parse", "as / pattern matching"],
    },
    r"CS0026:.*keyword.*this.*static": {
        "titulo": "CS0026 — this en static",
        "explicacion": "this no existe en contexto estático.",
        "soluciones": ["Quitá this o hacé el método de instancia"],
    },
    r"CS0101:.*namespace.*already contains a definition": {
        "titulo": "CS0101 — tipo duplicado",
        "explicacion": "Dos tipos con el mismo nombre en el namespace.",
        "soluciones": ["Renombrá", "partial class solo si es intencional mismo tipo"],
    },
    r"CS0111:.*already defines a member": {
        "titulo": "CS0111 — miembro duplicado",
        "explicacion": "Misma firma repetida.",
        "soluciones": ["Eliminá duplicado", "Sobrecarga con distintos parámetros"],
    },
    r"CS0122:.*inaccessible due to its protection level": {
        "titulo": "CS0122 — acceso por nivel",
        "explicacion": "private/protected impide acceso.",
        "soluciones": ["internal + InternalsVisibleTo", "API pública", "refactor"],
    },
    r"CS0162:.*Unreachable code": {
        "titulo": "CS0162 — código inalcanzable",
        "explicacion": "Código después de return/throw.",
        "soluciones": ["Eliminá o corregí flujo"],
    },
    r"CS0234:.*does not exist in the namespace": {
        "titulo": "CS0234 — tipo no está en namespace",
        "explicacion": "El subnombre no existe bajo ese namespace.",
        "soluciones": ["using correcto", "Assembly reference"],
    },
    r"CS0246:.*could not be found \(are you missing": {
        "titulo": "CS0246 — falta using o referencia",
        "explicacion": "Mensaje sugiere using o assembly.",
        "soluciones": ["Seguí la sugerencia del compilador"],
    },
    r"CS0311:.*cannot be used as type parameter": {
        "titulo": "CS0311 — restricción genérica",
        "explicacion": "El tipo argumento no cumple where T : ...",
        "soluciones": ["Implementá interfaz requerida", "Ajustá restricción"],
    },
    r"CS0400:.*could not be found in the global namespace": {
        "titulo": "CS0400 — global::",
        "explicacion": "Nombre tras global:: no existe.",
        "soluciones": ["Revisá alias global"],
    },
    r"CS0413:.*field.*assigned but its value is never used": {
        "titulo": "CS0413 — campo no usado",
        "explicacion": "Campo asignado nunca leído (warning nivel error según ruleset).",
        "soluciones": ["Usá el campo o eliminá"],
    },
    r"CS0535:.*does not implement interface member": {
        "titulo": "CS0535 — interfaz incompleta",
        "explicacion": "Falta implementar miembro de interfaz.",
        "soluciones": ["Implementá método", "clase abstracta base"],
    },
    r"CS0542:.*member names cannot be the same as their enclosing type": {
        "titulo": "CS0542 — mismo nombre que el tipo",
        "explicacion": "Miembro no puede llamarse igual que la clase contenedora.",
        "soluciones": ["Renombrá miembro"],
    },
    r"CS0552:.*conversion routines must take one parameter": {
        "titulo": "CS0552 — operador conversión",
        "explicacion": "user-defined conversion debe tener un solo parámetro.",
        "soluciones": ["Revisá firma de implicit/explicit operator"],
    },
    r"CS0708:.*static classes cannot have instance constructors": {
        "titulo": "CS0708 — static class",
        "explicacion": "static class no tiene ctor de instancia.",
        "soluciones": ["Quitá ctor o sacá static de la clase"],
    },
    r"CS0815:.*cannot assign void to an implicitly-typed variable": {
        "titulo": "CS0815 — var con void",
        "explicacion": "var no puede inferirse desde void.",
        "soluciones": ["No asignés resultado void", "Usá sentencia sola"],
    },
    r"CS1002:.*; expected": {
        "titulo": "CS1002 — falta ;",
        "explicacion": "Sintaxis esperaba punto y coma.",
        "soluciones": ["Cerrá sentencias", "Inicializadores de propiedad"],
    },
    r"CS1513:.*} expected": {
        "titulo": "CS1513 — falta }",
        "explicacion": "Llave de cierre faltante.",
        "soluciones": ["Balanceá bloques"],
    },
    r"CS1612:.*Cannot modify the return value": {
        "titulo": "CS1612 — retorno de struct",
        "explicacion": "No podés mutar campo de struct retornado sin copia intermedia.",
        "soluciones": ["Variable local = retorno; mutá local", "Cambiá a class"],
    },
    r"CS1503:.*Argument.*cannot convert from": {
        "titulo": "CS1503 — argumento incompatible",
        "explicacion": "Tipo de argumento no convertible al parámetro.",
        "soluciones": ["Cast", "Sobrecarga correcta", "nullability"],
    },
    r"CS1501:.*No overload for method.*takes": {
        "titulo": "CS1501 — sobrecarga",
        "explicacion": "Ninguna sobrecarga acepta esa cantidad/tipos.",
        "soluciones": ["Revisá parámetros opcionales", "params"],
    },
    r"CS0165:.*Use of unassigned local variable": {
        "titulo": "CS0165 — variable no asignada",
        "explicacion": "Definite assignment: camino sin asignar.",
        "soluciones": ["Inicializá en todas las ramas", "= default"],
    },
    r"CS8600:|CS8602:|CS8603:|CS8604:|CS8618:|CS8629:": {
        "titulo": "Nullable reference (CS86xx)",
        "explicacion": "Advertencias de nullability en código con #nullable enable.",
        "soluciones": ["?, !, null-forgiving con criterio", "Comprobá null antes de usar"],
    },
    r"CS4014:.*not awaited": {
        "titulo": "CS4014 — async sin await",
        "explicacion": "Llamás async Task sin await; la tarea puede perderse.",
        "soluciones": ["await", ".Wait() con cuidado", "_ = para fire-and-forget explícito"],
    },
    r"CS1998:.*async method lacks.*await": {
        "titulo": "CS1998 — async sin await",
        "explicacion": "async pero sin await (warning).",
        "soluciones": ["Quitá async", "Agregá await real"],
    },
    r"CS5001:.*does not contain.*Main.*suitable entry point": {
        "titulo": "CS5001 — sin Main",
        "explicacion": "Programa ejecutable sin punto de entrada.",
        "soluciones": ["static void Main", "OutputType Exe", "top-level statements"],
    },
    r"CS8802:.*Only one compilation unit can have top-level statements": {
        "titulo": "CS8802 — varios top-level",
        "explicacion": "Solo un archivo puede tener statements de nivel superior.",
        "soluciones": ["Envuelvé en Main en otros archivos"],
    },
    r"CS0579:.*Duplicate.*attribute": {
        "titulo": "CS0579 — atributo duplicado",
        "explicacion": "Mismo atributo repetido donde no se permite.",
        "soluciones": ["Eliminá duplicado"],
    },
    r"CS0840:.*must declare a body|abstract.*cannot have body": {
        "titulo": "CS0840 — abstract/sealed cuerpo",
        "explicacion": "abstract sin cuerpo o conflicto sealed.",
        "soluciones": ["Revisá abstract override", "Quita cuerpo en abstract"],
    },
    r"CS1729:.*does not contain a constructor": {
        "titulo": "CS1729 — constructor",
        "explicacion": "new con argumentos que no coinciden con ningún ctor.",
        "soluciones": ["Parámetros del ctor", "ctor sin parámetros"],
    },
    r"CS7036:.*There is no argument given that corresponds to the required parameter": {
        "titulo": "CS7036 — parámetro requerido",
        "explicacion": "Falta argumento obligatorio (incl. record primary ctor).",
        "soluciones": ["Nombrá parámetros opcionales", "Pasa todos los required"],
    },
    r"CS8209:.*A value of type 'void' may not be assigned": {
        "titulo": "CS8209 — void en asignación",
        "explicacion": "Tuple o out con void.",
        "soluciones": ["No captures void"],
    },
    r"CS8917:.*delegate type could not be inferred": {
        "titulo": "CS8917 — lambda delegate",
        "explicacion": "El compilador no infiere el tipo del delegate.",
        "soluciones": ["Tipá lambda: Func<...>, Action<...>", "Cast explícito"],
    },
    r"MSB3644:|MSB4018:": {
        "titulo": "Error de MSBuild",
        "explicacion": "SDK/targeting pack faltante o tarea falló.",
        "soluciones": ["Instalá targeting pack", "dotnet workload", "Revisá csproj TargetFramework"],
    },
    r"CS1001:.*Identifier expected": {
        "titulo": "CS1001 — falta identificador",
        "explicacion": "Sintaxis esperaba nombre (tipo, variable, etc.).",
        "soluciones": ["Revisá coma o palabra clave mal puesta"],
    },
    r"CS1003:.*Syntax error": {
        "titulo": "CS1003 — error de sintaxis",
        "explicacion": "Token inesperado o faltante.",
        "soluciones": ["Paréntesis/llaves", "Punto y coma"],
    },
    r"CS1525:.*Invalid expression term": {
        "titulo": "CS1525 — término inválido",
        "explicacion": "Expresión mal formada.",
        "soluciones": ["Operador o literal mal ubicado"],
    },
    r"CS1591:.*Missing XML comment": {
        "titulo": "CS1591 — XML doc",
        "explicacion": "Documentación XML obligatoria por reglas del proyecto.",
        "soluciones": ["/// summary", "Desactivá warnings doc en csproj"],
    },
    r"CS1997:.*async.*cannot return a value": {
        "titulo": "CS1997 — async void/value",
        "explicacion": "async Task vs async void mal usado.",
        "soluciones": ["Task como retorno si necesitás await externo"],
    },
    r"CS8072:.*expression tree.*contains": {
        "titulo": "CS8072 — árbol de expresión",
        "explicacion": "IQueryable/LINQ a SQL no puede traducir esa operación.",
        "soluciones": [".AsEnumerable() antes de método no traducible", "Reescribí query"],
    },
    r"CS8121:.*expression of type.*cannot be handled": {
        "titulo": "CS8121 — pattern matching",
        "explicacion": "Patrón switch/is no cubre el tipo.",
        "soluciones": ["Agregá case/when", "Tipo base común"],
    },
    r"CS8509:.*not exhaustive": {
        "titulo": "CS8509 — switch no exhaustivo",
        "explicacion": "Switch sobre enum/union requiere todos los valores.",
        "soluciones": ["default case", "Exhaustive switch C# 11+"],
    },
    r"CS8767:.*nullability.*mismatch": {
        "titulo": "CS8767 — nullability override",
        "explicacion": "Override con contrato nullable distinto al base.",
        "soluciones": ["Alineá ? y ! en override", "T pragma warning si es intencional"],
    },
    r"CS9195:.*file-scoped namespace": {
        "titulo": "CS9195 — file-scoped",
        "explicacion": "Conflicto con namespace clásico en mismo archivo.",
        "soluciones": ["Un solo estilo de namespace por archivo"],
    },
    r"CS0229:.*ambiguity|is ambiguous between": {
        "titulo": "CS0229 — ambigüedad",
        "explicacion": "Dos miembros (p. ej. herencia múltiple) compiten con el mismo nombre.",
        "soluciones": ["Calificá con nombre de clase base", "new en la derivada"],
    },
    r"CS0051:.*inconsistent accessibility": {
        "titulo": "CS0051 — accesibilidad inconsistente",
        "explicacion": "Un tipo menos accesible expone otro más accesible (public method con parámetro internal).",
        "soluciones": ["Hacé pública la clase del parámetro", "Restringí el método"],
    },
    r"CS1540:.*cannot access protected member": {
        "titulo": "CS1540 — protected vía tipo derivado",
        "explicacion": "Accedés a protected de la base a través de una referencia al tipo derivado de forma inválida.",
        "soluciones": ["this.Member como derivada", "Revisá visibilidad y static context"],
    },
    r"CS0177:.*out parameter|control leaves.*out parameter": {
        "titulo": "CS0177 — parámetro out no asignado",
        "explicacion": "Una rama sale sin asignar el out en todos los caminos.",
        "soluciones": ["Asigná out en cada rama", "throw en caso imposible"],
    },
    r"CS1622:.*cannot return a value from an iterator": {
        "titulo": "CS1622 — return en iterador",
        "explicacion": "En iterator (yield) usás return con valor en lugar de yield return.",
        "soluciones": ["yield return", "yield break"],
    },
    r"CS8370:.*feature.*not available|required language version": {
        "titulo": "CS8370 — versión de lenguaje",
        "explicacion": "Usás sintaxis de C# más nueva que la del proyecto (LangVersion).",
        "soluciones": ["<LangVersion> en csproj", "preview si es intencional"],
    },
}
