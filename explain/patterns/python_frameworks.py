# Django, Flask/Werkzeug, FastAPI/Starlette, Pydantic, SQLAlchemy, Celery, etc.

ERRORES_PYTHON_FW = {
    r"django\.core\.exceptions\.ImproperlyConfigured": {
        "titulo": "Django — configuración incorrecta",
        "explicacion": "SETTINGS, apps, middleware o variable de entorno no cumple lo que Django espera.",
        "soluciones": ["Revisá INSTALLED_APPS y MIDDLEWARE", "DEBUG/SECRET_KEY/ALLOWED_HOSTS", "django.setup() antes de modelos sueltos"],
    },
    r"django\.core\.exceptions\.ValidationError": {
        "titulo": "Django — validación de modelo/formulario",
        "explicacion": "clean(), full_clean() o Form no aceptaron los datos (campos, unique, custom validators).",
        "soluciones": ["form.errors / e.error_dict", "Revisá Model.clean y constraints"],
    },
    r"django\.core\.exceptions\.PermissionDenied": {
        "titulo": "Django — permiso denegado",
        "explicacion": "raise PermissionDenied o decorador/mixin de auth bloqueó la vista.",
        "soluciones": ["@permission_required", "UserPassesTestMixin", "403 vs login"],
    },
    r"django\.core\.exceptions\.DisallowedHost": {
        "titulo": "Django — host no permitido",
        "explicacion": "El Host de la petición no está en ALLOWED_HOSTS.",
        "soluciones": ["Añadí el dominio o * solo en dev", "Proxy y USE_X_FORWARDED_HOST"],
    },
    r"django\.urls\.exceptions\.NoReverseMatch": {
        "titulo": "Django — reverse de URL falló",
        "explicacion": "reverse(), {% url %} o redirect no encuentran nombre de ruta o faltan kwargs.",
        "soluciones": ["Nombre en path() coincide con el usado", "kwargs obligatorios", "namespace include()"],
    },
    r"django\.core\.exceptions\.FieldError": {
        "titulo": "Django — FieldError",
        "explicacion": "Nombre de campo inválido en QuerySet, values() o Meta.",
        "soluciones": ["Revisá select_related/prefetch y nombres del modelo", "Migraciones aplicadas"],
    },
    r"\.DoesNotExist:\s*$|DoesNotExist:\s|matching query does not exist": {
        "titulo": "Django — objeto no existe",
        "explicacion": "get() o acceso one-to-one sin filas (Model.DoesNotExist).",
        "soluciones": ["get_object_or_404", "filter().first()", "try/except DoesNotExist"],
    },
    r"MultipleObjectsReturned": {
        "titulo": "Django — varias filas con get()",
        "explicacion": "get() encontró más de un registro; la consulta no es única.",
        "soluciones": ["filter()", "distinct()", "restricción unique en BD"],
    },
    r"django\.db\.utils\.IntegrityError": {
        "titulo": "Django — violación de integridad SQL",
        "explicacion": "UNIQUE, FK o CHECK falló al guardar (ORM o SQL crudo).",
        "soluciones": ["Datos duplicados", "on_delete", "transacción atómica"],
    },
    r"django\.db\.utils\.(OperationalError|ProgrammingError)": {
        "titulo": "Django — error SQL / conexión",
        "explicacion": "BD caída, SQL inválido, tabla inexistente o migración pendiente.",
        "soluciones": ["migrate", "Credenciales DATABASES", "Revisá el SQL en el traceback"],
    },
    r"django\.db\.migrations\.exceptions\.(InconsistentMigrationHistory|CircularDependency)": {
        "titulo": "Django — migraciones inconsistentes",
        "explicacion": "Historial de migraciones no encaja entre ramas o entornos.",
        "soluciones": ["merge migrations", "squash con cuidado", "backup antes de --fake"],
    },
    r"rest_framework\.exceptions\.|rest_framework\.serializers\.ValidationError": {
        "titulo": "Django REST Framework",
        "explicacion": "DRF: serializer, parser, auth o permisos rechazaron la petición.",
        "soluciones": ["serializer.errors", "IsAuthenticated", "raise_exception=True en validación"],
    },
    r"werkzeug\.routing\.exceptions\.(NotFound|BuildError|MethodNotAllowed)": {
        "titulo": "Werkzeug / Flask — routing",
        "explicacion": "Ruta no registrada, url_for sin endpoint o método HTTP no permitido.",
        "soluciones": ["Registrá la ruta y el nombre", "Argumentos de url_for", "methods= en route"],
    },
    r"werkzeug\.exceptions\.(BadRequest|Unauthorized|Forbidden|InternalServerError)": {
        "titulo": "Werkzeug — excepción HTTP",
        "explicacion": "Flask/Werkzeug mapeó error a código HTTP concreto.",
        "soluciones": ["Revisá abort(code)", "Datos del cliente o auth"],
    },
    r"fastapi\.exceptions\.(HTTPException|RequestValidationError|WebSocketRequestValidationError)": {
        "titulo": "FastAPI — HTTP o validación",
        "explicacion": "raise HTTPException o el body/query no pasó el modelo Pydantic.",
        "soluciones": ["Esquema del modelo", "response_model", "422 en docs /openapi"],
    },
    r"starlette\.exceptions\.|starlette\.routing\.": {
        "titulo": "Starlette (FastAPI)",
        "explicacion": "Capa ASGI: ruta, WebSocket o middleware falló.",
        "soluciones": ["Orden de middleware", "Mount vs include_router"],
    },
    r"pydantic_core\._pydantic_core\.ValidationError|pydantic\.error_wrappers\.ValidationError": {
        "titulo": "Pydantic — validación",
        "explicacion": "Datos no cumplen el modelo (v1/v2 muestran errores por campo).",
        "soluciones": ["Leé error.errors()", "Tipos y Optional", "model_config extra"],
    },
    r"pydantic\.errors\.(PydanticUserError|ConfigError)": {
        "titulo": "Pydantic — configuración del modelo",
        "explicacion": "Modelo mal definido o opción incompatible con la versión.",
        "soluciones": ["Migración v1→v2 (model_config)", "Docs de tu versión de Pydantic"],
    },
    r"sqlalchemy\.exc\.IntegrityError": {
        "titulo": "SQLAlchemy — integridad",
        "explicacion": "Constraint de BD al hacer flush/commit.",
        "soluciones": ["Unique/ FK", "session.rollback()", "Datos antes de commit"],
    },
    r"sqlalchemy\.exc\.(OperationalError|ProgrammingError|DatabaseError)": {
        "titulo": "SQLAlchemy — SQL o conexión",
        "explicacion": "Driver rechazó la query o perdió conexión.",
        "soluciones": ["URL de engine", "pool_pre_ping", "SQL generado en echo=True"],
    },
    r"sqlalchemy\.exc\.(NoReferencedTableError|InvalidRequestError|ArgumentError)": {
        "titulo": "SQLAlchemy — modelo / mapeo",
        "explicacion": "ForeignKey a tabla no mapeada, relación mal declarada o API mal usada.",
        "soluciones": ["Base.metadata.create_all orden", "relationship() y back_populates"],
    },
    r"sqlalchemy\.orm\.exc\.(DetachedInstanceError|ObjectDeletedError|StaleDataError)": {
        "titulo": "SQLAlchemy ORM — sesión",
        "explicacion": "Objeto usado fuera de sesión, borrado o versión optimista falló.",
        "soluciones": ["session.merge", "expire_on_commit", "refresh antes de leer"],
    },
    r"alembic\.util\.exc\.CommandError": {
        "titulo": "Alembic",
        "explicacion": "Comando revision/upgrade/downgrade falló (head múltiple, branch, etc.).",
        "soluciones": ["alembic heads", "merge", "Revisá env.py y script_location"],
    },
    r"celery\.exceptions\.|billiard\.exceptions\.": {
        "titulo": "Celery / billiard",
        "explicacion": "Worker, broker o pool de procesos reportó error.",
        "soluciones": ["Broker URL y redis/rabbit arriba", "result_backend", "task_always_eager en tests"],
    },
    r"kombu\.exceptions\.|amqp\.exceptions\.": {
        "titulo": "Celery — broker (kombu/amqp)",
        "explicacion": "Cola de mensajes rechazó conexión o formato.",
        "soluciones": ["Credenciales y vhost", "Firewall", "Versión del broker"],
    },
    r"redis\.exceptions\.(ConnectionError|TimeoutError|BusyLoadingError)": {
        "titulo": "Redis (cliente Python)",
        "explicacion": "No hay conexión, timeout o instancia cargando dataset.",
        "soluciones": ["redis-cli ping", "maxclients", "retry on timeout"],
    },
    r"httpx\.(ConnectError|ReadTimeout|HTTPStatusError|LocalProtocolError)": {
        "titulo": "HTTPX",
        "explicacion": "Cliente async/sync falló al conectar, leer o código HTTP no esperado.",
        "soluciones": ["URL y TLS", "raise_for_status()", "timeouts explícitos"],
    },
    r"requests\.exceptions\.(ConnectionError|HTTPError|Timeout|SSLError|ChunkedEncodingError)": {
        "titulo": "Requests",
        "explicacion": "Red, TLS, timeout o cuerpo de respuesta corrupto.",
        "soluciones": ["verify=False solo en dev", "stream=True y lectura completa", "reintentos"],
    },
    r"pymongo\.errors\.(DuplicateKeyError|ServerSelectionTimeoutError|ConfigurationError)": {
        "titulo": "PyMongo / MongoDB",
        "explicacion": "Índice único, no hay réplica disponible o URI inválida.",
        "soluciones": ["connection string", "replicaSet", "índices y datos"],
    },
    r"pytest\.fixture|fixture.*not found|PytestDeprecationWarning.*fixture": {
        "titulo": "pytest — fixtures",
        "explicacion": "Nombre de fixture inexistente, scope incorrecto o plugin no cargado.",
        "soluciones": ["conftest.py en path", "pytest_plugins", "nombre del argumento = nombre fixture"],
    },
    r"_pytest\.(config|runner)\.|ERROR at setup|ERROR at teardown": {
        "titulo": "pytest — setup/teardown",
        "explicacion": "Fallo en fixture autouse, scope session o hook.",
        "soluciones": ["Traceback del error real arriba", "yield fixture y cleanup"],
    },
    r"jinja2\.(exceptions\.|TemplateError|TemplateSyntaxError|UndefinedError)": {
        "titulo": "Jinja2 — plantilla",
        "explicacion": "Sintaxis de template, variable indefinida o error al renderizar.",
        "soluciones": ["Revisá {{ }} y bloques", "Pasa variables al Environment", "strict_undefined"],
    },
    r"gunicorn\.errors\.|WORKER TIMEOUT|Worker failed to boot": {
        "titulo": "Gunicorn",
        "explicacion": "Worker murió, timeout o fallo al arrancar la app WSGI.",
        "soluciones": ["Logs --log-level debug", "timeout y workers", "Import errors en wsgi.py"],
    },
    r"uvicorn\.errors\.|ERROR:.*\[uvicorn\]|Failed to start uvicorn": {
        "titulo": "Uvicorn — error de arranque o servidor",
        "explicacion": "Fallo al cargar ASGI, puerto ocupado o excepción en el worker.",
        "soluciones": ["Otro --port", "Traceback de import de app:factory", "Logs con --log-level debug"],
    },
}
