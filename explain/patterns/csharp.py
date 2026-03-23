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
    r"CS0161:.*not all code paths return a value": {
        "titulo": "CS0161 — return faltante",
        "explicacion": "Función con tipo de retorno no void no retorna en todos los caminos.",
        "soluciones": ["return en cada rama", "throw en casos imposibles"],
    },
    r"CS0236:.*field initializers cannot reference": {
        "titulo": "CS0236 — inicializador de campo",
        "explicacion": "Un campo no estático no puede inicializarse con otro campo de instancia en el mismo orden.",
        "soluciones": ["Inicializá en el constructor", "static readonly para constantes de tipo"],
    },
    r"CS0841:.*Cannot use local variable": {
        "titulo": "CS0841 — variable antes de asignar",
        "explicacion": "Leés una variable local antes de que el compilador considere asignada (definite assignment).",
        "soluciones": ["Inicializá antes del uso", "Reordená declaraciones"],
    },
    r"CS0200:.*Property or indexer.*cannot be assigned to": {
        "titulo": "CS0200 — propiedad solo lectura",
        "explicacion": "Asignás a una propiedad sin setter o con init ya consumido.",
        "soluciones": ["Agregá set", "Usá ctor/init", "Campo privado con lógica"],
    },
    r"CS1504:.*Source file.*could not be opened": {
        "titulo": "CS1504 — archivo fuente",
        "explicacion": "El compilador no pudo abrir un .cs (ruta, permisos, archivo borrado).",
        "soluciones": ["Ruta en csproj", "Archivo en disco", "Encoding"],
    },
    r"NETSDK1045:|The current .NET SDK does not support": {
        "titulo": "SDK .NET insuficiente",
        "explicacion": "El TargetFramework requiere un SDK más nuevo del instalado.",
        "soluciones": ["Instalá SDK más reciente", "global.json con versión", "Bajá netX.Y del csproj"],
    },
    r"CS0119:.*is not valid in the given context": {
        "titulo": "CS0119 — tipo usado como variable",
        "explicacion": "El nombre es un tipo pero lo usás como valor (confusión con static/namespace).",
        "soluciones": ["new T()", "Nombre calificado correcto", "using alias"],
    },
    r"CS0121:.*call is ambiguous": {
        "titulo": "CS0121 — llamada ambigua",
        "explicacion": "Varias sobrecargas encajan igual de bien.",
        "soluciones": ["Cast de argumentos", "Eliminá sobrecargas redundantes"],
    },
    r"CS0136:.*cannot declare.*in this scope": {
        "titulo": "CS0136 — sombra en scope",
        "explicacion": "Declarás local con el mismo nombre que otro en un scope envolvente.",
        "soluciones": ["Renombrá", "Bloques { } más pequeños"],
    },
    r"CS0152:.*switch statement contains multiple cases": {
        "titulo": "CS0152 — case duplicado",
        "explicacion": "Dos case con el mismo valor constante.",
        "soluciones": ["Unificá casos", "Corregí el literal duplicado"],
    },
    r"CS0176:.*static member.*cannot be accessed": {
        "titulo": "CS0176 — miembro static",
        "explicacion": "Accedés a static con instancia en lugar del tipo.",
        "soluciones": ["Tipo.Miembro en lugar de instancia.Miembro"],
    },
    r"CS0266:.*Cannot implicitly convert type": {
        "titulo": "CS0266 — conversión implícita con pérdida",
        "explicacion": "Conversión numérica posible pero requiere cast explícito (p. ej. double a int).",
        "soluciones": ["(int)x con criterio", "Convert.ToInt32"],
    },
    r"CS1063:.*Extension methods.*defined on": {
        "titulo": "CS1063 — extensión en tipo equivocado",
        "explicacion": "El método de extensión no aplica al tipo del receptor.",
        "soluciones": ["using del namespace de extensión", "Revisá tipo del this"],
    },
    r"CS1508:.*Resource identifier.*has already been used": {
        "titulo": "CS1508 — recurso embebido duplicado",
        "explicacion": "Dos archivos con el mismo nombre lógico en recursos del ensamblado.",
        "soluciones": ["LogicalName distinto en .csproj", "Renombrá archivos"],
    },
    r"CS1739:.*best overload.*does not have a parameter named": {
        "titulo": "CS1739 — argumento nombrado",
        "explicacion": "Pasás nombre: valor que no coincide con ningún parámetro de la sobrecarga elegida.",
        "soluciones": ["Revisá nombres de parámetros", "Orden posicional"],
    },
    r"CS1977:.*Cannot use a lambda expression as an argument": {
        "titulo": "CS1977 — lambda y dynamic",
        "explicacion": "dynamic no puede enlazar overload con lambda sin tipo de delegate explícito.",
        "soluciones": ["Cast a Action/Func", "Evitá dynamic en esa llamada"],
    },
    r"CS8070:.*feature.*top-level statements": {
        "titulo": "CS8070 — top-level statements",
        "explicacion": "Mezcla incorrecta de top-level con otras unidades o versión de lenguaje.",
        "soluciones": ["Un solo archivo top-level", "LangVersion preview si aplica"],
    },
    r"CS9113:.*parameter.*is unread": {
        "titulo": "CS9113 — parámetro primary constructor no usado",
        "explicacion": "En record/class con primary constructor, un parámetro no se usa en el cuerpo.",
        "soluciones": ["Usá el campo", "Descartá con _", "Quita el parámetro"],
    },
    r"CS0128:.*already defined in this scope": {
        "titulo": "CS0128 — variable local duplicada",
        "explicacion": "Dos locales con el mismo nombre en el mismo bloque.",
        "soluciones": ["Renombrá", "Bloques anidados"],
    },
    r"CS0145:.*const field": {
        "titulo": "CS0145 — campo const",
        "explicacion": "const en clase requiere inicializador estático en sitio.",
        "soluciones": ["= valor constante", "static readonly"],
    },
    r"CS0155:.*catch|throw.*System\.Exception": {
        "titulo": "CS0155 — catch o throw inválido",
        "explicacion": "catch de tipo que no hereda de Exception o throw mal formado.",
        "soluciones": ["catch (Exception ex)", "throw; o throw new"],
    },
    r"CS0160:.*previous catch clause already catches": {
        "titulo": "CS0160 — catch inalcanzable",
        "explicacion": "Un catch base está antes que uno más específico.",
        "soluciones": ["Orden: específico primero"],
    },
    r"CS0188:.*before all fields": {
        "titulo": "CS0188 — this antes de campos",
        "explicacion": "En struct, usás this antes de asignar todos los campos.",
        "soluciones": ["Asigná campos en orden", "ctor con : this(...)"],
    },
    r"CS0191:.*readonly field": {
        "titulo": "CS0191 — readonly fuera de ctor",
        "explicacion": "Asignás readonly fuera del constructor o del inicializador.",
        "soluciones": ["Solo en ctor/static ctor", "Quita readonly"],
    },
    r"CS0214:.*pointers and fixed size buffers": {
        "titulo": "CS0214 — punteros unsafe",
        "explicacion": "Operación de puntero fuera de unsafe.",
        "soluciones": ["unsafe { }", "Span<T> en lugar de puntero"],
    },
    r"CS0227:.*unsafe code": {
        "titulo": "CS0227 — unsafe deshabilitado",
        "explicacion": "Proyecto sin AllowUnsafeBlocks.",
        "soluciones": ["<AllowUnsafeBlocks>true</AllowUnsafeBlocks>"],
    },
    r"CS0248:.*void": {
        "titulo": "CS0248 — void en expresión",
        "explicacion": "Usás void como tipo de variable o operando.",
        "soluciones": ["No uses void salvo retorno de método"],
    },
    r"CS0513:.*abstract.*in sealed class": {
        "titulo": "CS0513 — abstract en sealed",
        "explicacion": "Clase sealed no puede tener abstract.",
        "soluciones": ["Quita sealed o abstract"],
    },
    r"CS0515:.*fixed|override.*in fixed": {
        "titulo": "CS0515 — override en método fixed",
        "explicacion": "override ilegal en contexto fixed (raro).",
        "soluciones": ["Revisá firma y fixed statement"],
    },
    r"CS0557:.*duplicate user conversion": {
        "titulo": "CS0557 — conversión duplicada",
        "explicacion": "Dos conversiones implícitas/explícitas ambiguas.",
        "soluciones": ["Una conversión por dirección", "explicit"],
    },
    r"CS0563:.*binary operator.*parameter": {
        "titulo": "CS0563 — operador binario",
        "explicacion": "Operador binario: un parámetro debe ser el tipo contenedor.",
        "soluciones": ["Firma (T, T) o (T, int) con T contenedor"],
    },
    r"CS0571:.*operator.*cannot implicitly": {
        "titulo": "CS0571 — operador acceso",
        "explicacion": "No podés usar . en operador implícito; sintaxis especial.",
        "soluciones": ["implicit operator T(...)"],
    },
    r"CS0591:.*Invalid value for argument": {
        "titulo": "CS0591 — argumento de atributo",
        "explicacion": "Valor inválido en atributo (enum, tipo).",
        "soluciones": ["Valores permitidos del atributo"],
    },
    r"CS0648:.*extern alias": {
        "titulo": "CS0648 — extern alias",
        "explicacion": "Referencia con alias extern mal referenciada.",
        "soluciones": ["extern alias en csproj", ":: global"],
    },
    r"CS0650:.*bad array declarator": {
        "titulo": "CS0650 — declarador de array",
        "explicacion": "Tamaño de array en posición incorrecta (C# vs C).",
        "soluciones": ["int[] no int a[]"],
    },
    r"CS0662:.*out.*Attribute": {
        "titulo": "CS0662 — out y atributo",
        "explicacion": "Incompatibilidad entre out y ciertos atributos en P/Invoke.",
        "soluciones": ["Revisá DllImport y marshalling"],
    },
    r"CS0674:.*struct.*extends System\.MulticastDelegate": {
        "titulo": "CS0674 — struct delegate",
        "explicacion": "struct no puede heredar MulticastDelegate.",
        "soluciones": ["delegate es referencia type"],
    },
    r"CS0683:.*differing param lists": {
        "titulo": "CS0683 — explícito interface",
        "explicacion": "Implementación explícita no coincide con interfaz.",
        "soluciones": ["Firma idéntica a la interfaz"],
    },
    r"CS0708:.*field.*in static class": {
        "titulo": "CS0708 — campo instancia en static",
        "explicacion": "static class no puede tener campos de instancia.",
        "soluciones": ["static readonly", "Quita static de la clase"],
    },
    r"CS0737:.*does not implement": {
        "titulo": "CS0737 — interfaz no implementada",
        "explicacion": "Miembros no públicos no cuentan para interfaz pública.",
        "soluciones": ["public en miembros de interfaz"],
    },
    r"CS0750:.*partial method": {
        "titulo": "CS0750 — partial method",
        "explicacion": "partial method con modificador inválido o sin definición.",
        "soluciones": ["Reglas partial void", "Cuerpo en un partial"],
    },
    r"CS0759:.*partial.*modifiers": {
        "titulo": "CS0759 — partial inconsistente",
        "explicacion": "Dos partes de partial con modificadores distintos.",
        "soluciones": ["Unificá public/private static"],
    },
    r"CS0826:.*implicitly typed array": {
        "titulo": "CS0826 — array implícito",
        "explicacion": "new[] sin tipo común inferible entre elementos.",
        "soluciones": ["Tipo explícito new int[]", "Cast"],
    },
    r"CS0834:.*lambda.*statement body": {
        "titulo": "CS0834 — lambda en árbol",
        "explicacion": "Expression lambda vs statement body en Expression<T>.",
        "soluciones": ["Expresión única", "Statement en Func si aplica"],
    },
    r"CS0854:.*expression tree.*optional argument": {
        "titulo": "CS0854 — argumento opcional en expression tree",
        "explicacion": "Expression tree no puede tener args opcionales en la llamada.",
        "soluciones": ["Pasá todos los args explícitos"],
    },
    r"CS1620:.*ref.*out.*foreach": {
        "titulo": "CS1620 — ref/out en foreach",
        "explicacion": "foreach variable es read-only; no ref/out.",
        "soluciones": ["for con índice", "ToList y mutar"],
    },
    r"CS1631:.*yield return.*catch": {
        "titulo": "CS1631 — yield en catch",
        "explicacion": "yield return no permitido dentro de catch/finally.",
        "soluciones": ["Reestructurá try/catch fuera del iterador"],
    },
    r"CS1643:.*foreach.*not directly": {
        "titulo": "CS1643 — foreach en query",
        "explicacion": "Notación de query con foreach anidado inválido.",
        "soluciones": ["from/select explícito", "Método syntax"],
    },
    r"CS1674:.*using.*must implement IDisposable": {
        "titulo": "CS1674 — using sin IDisposable",
        "explicacion": "using requiere IDisposable.",
        "soluciones": ["Implementá Dispose", "await using IAsyncDisposable"],
    },
    r"CS1685:.*predefined type.*multiple": {
        "titulo": "CS1685 — tipo predefinido duplicado",
        "explicacion": "Conflicto de System.Runtime / mscorlib múltiples.",
        "soluciones": ["Binding redirects", "Unificar paquetes System.Runtime"],
    },
    r"CS1737:.*optional parameters.*after": {
        "titulo": "CS1737 — opcionales al final",
        "explicacion": "Parámetros opcionales deben ir después de los requeridos.",
        "soluciones": ["Reordená parámetros"],
    },
    r"CS1741:.*ref.*out.*default": {
        "titulo": "CS1741 — default en ref/out",
        "explicacion": "ref/out no pueden tener valor default en la misma firma mal formada.",
        "soluciones": ["Firma válida C#"],
    },
    r"CS1763:.*variadic": {
        "titulo": "CS1763 — params",
        "explicacion": "params debe ser último y un solo array.",
        "soluciones": ["params object[] al final"],
    },
    r"CS1988:.*async methods.*ref.*unsafe": {
        "titulo": "CS1988 — async y ref/unsafe",
        "explicacion": "async method no puede tener ref unsafe parameters según reglas.",
        "soluciones": ["Span", "Quita async de esa capa"],
    },
    r"CS4008:.*await.*void": {
        "titulo": "CS4008 — await void",
        "explicacion": "await en expresión void.",
        "soluciones": ["async Task", "No await void returning"],
    },
    r"CS4015:.*async.*Main": {
        "titulo": "CS4015 — async Main",
        "explicacion": "async Main requiere Task/Task<int> retorno.",
        "soluciones": ["static async Task Main()", "top-level async"],
    },
    r"CS4016:.*async.*void": {
        "titulo": "CS4016 — async void",
        "explicacion": "async void solo en event handlers según estilo.",
        "soluciones": ["async Task", "Excepciones se pierden en async void"],
    },
    r"CS8425:.*async.*iterator": {
        "titulo": "CS8425 — async iterator",
        "explicacion": "IAsyncEnumerable mal formado o yield en async stream.",
        "soluciones": ["async IAsyncEnumerable", "await foreach"],
    },
    r"CS8792:.*partial.*method": {
        "titulo": "CS8792 — partial method returning",
        "explicacion": "partial method con return type debe tener definición.",
        "soluciones": ["Ambas partes partial"],
    },
    r"CS8981:.*type name.*only contains lower-cased ascii": {
        "titulo": "CS8981 — nombre tipo en minúsculas",
        "explicacion": "Advertencia/nivel error: tipo `list` vs convención.",
        "soluciones": ["PascalCase", "Suprimí warning si es intencional"],
    },
    r"CS9050:.*file-scoped": {
        "titulo": "CS9050 — file-scoped namespace",
        "explicacion": "Conflicto de namespace file-scoped con declaración interna.",
        "soluciones": ["Un estilo por archivo"],
    },
    r"CS9230:.*ref struct": {
        "titulo": "CS9230 — ref struct",
        "explicacion": "Restricción de ref struct (heap, async, etc.).",
        "soluciones": ["stackalloc", "Span rules"],
    },
    r"CS0171:.*fully assign": {
        "titulo": "CS0171 — struct sin asignar",
        "explicacion": "Constructor no asignó todos los campos del struct antes de salir.",
        "soluciones": ["this : this(...)", "Asigná cada campo", "readonly en propiedades auto"],
    },
    r"CS8410:": {
        "titulo": "CS8410 — readonly / ref struct",
        "explicacion": "Campo readonly, ref struct o regla de inicialización incumplida en el contexto.",
        "soluciones": ["Constructor primario", "init-only donde aplique", "Leé el texto completo del diagnóstico"],
    },
}
