# Entity Framework Core, ASP.NET Core DI, xUnit, NUnit, JSON.NET, AutoMapper, etc.

ERRORES_CSHARP_FW = {
    r"Microsoft\.EntityFrameworkCore\.DbUpdateException": {
        "titulo": "EF Core — DbUpdateException",
        "explicacion": "SaveChanges falló por restricción de BD, concurrencia o datos inválidos.",
        "soluciones": ["InnerException SQL", "Fluent API required", "transacciones"],
    },
    r"DbUpdateConcurrencyException": {
        "titulo": "EF Core — concurrencia",
        "explicacion": "Nadie filas afectadas: otro proceso cambió el mismo registro (token de concurrencia).",
        "soluciones": ["RowVersion/Timestamp", "Reload y reintentar", "Resolución de conflicto"],
    },
    r"InvalidOperationException.*(DbContext|DbSet|OnModelCreating|cannot be used)": {
        "titulo": "EF Core — uso de DbContext",
        "explicacion": "Contexto disposed, dos contextos en una consulta, o modelo mal configurado.",
        "soluciones": ["await using / using scope", "No mezclar contextos en una query", "Migraciones al día"],
    },
    r"SqlException|Microsoft\.Data\.SqlClient\.SqlException": {
        "titulo": "SQL Server (SqlClient)",
        "explicacion": "Error devuelto por el motor SQL (sintaxis, login, timeout, deadlocks).",
        "soluciones": ["Número de error SQL en mensaje", "Cadena de conexión", "Índices y locks"],
    },
    r"Npgsql\.|PostgresException": {
        "titulo": "PostgreSQL (Npgsql)",
        "explicacion": "Error del servidor Postgres vía provider .NET.",
        "soluciones": ["SqlState en excepción", "Connection string y SSL"],
    },
    r"Some services are not able to be constructed|Unable to resolve service for type": {
        "titulo": "ASP.NET Core — inyección de dependencias",
        "explicacion": "El contenedor no puede crear un servicio: falta AddSingleton/Scoped/Transient o dependencia circular.",
        "soluciones": ["Registrá la interfaz en Program.cs", "Revisá ciclos A→B→A", "TryAdd* si aplica"],
    },
    r"System\.AggregateException.*One or more errors occurred": {
        "titulo": "AggregateException (async/Task)",
        "explicacion": "Varias tareas fallaron; la causa real está en InnerExceptions.",
        "soluciones": ["Flatten().InnerException", "await cada Task", "WhenAll con try por tarea"],
    },
    r"Xunit\.Sdk\.|Xunit\.Runner": {
        "titulo": "xUnit",
        "explicacion": "Test falló o el runner no cargó ensamblado/clase.",
        "soluciones": ["Mensaje de assert en salida", "Fact/Theory y datos", "TargetFramework compatible"],
    },
    r"NUnit\.Framework\.(AssertionException|IgnoreException)|NUnit\.Engine\.NUnitEngineException": {
        "titulo": "NUnit",
        "explicacion": "Assert falló o motor de tests reportó error de carga.",
        "soluciones": ["Expected vs Actual", "TestCaseSource", "adapter en .csproj"],
    },
    r"Newtonsoft\.Json\.(JsonSerializationException|JsonReaderException|JsonWriterException)": {
        "titulo": "Json.NET (Newtonsoft)",
        "explicacion": "JSON no coincide con el modelo, propiedad desconocida o texto mal formado.",
        "soluciones": ["JsonProperty names", "MissingMemberHandling", "Formatting del payload"],
    },
    r"System\.Text\.Json\.(JsonException|JsonSerializerException)": {
        "titulo": "System.Text.Json",
        "explicacion": "Serialización/deserialización falló (nombre de propiedad, número, UTF-8).",
        "soluciones": ["JsonNamingPolicy", "JsonPropertyName", "ReferenceHandler si ciclos"],
    },
    r"AutoMapper\.AutoMapperMappingException|AutoMapperConfigurationException": {
        "titulo": "AutoMapper",
        "explicacion": "No hay mapa entre tipos o configuración inválida al arrancar.",
        "soluciones": ["CreateMap<Src,Dst>", "ForMember", "AssertConfigurationIsValid en tests"],
    },
    r"Swashbuckle|Swashbuckle\.AspNetCore|NSwag": {
        "titulo": "OpenAPI / Swagger (Swashbuckle, NSwag)",
        "explicacion": "Generación de swagger.json falló (tipos anónimos, conflictos de ruta).",
        "soluciones": ["SchemaId personalizado", "ApiExplorer", "versiones duplicadas de tipos"],
    },
    r"Microsoft\.AspNetCore\.(Routing|Mvc).*ambiguous|AmbiguousMatchException": {
        "titulo": "ASP.NET Core — rutas ambiguas",
        "explicacion": "Dos endpoints coinciden con la misma petición.",
        "soluciones": ["Order, HTTP method", "Route templates más específicos", "Minimal APIs vs controllers"],
    },
    r"AntiforgeryValidationException|Antiforgery.*token": {
        "titulo": "ASP.NET Core — antiforgery",
        "explicacion": "Token CSRF ausente, expirado o cookie/header no coinciden.",
        "soluciones": ["@Html.AntiForgeryToken", "ValidateAntiForgeryToken", "SameSite cookies"],
    },
    r"Microsoft\.IdentityModel|JwtSecurityToken|IDX\d+": {
        "titulo": "JWT / IdentityModel (Auth)",
        "explicacion": "Token inválido, firma incorrecta, audiencia/issuer o reloj desfasado.",
        "soluciones": ["Authority y MetadataAddress", "ValidateLifetime", "Clave de firma"],
    },
    r"StackExchange\.Redis\.RedisConnectionException|RedisTimeoutException": {
        "titulo": "StackExchange.Redis",
        "explicacion": "No conecta al servidor Redis o comando expiró.",
        "soluciones": ["ConnectionMultiplexer", "abortConnect=false en arranque", "timeouts y thread pool"],
    },
}
