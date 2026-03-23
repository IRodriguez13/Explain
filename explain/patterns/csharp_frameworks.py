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
    # --- ASP.NET Core pipeline, hosting, HTTP ---
    r"Microsoft\.AspNetCore\.Http\.BadHttpRequestException": {
        "titulo": "BadHttpRequestException",
        "explicacion": "Kestrel/HTTP detectó cuerpo truncado, Content-Length inválido, línea de request ilegal o límite de tamaño.",
        "soluciones": ["KestrelLimits", "Request body buffering", "Cliente envía headers y body coherentes"],
    },
    r"Microsoft\.AspNetCore\.Connections\.AddressInUseException": {
        "titulo": "Kestrel — puerto en uso",
        "explicacion": "El puerto configurado (URLs) ya está ocupado por otro proceso.",
        "soluciones": ["Otro --urls", "lsof/kill del proceso previo", "UseUrls en launchSettings"],
    },
    r"Microsoft\.AspNetCore\.Server\.Kestrel\.|BadHttpRequestException.*Kestrel": {
        "titulo": "Kestrel — error de servidor",
        "explicacion": "Límites de conexión, TLS mal configurado, o error interno del transporte.",
        "soluciones": ["ConfigureKestrel", "Certificados HTTPS dev", "ListenOptions"],
    },
    r"Microsoft\.Extensions\.Hosting\.HostAbortedException|BackgroundServiceExceptionBehavior": {
        "titulo": "Host / BackgroundService",
        "explicacion": "El host se detuvo o un IHostedService lanzó excepción según la política configurada.",
        "soluciones": ["StopHost timeout", "Try/catch en ExecuteAsync", "ConfigureServices behavior"],
    },
    r"Microsoft\.AspNetCore\.Routing\.Matching\.AmbiguousMatchException": {
        "titulo": "AmbiguousMatchException (routing)",
        "explicacion": "Dos endpoints minimal o MVC coinciden sin desempate claro.",
        "soluciones": ["Order en minimal", "HTTP method", "Route constraints más específicos"],
    },
    r"Microsoft\.AspNetCore\.Mvc\.Infrastructure\.AmbiguousActionException|AmbiguousMatchException.*action": {
        "titulo": "Acción MVC ambigua",
        "explicacion": "Varias acciones del controller encajan con la misma ruta y verbo.",
        "soluciones": ["Route templates distintos", "[HttpGet(\"x\")] explícito", "Area/Order"],
    },
    r"InvalidOperationException.*endpoint|No endpoint matches|The request matched multiple endpoints": {
        "titulo": "Endpoints — ninguno o varios",
        "explicacion": "El pipeline de endpoint routing no encontró match o encontró más de uno.",
        "soluciones": ["MapGet/MapControllers orden", "FallbackPolicy", "UseRouting/UseEndpoints orden"],
    },
    r"Microsoft\.AspNetCore\.Authentication\.AuthenticationFailureException": {
        "titulo": "AuthenticationFailureException",
        "explicacion": "Handler de autenticación (Cookie, JwtBearer, OAuth) rechazó la identidad.",
        "soluciones": ["Logs del handler", "Esquema correcto", "Challenge vs Forbid"],
    },
    r"Microsoft\.AspNetCore\.Authorization\.(AuthorizationMiddlewareResultHandler|AuthorizationHandlerContext)|ForbidResult|ChallengeResult": {
        "titulo": "Autorización — Forbid / Challenge",
        "explicacion": "Policy, roles o claims no cumplidos; el middleware emitió Forbid o Challenge.",
        "soluciones": ["[Authorize(Policy=)]", "IAuthorizationHandler", "FallbackPolicy"],
    },
    r"AntiforgeryValidationException|AntiforgeryToken|The antiforgery token": {
        "titulo": "Antiforgery / CSRF",
        "explicacion": "Token ausente, cookie no enviada, header __RequestVerificationToken o form field incorrecto.",
        "soluciones": ["AddAntiforgery", "ValidateAntiForgeryToken", "SameSite=None; Secure en HTTPS"],
    },
    r"Microsoft\.AspNetCore\.Http\.Features\.BadHttpRequestFeature|Request body too large": {
        "titulo": "Request demasiado grande",
        "explicacion": "Multipart o body supera MultipartBodyLengthLimit / Kestrel max request.",
        "soluciones": ["FormOptions", "RequestSizeLimit attribute", "streaming para archivos grandes"],
    },
    r"InvalidOperationException.*form content type|Unexpected end of Stream|MultipartReader": {
        "titulo": "Multipart / form parsing",
        "explicacion": "Boundary incorrecto, stream cortado o Content-Type no es multipart/form-data válido.",
        "soluciones": ["Cliente envía boundary correcto", "No leer body dos veces sin EnableBuffering"],
    },
    # --- FastEndpoints, Carter, minimal APIs ---
    r"FastEndpoints\.[A-Za-z_]+Exception|FastEndpoints\.ValidatorExecutor": {
        "titulo": "FastEndpoints",
        "explicacion": "Validación del endpoint, registro de validator, o ejecución del handler falló.",
        "soluciones": ["AbstractValidator<TRequest>", "SendErrorsAsync", "Scoped validators en DI"],
    },
    r"FluentValidation\.ValidationException|FluentValidation\.AsyncValidatorInvokedSynchronouslyException": {
        "titulo": "FluentValidation",
        "explicacion": "Reglas ValidateAsync invocadas de forma síncrona, o modelo no pasó RuleFor.",
        "soluciones": ["ValidateAsync en pipeline", "AbstractValidator con reglas claras", "Include rules"],
    },
    r"Carter\.|ICarterModule": {
        "titulo": "Carter (minimal modules)",
        "explicacion": "Módulo de rutas Carter no registrado, conflicto de ruta o dependencia del módulo falló.",
        "soluciones": ["AddCarter()", "MapCarter()", "Revisá AddEndpoints de cada module"],
    },
    r"MediatR\.|Handler was not found for request|No service for type.*IRequestHandler": {
        "titulo": "MediatR",
        "explicacion": "No hay IRequestHandler registrado para el comando/query, o el assembly no se escaneó.",
        "soluciones": ["AddMediatR(cfg => cfg.RegisterServicesFromAssembly)", "Handler en DI", "Tipo genérico del request"],
    },
    r"Polly\.(CircuitBreaker\.)?BrokenCircuitException|Polly\.Timeout\.TimeoutRejectedException|Polly\.RateLimit\.RateLimitRejectedException": {
        "titulo": "Polly — resiliencia",
        "explicacion": "Circuit abierto, timeout de la política, o rate limit excedido.",
        "soluciones": ["Handle/retry policy", "Duración de break", "Bulkhead si hay saturación"],
    },
    r"Refit\.ApiException|Refit\.ValidationApiException": {
        "titulo": "Refit (HTTP client)",
        "explicacion": "La API remota devolvió error HTTP o el contenido no deserializó al tipo esperado.",
        "soluciones": ["response.Content", "ApiResponse<T>", "Serialización Json"],
    },
    r"Grpc\.Core\.RpcException|Grpc\.Net\.Client\.Internal\.GrpcCall|StatusCode\.(Unavailable|DeadlineExceeded|Unauthenticated)": {
        "titulo": "gRPC (.NET)",
        "explicacion": "Canal gRPC caído, deadline, TLS/mTLS o metadata de auth incorrecta.",
        "soluciones": ["SocketsHttpHandler", "Credenciales CallCredentials", "Health checks del servicio"],
    },
    r"Yarp\.ReverseProxy\.Forwarder\.|IForwarderErrorFeature|502 Bad Gateway.*YARP": {
        "titulo": "YARP — reverse proxy",
        "explicacion": "El destino no respondió, certificado inválido en cluster, o transform de request falló.",
        "soluciones": ["Destination health", "HttpClient config en cluster", "Activity logs"],
    },
    r"Microsoft\.AspNetCore\.RateLimiting\.|RateLimiterOptions|StatusCode:\s*429": {
        "titulo": "Rate limiting (ASP.NET 7+)",
        "explicacion": "El cliente superó FixedWindow/SlidingWindow/TokenBucket configurado.",
        "soluciones": ["AddRateLimiter + policy", "Retry-After header", "PartitionByUserOrIp"],
    },
    r"Microsoft\.AspNetCore\.SignalR\.HubException|HubException|Cannot send message.*connection": {
        "titulo": "SignalR",
        "explicacion": "Cliente desconectado, método hub lanzó, o serialización del mensaje falló.",
        "soluciones": ["Groups.AddToGroupAsync", "JsonProtocol vs MessagePack", "ConnectionId válido"],
    },
    r"Microsoft\.AspNetCore\.Components\.|JSException|RemoteRendererException|blazor": {
        "titulo": "Blazor (Server/Web)",
        "explicacion": "Error en render, circuito SignalR roto, o interop JS↔.NET falló.",
        "soluciones": ["DetailedErrors en dev", "JSInvokable y serialización", "Reconnect UI"],
    },
    r"Microsoft\.AspNetCore\.Mvc\.Razor\.|Razor\.RuntimeCompilation|ViewEngineResult": {
        "titulo": "Razor / MVC views",
        "explicacion": "Vista no encontrada, error de compilación en .cshtml, o layout ausente.",
        "soluciones": ["AddControllersWithViews + Razor runtime compile en dev", "Ruta ReturnView"],
    },
    r"Microsoft\.AspNetCore\.Diagnostics\.DeveloperExceptionPage|DeveloperExceptionPageMiddleware": {
        "titulo": "Developer exception page",
        "explicacion": "Excepción no capturada en pipeline con entorno Development (página amarilla).",
        "soluciones": ["UseExceptionHandler en Production", "Leé el stack del middleware"],
    },
    r"Microsoft\.AspNetCore\.Http\.HttpResults\.|IResult": {
        "titulo": "Minimal APIs — IResult",
        "explicacion": "Result factory (Results.Json, File, Problem) recibió argumentos inválidos o stream cerrado.",
        "soluciones": ["TypedResults", "StatusCode explícito", "OpenApi metadata"],
    },
    # --- Options, HTTP client factory, health ---
    r"Microsoft\.Extensions\.Options\.OptionsValidationException|ValidateDataAnnotations|ValidateOnStart": {
        "titulo": "IOptions — validación",
        "explicacion": "IValidateOptions<T> o DataAnnotations falló al arrancar o al primer resolve.",
        "soluciones": ["AddOptions<T>().ValidateOnStart()", "Mensajes de validación en logs"],
    },
    r"System\.Net\.Http\.HttpRequestException|TaskCanceledException.*HttpClient": {
        "titulo": "HttpClient — red",
        "explicacion": "DNS, conexión rechazada, TLS handshake o cancelación por timeout del client.",
        "soluciones": ["IHttpClientFactory + named client", "Polly handler", "Timeout global vs per-request"],
    },
    r"Microsoft\.Extensions\.Diagnostics\.HealthChecks\.|Health check.*with status Unhealthy": {
        "titulo": "Health checks",
        "explicacion": "Un check registrado devolvió Unhealthy o el tag de readiness falló.",
        "soluciones": ["MapHealthChecks", "AddCheck con lógica estable", "Kubernetes probes"],
    },
    # --- Identity, tokens, OpenIddict, Duende ---
    r"OpenIddict\.[A-Za-z_.]+Exception|OpenIddictCoreBuilder": {
        "titulo": "OpenIddict",
        "explicacion": "Flujo OAuth/OIDC: cliente, scope o token no válido según el servidor.",
        "soluciones": ["OpenIddictApplicationManager", "Permisos endpoint", "Logs de validación"],
    },
    r"Duende\.IdentityServer\.|IdentityServer4\.|invalid_scope|invalid_client": {
        "titulo": "Duende / IdentityServer",
        "explicacion": "STS rechazó cliente, redirect URI, grant o scope.",
        "soluciones": ["Client config en DB/config", "Grant types habilitados", "Secrets del cliente"],
    },
    r"Microsoft\.AspNetCore\.Identity\.|UserManager|SignInManager|IdentityError": {
        "titulo": "ASP.NET Identity",
        "explicacion": "Creación de usuario, login, lockout o validación de password falló.",
        "soluciones": ["IdentityResult.Errors", "PasswordOptions", "TwoFactor"],
    },
    # --- Testing, WebApplicationFactory ---
    r"WebApplicationFactory|Microsoft\.AspNetCore\.Mvc\.Testing\.|TestServer": {
        "titulo": "WebApplicationFactory / TestServer",
        "explicacion": "Host de integración no levantó, content root incorrecto, o servicio real no sustituido en tests.",
        "soluciones": ["ConfigureWebHost", "UseEnvironment(\"Development\")", "Replace DI con mocks"],
    },
    # --- EF / providers adicionales ---
    r"Microsoft\.EntityFrameworkCore\.DbUpdateException.*inner|RetryLimitExceededException": {
        "titulo": "EF Core — reintentos",
        "explicacion": "ExecutionStrategy agotó reintentos ante error transitorio de BD.",
        "soluciones": ["EnableRetryOnFailure", "Transacciones compatibles con retry", "InnerException SQL"],
    },
    r"Microsoft\.EntityFrameworkCore\.Infrastructure\.|RelationalEventId\.|SqliteException": {
        "titulo": "EF Core — infra / SQLite",
        "explicacion": "Migración, conexión SQLite bloqueada, o SQL generado inválido para el provider.",
        "soluciones": ["UseSqlite y WAL", "BusyTimeout", "Migrations aplicadas"],
    },
    r"MySqlConnector\.MySqlException|MySql\.Data\.MySqlClient\.MySqlException": {
        "titulo": "MySQL (Connector/NET)",
        "explicacion": "Error del servidor MySQL (deadlock, syntax, connection lost).",
        "soluciones": ["SqlState / Error number", "Connection string y pooling", "Retry en transitorios"],
    },
    r"Microsoft\.Data\.Sqlite\.SqliteException": {
        "titulo": "Microsoft.Data.Sqlite",
        "explicacion": "SQLite: locked, constraint, o archivo de BD inaccesible.",
        "soluciones": ["Cache=Shared", "BusyTimeout", "Una escritura a la vez"],
    },
    r"Oracle\.ManagedDataAccess|OracleException": {
        "titulo": "Oracle (managed driver)",
        "explicacion": "Error ORA-xxxxx del servidor Oracle.",
        "soluciones": ["Número ORA", "TNS y wallet si Autonomous"],
    },
    # --- Messaging, jobs ---
    r"MassTransit\.(RequestFaultException|RequestTimeoutException)|RabbitMQ\.Client\.Exceptions": {
        "titulo": "MassTransit / RabbitMQ",
        "explicacion": "Mensaje fault, timeout de request/response, o conexión AMQP rota.",
        "soluciones": ["IBusControl reconnect", "ReceiveEndpoint", "Dead-letter y retry policy"],
    },
    r"Hangfire\.(Common|BackgroundJob|Server)\.|JobAbortedException|BackgroundJobClientException": {
        "titulo": "Hangfire",
        "explicacion": "Cola SQL/Redis falló, job lanzó excepción recurrente, o servidor no procesa.",
        "soluciones": ["Dashboard", "UseSqlServerStorage", "RetryAttribute y filtros"],
    },
    r"Quartz\.(JobExecutionException|SchedulerException)": {
        "titulo": "Quartz.NET",
        "explicacion": "Job lanzó, scheduler pausado, o trigger mal configurado.",
        "soluciones": ["DisallowConcurrentExecution", "MisfireInstruction", "Cron válido"],
    },
    # --- Logging, observabilidad ---
    r"Serilog\.Core\.|SelfLog\.|LoggerConfiguration": {
        "titulo": "Serilog",
        "explicacion": "Sink falló (archivo, Seq, Elasticsearch) o configuración de logger inválida.",
        "soluciones": ["SelfLog.Enable", "WriteTo condicional", "RenderedMessage vs structured"],
    },
    r"OpenTelemetry\.|ActivitySource|MeterProvider": {
        "titulo": "OpenTelemetry .NET",
        "explicacion": "Exporter no pudo enviar spans/metrics o SDK mal inicializado.",
        "soluciones": ["AddOpenTelemetry", "OTEL_EXPORTER_OTLP_ENDPOINT", "Sampling"],
    },
    # --- Otras libs frecuentes en APIs ---
    r"Humanizer\.|PluralizationService": {
        "titulo": "Humanizer",
        "explicacion": "Cultura o pluralización no disponible para el recurso (menos frecuente como crash).",
        "soluciones": ["CurrentUICulture", "Fallback culture"],
    },
    r"MimeKit\.|MailKit\.(Net\.|Security\.)": {
        "titulo": "MailKit / MimeKit",
        "explicacion": "SMTP/IMAP: auth TLS, certificado, o mensaje MIME inválido.",
        "soluciones": ["CheckCertificateRevocation", "SecureSocketOptions", "UTF-8 en headers"],
    },
    r"SixLabors\.ImageSharp\.|ImageProcessingException": {
        "titulo": "ImageSharp",
        "explicacion": "Formato de imagen corrupto, dimensiones excesivas o decoder no disponible.",
        "soluciones": ["Identify antes de decode", "MaxDimensions", "FormatDetector"],
    },
    r"AWSSDK\.|Amazon\.(S3|DynamoDB|Runtime)\.": {
        "titulo": "AWS SDK for .NET",
        "explicacion": "Credenciales, región, throttling o error de servicio AWS.",
        "soluciones": ["Exception.Message y ErrorCode", "IAM role en ECS/Lambda", "Retry mode adaptive"],
    },
    r"Azure\.(Core|Identity|Storage)\.|RequestFailedException": {
        "titulo": "Azure SDK",
        "explicacion": "RequestFailedException con status de ARM/Storage/KeyVault.",
        "soluciones": ["DefaultAzureCredential chain", "Status y ErrorCode", "Endpoint correcto"],
    },
    r"Stripe\.StripeException|Stripe\.Error": {
        "titulo": "Stripe.NET",
        "explicacion": "API de pagos rechazó tarjeta, clave secreta inválida o idempotency.",
        "soluciones": ["StripeError type/code", "Webhook signature", "Test vs live keys"],
    },
    r"KubernetesClient\.|k8s\.(Autorest\.)?KubernetesException": {
        "titulo": "Kubernetes client (.NET)",
        "explicacion": "API server rechazó recurso, RBAC, o kubeconfig inválido.",
        "soluciones": ["kubectl auth", "InnerException HTTP status", "Namespace y CRD"],
    },
    r"Docker\.DotNet\.DockerApiException": {
        "titulo": "Docker.DotNet",
        "explicacion": "Daemon Docker rechazó operación (socket, imagen inexistente).",
        "soluciones": ["DOCKER_HOST", "API version mismatch", "Permisos del socket"],
    },
    r"NSwag\.|NJsonSchema\.JsonSchemaException": {
        "titulo": "NSwag / NJsonSchema",
        "explicacion": "Generación de cliente o OpenAPI falló por schema recursivo o tipo no soportado.",
        "soluciones": ["SchemaProcessors", "Excluir tipos problemáticos", "Referencia $ref"],
    },
    r"Swashbuckle\.AspNetCore\.SwaggerGen\.SwaggerGeneratorException": {
        "titulo": "Swashbuckle — SwaggerGenerator",
        "explicacion": "Conflicto de OperationId, mismo nombre de schema, o IActionResult ambiguo.",
        "soluciones": ["CustomSchemaIds", "ProducesResponseType", "MapType"],
    },
    r"Microsoft\.AspNetCore\.OpenApi\.|OpenApiOperationTransformer": {
        "titulo": "OpenAPI nativo (ASP.NET)",
        "explicacion": "Transformación de documento OpenAPI falló o tipo no es serializable en schema.",
        "soluciones": ["AddOpenApi", "SchemaTransformers", "WithOpenApi en endpoints"],
    },
    r"ProblemDetails|IProblemDetailsService|ValidationProblemDetails": {
        "titulo": "Problem Details (RFC 7807)",
        "explicacion": "API devolvió 4xx/5xx con cuerpo problem+json; el cliente o middleware lo interpreta.",
        "soluciones": ["AddProblemDetails", "Results.Problem", "Title/Detail/Extensions coherentes"],
    },
    r"Wolverine\.|JasperFx": {
        "titulo": "Wolverine (mensajería)",
        "explicacion": "Handler, transport o serialización de mensaje falló en el bus ligero.",
        "soluciones": ["UseWolverine cfg", "Durability mode", "Dead letter storage"],
    },
    r"Rebus\.|Rebus\.Exceptions": {
        "titulo": "Rebus",
        "explicacion": "Transport o handler de mensajes falló; segunda cola o timeout.",
        "soluciones": ["Configure.With", "Error queue", "Idempotent handlers"],
    },
    r"MediatR\.|IRequestHandler": {
        "titulo": "MediatR",
        "explicacion": "Handler no registrado, request sin handler, o excepción dentro del pipeline.",
        "soluciones": ["AddMediatR + assembly scan", "IRequestHandler<TReq,TRes> correcto", "Behaviors y excepciones"],
    },
    r"MassTransit\.|RabbitMqConnectionException|ConsumeContext": {
        "titulo": "MassTransit",
        "explicacion": "Broker, serialización o consumidor rechazó el mensaje; reconexión o poison message.",
        "soluciones": ["URI RabbitMQ/Azure SB", "Retry policy", "Dead-letter y logs de consumidor"],
    },
}
