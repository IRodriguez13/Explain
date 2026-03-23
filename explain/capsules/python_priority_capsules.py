# Fichas --man adicionales para Python (prioridad alta): patrones en patterns/ no cubiertos en handwritten_extra.
# Claves = regex exactas de explain/patterns/python_lang.py, python_warnings.py, python_frameworks.py

from __future__ import annotations

from typing import Any


def _(
    mal: str,
    bien: str,
    que: str,
    regla: str,
) -> dict[str, Any]:
    return {
        "codigo_incorrecto": mal,
        "codigo_correcto": bien,
        "que_paso": que,
        "regla": regla,
    }


CAPSULES_PYTHON_PRIORITY: dict[str, dict[str, Any]] = {
    # Misma clave que ERRORES_PYTHON (patrón combinado distinto de UserWarning:/RuntimeWarning: sueltos).
    r"UserWarning|RuntimeWarning": _(
        "warnings.warn('dato raro')  # numpy/pandas",
        "Leé el texto del warning y la doc de la versión de la librería",
        "Una librería emitió `UserWarning` o `RuntimeWarning` (uso dudoso, overflow, etc.).",
        "El mensaje suele indicar la causa; no lo ignores en CI si afecta resultados numéricos.",
    ),
    r"SyntaxError:.*future feature": _(
        "match x:\n    case _:\n        pass",
        "# Python < 3.10: sin match/case; usá if/elif o subí versión",
        "Usás sintaxis de una versión de Python más nueva que el intérprete.",
        "Alineá `python --version` con el código o reescribí sin esa feature.",
    ),
    r"StopIteration": _(
        "def g():\n    raise StopIteration\n    yield 1",
        "def g():\n    return  # fin del generador",
        "StopIteration en generadores: en PEP 479 se convierte en RuntimeError si se propaga mal.",
        "No captures `StopIteration` manualmente al consumir generators; dejá que `for`/`next` lo manejen.",
    ),
    r"AssertionError:": _(
        "assert usuario_edad > 0",
        "if usuario_edad <= 0:\n    raise ValueError('edad inválida')",
        "`assert` falló: condición falsa en desarrollo/tests.",
        "No uses `assert` para validar entrada de usuario (`python -O` lo elimina).",
    ),
    r"PermissionError:": _(
        "open('/root/secreto.txt')",
        "open(Path.home() / 'datos.txt', 'w')",
        "El proceso no tiene permiso de lectura/escritura en esa ruta.",
        "Revisá dueño, `chmod`, y que no escribas en directorios del sistema sin privilegios.",
    ),
    r"IsADirectoryError|NotADirectoryError": _(
        "open('/tmp', 'r')",
        "open('/tmp/archivo.txt', 'r')",
        "Abrís un directorio como archivo, o operación de directorio sobre un archivo.",
        "Usá `pathlib.Path.is_dir()` / `is_file()` antes de `open`.",
    ),
    r"UnicodeDecodeError:": _(
        "open('f.bin').read().decode()",
        "open('f.bin', encoding='utf-8', errors='replace').read()",
        "Los bytes no son válidos para el encoding usado al decodificar.",
        "Especificá `encoding` y `errors`; detectá encoding si el origen es desconocido.",
    ),
    r"UnicodeEncodeError:": _(
        "print(texto_raro)  # consola latin-1",
        "sys.stdout.reconfigure(encoding='utf-8')  # o escribí a archivo UTF-8",
        "No se puede representar el carácter en el encoding de salida.",
        "UTF-8 en terminal/archivo o `encode(..., errors='replace')`.",
    ),
    r"OSError:.*Address already in use": _(
        "s.bind(('0.0.0.0', 8000))  # puerto ocupado",
        "s.bind(('0.0.0.0', 0))  # o otro puerto libre",
        "Otro proceso ya escucha en ese puerto.",
        "`ss -tlnp` / `lsof -i` y matá el proceso o cambiá el puerto.",
    ),
    r"BrokenPipeError|ConnectionResetError|ConnectionRefusedError": _(
        "sock.send(b'data')  # peer ya cerró",
        "try:\n    sock.send(b'data')\nexcept BrokenPipeError:\n    pass",
        "El otro extremo cerró la conexión o rechazó el intento.",
        "Verificá que el servidor esté arriba, firewall, y manejá reconexión.",
    ),
    r"TimeoutError:": _(
        "await asyncio.wait_for(slow(), timeout=0.001)",
        "Aumentá timeout o optimizá la operación.",
        "La operación excedió el tiempo límite (asyncio, sockets, etc.).",
        "Valores de timeout realistas y reintentos con backoff.",
    ),
    r"MemoryError:": _(
        "xs = list(range(10**12))",
        "xs = range(10**12)  # lazy, o generador por lotes",
        "El proceso no pudo reservar más memoria.",
        "Generadores, streaming, tipos más compactos; revisá fugas.",
    ),
    r"GeneratorExit|asyncio\.CancelledError": _(
        "async def t():\n    raise asyncio.CancelledError",
        "async def t():\n    try:\n        await work()\n    finally:\n        cleanup()",
        "Tarea o generador cancelado durante shutdown o `task.cancel()`.",
        "`finally` para liberar recursos; no silencies cancelación sin criterio.",
    ),
    r"pickle\.|PicklingError|UnpicklingError": _(
        "pickle.dumps(lambda x: x)",
        "json.dumps({'a': 1})  # o registra clase pickleable",
        "Objeto no serializable con pickle o clase desconocida al cargar.",
        "Evitá pickle con datos no confiables; preferí JSON para datos simples.",
    ),
    r"sqlite3\.|OperationalError: no such table": _(
        "conn.execute('SELECT * FROM users')",
        "conn.execute('CREATE TABLE IF NOT EXISTS users (...)')",
        "Tabla o SQL incorrecto en SQLite.",
        "Migraciones/schema y nombres de tabla coincidentes.",
    ),
    r"subprocess\.|CalledProcessError": _(
        "subprocess.run(['false'], check=True)",
        "subprocess.run(['false'], check=False); print(r.returncode)",
        "El subproceso terminó con código distinto de cero y `check=True`.",
        "Leé `stderr`/`stdout` y `returncode`; `check=False` si el fallo es esperado.",
    ),
    r"yaml\.|YAMLError": _(
        "yaml.safe_load('a: [')",
        "yaml.safe_load('a:\\n  - 1')",
        "YAML mal formado (indentación, comillas, estructura).",
        "Indentación consistente; validá con un linter YAML.",
    ),
    r"tomllib\.|tomli": _(
        "tomllib.loads('a =')",
        "tomllib.loads('a = 1')",
        "TOML inválido (Python 3.11+ `tomllib`).",
        "Secciones `[table]`, tipos y comas según spec TOML.",
    ),
    r"pkg_resources\.(DistributionNotFound|VersionConflict)|metadata.*(failed|invalid)": _(
        "import paquete_inexistente",
        "pip install -e . en venv limpio",
        "setuptools/pip: dependencia faltante, conflicto de versión o metadata rota.",
        "`pip check`, venv nuevo, `requirements.txt` alineado.",
    ),
    r"DeprecationWarning|PendingDeprecationWarning": _(
        "import imp  # obsoleto",
        "import importlib",
        "API marcada obsoleta; en el futuro puede eliminarse.",
        "Seguí el mensaje del warning y la documentación de tu versión de Python.",
    ),
    r"IndentationError: expected an indented block": _(
        "def f():\n# falta cuerpo",
        "def f():\n    pass",
        "Después de `:` debe haber una línea indentada.",
        "Añadí cuerpo o `pass` como placeholder.",
    ),
    r"SyntaxError:.*await outside async": _(
        "result = await fetch()",
        "async def main():\n    result = await fetch()",
        "`await` solo dentro de `async def` (o en ciertos contextos top-level controlados).",
        "Envolvé en `async def` y usá `asyncio.run(main())`.",
    ),
    r"TypeError:.*missing .* required": _(
        "def f(a, b): pass\nf(1)",
        "f(1, 2)  # o def f(a, b=0)",
        "Falta argumento posicional u obligatorio por nombre.",
        "Compará la llamada con la firma; valores por omisión o kwargs.",
    ),
    r"BufferError|buffer": _(
        "mv = memoryview(b'abc')\nmv.release()\nmv[0]",
        "No uses la vista después de `release()`.",
        "Operación inválida sobre buffer o memoryview liberada.",
        "Sincronizá el ciclo de vida de vistas y exports.",
    ),
    r"EOFError:": _(
        "input()  # stdin vacío (pipe)",
        "if sys.stdin.isatty(): ... else: leer con try/except EOFError",
        "Fin de entrada inesperado (`input()`, `read()`).",
        "Comprobá pipelines y archivos vacíos.",
    ),
    r"FloatingPointError|OverflowError": _(
        "1e308 * 1e308",
        "import decimal\ndecimal.Decimal('1e400')  # o numpy con dtype",
        "Resultado numérico fuera de rango o operación float inválida.",
        "`decimal.Decimal` o dtypes explícitos en NumPy.",
    ),
    r"SystemExit:": _(
        "import sys\nsys.exit(1)",
        "# intencional en CLI: documentá códigos de salida",
        "Salida explícita del intérprete vía `sys.exit` o `quit()`.",
        "En tests/CI, códigos de salida coherentes (0 éxito, ≠0 error).",
    ),
    r"KeyboardInterrupt": _(
        "# Ctrl+C durante bucle largo",
        "try:\n    ...\nexcept KeyboardInterrupt:\n    print('cancelado')",
        "El usuario pulsó Ctrl+C.",
        "Cleanup en `except KeyboardInterrupt` o `finally` si hace falta.",
    ),
    r"ssl\.SSLError|SSLCertVerificationError|CERTIFICATE_VERIFY_FAILED": _(
        "requests.get('https://...', verify=True)  # CA vieja",
        "Actualizá certifi / CA del sistema; no desactives verify sin criterio fuerte",
        "Handshake TLS fallido o cadena de certificados no confiable.",
        "Fecha del sistema, bundle de CA, y `verify=` solo en entornos controlados.",
    ),
    r"BlockingIOError:|InterruptedError:": _(
        "sock.setblocking(False)\nsock.recv(4096)  # sin datos",
        "select/poll o loop async hasta que haya datos",
        "E/S no bloqueante sin datos, o syscall interrumpida por señal.",
        "Patrones `try again` / `EINTR` según el caso.",
    ),
    r"asyncio\.(CancelledError|TimeoutError|InvalidStateError)": _(
        "fut = asyncio.Future()\nfut.set_result(1)\nfut.set_result(2)",
        "Una sola transición de estado por Future.",
        "Tarea cancelada, `wait_for` expiró, o Future en estado inválido.",
        "`asyncio.wait_for`, manejo de `CancelledError`, no reutilices Futures mal.",
    ),
    r"configparser\.(Error|NoSectionError|NoOptionError|InterpolationError)": _(
        "cfg.get('inexistente', 'clave')",
        "cfg.has_section('seccion') and cfg.get('seccion', 'clave')",
        "INI mal formado o sección/opción ausente.",
        "`[secciones]`, claves correctas; `RawConfigParser` si `%` molesta.",
    ),
    r"xml\.etree\.ElementTree\.ParseError|ExpatError:": _(
        "ET.fromstring('<root><a>')",
        "ET.fromstring('<root><a/></root>')",
        "XML mal cerrado, entidades o encoding incorrecto.",
        "Validá contra esquema; `encoding=` explícito al leer bytes.",
    ),
    r"zipfile\.(BadZipFile|LargeZipFile)": _(
        "zipfile.ZipFile('no_es_zip.zip')",
        "Verificá que el archivo sea ZIP íntegro y no corrupto.",
        "Archivo corrupto, no ZIP, o supera límites sin ZIP64.",
        "Integridad del archivo; `ZIP64` para archivos muy grandes.",
    ),
    r"csv\.Error:": _(
        'csv.reader(io.StringIO(\'a,"b\'))',
        "Ajustá quoting y dialecto al formato real del CSV.",
        "Fila mal formada para el dialecto (comillas, delimitador).",
        "`csv.Sniffer` o dialect explícito; encoding al abrir el archivo.",
    ),
    r"PendingDeprecationWarning:": _(
        "warnings.warn('viejo', PendingDeprecationWarning)",
        "Migrá antes de que pase a DeprecationWarning.",
        "Aviso previo a deprecación fuerte.",
        "Planificá migración según el mensaje.",
    ),
    r"SyntaxWarning:": _(
        "x is \"\"",
        "x == \"\"  # o bool(x) según intención",
        "Construcción sintáctica dudosa o ambigua.",
        "Seguí la sugerencia del warning (`is` vs `==`, etc.).",
    ),
    r"BytesWarning:": _(
        "if b'x' == 'x': pass",
        "Compará str con str y bytes con bytes.",
        "Comparación o mezcla dudosa str/bytes.",
        "Literales `b'...'` y decode/encode explícitos.",
    ),
    r"ImportWarning:": _(
        "# import hook o finder inusual",
        "Revisá estructura de paquete y `__init__.py`.",
        "Problema menor en el proceso de importación.",
        "Rutas, namespace packages, y versiones de Python.",
    ),
    r"UnicodeWarning:": _(
        "# operación Unicode en entorno mixto",
        "Normalizá a UTF-8 y manejá errores en decode/encode.",
        "Operación Unicode potencialmente problemática.",
        "Encoding consistente en todo el pipeline.",
    ),
    r"FutureWarning:": _(
        "import pandas as pd\n# API que cambiará en próxima major",
        "Adaptá a la API nueva indicada en el mensaje (NumPy/pandas típico).",
        "El comportamiento cambiará en una versión futura.",
        "Leé el texto del warning y la guía de migración de la librería.",
    ),
    r"EncodingWarning:": _(
        "open('f.txt')  # sin encoding en 3.10+",
        "open('f.txt', encoding='utf-8')",
        "Python avisa de encoding implícito ambiguo al abrir texto.",
        "`encoding='utf-8'` explícito en `open()`.",
    ),
    r"RuntimeWarning:": _(
        "import numpy as np\nnp.float128  # ejemplo según versión",
        "Revisá el mensaje y documentación del módulo.",
        "Situación sospechosa en runtime (numpy, math, etc.).",
        "Stack trace y datos de entrada; no ignores en CI si es crítico.",
    ),
    # --- Frameworks (python_frameworks.py) complementarios ---
    r"django\.core\.exceptions\.PermissionDenied": _(
        "raise PermissionDenied()",
        "@login_required o permisos explícitos en la vista",
        "Django bloqueó la vista o `raise PermissionDenied`.",
        "Autenticación, `PermissionDenied` vs redirect a login, tests con usuario.",
    ),
    r"django\.core\.exceptions\.DisallowedHost": _(
        "ALLOWED_HOSTS = []",
        "ALLOWED_HOSTS = ['localhost', '127.0.0.1']",
        "El header Host no está en ALLOWED_HOSTS.",
        "Dominios reales en prod; proxy y `USE_X_FORWARDED_HOST` si aplica.",
    ),
    r"django\.core\.exceptions\.FieldError": _(
        "Model.objects.filter(campo_typo=1)",
        "Nombre de campo según el modelo y migraciones aplicadas.",
        "Campo inválido en QuerySet o Meta.",
        "`select_related`/`values` con nombres correctos; `migrate`.",
    ),
    r"MultipleObjectsReturned": _(
        "Model.objects.get(nombre='dup')  # hay dos",
        "Model.objects.filter(nombre='dup').first()",
        "`get()` encontró más de una fila.",
        "Restringí la consulta o usá `filter`; unique en BD si debe ser único.",
    ),
    r"django\.db\.utils\.(OperationalError|ProgrammingError)": _(
        "# BD caída o SQL inválido",
        "migrate, credenciales DATABASES, revisá SQL en traceback",
        "Error de conexión o SQL en el ORM.",
        "Servidor BD, migraciones pendientes, SQL generado.",
    ),
    r"django\.db\.migrations\.exceptions\.(InconsistentMigrationHistory|CircularDependency)": _(
        "# historial de migraciones desincronizado",
        "merge migrations, backup antes de --fake",
        "Historial de migraciones inconsistente entre ramas.",
        "`showmigrations`, merge cuidadoso, documentación Django.",
    ),
    r"starlette\.exceptions\.|starlette\.routing\.": _(
        "# FastAPI/Starlette: 404 o middleware",
        "Orden de middleware, Mount vs include_router",
        "Capa ASGI: ruta, WebSocket o middleware.",
        "Revisá orden de capas y prefijos de rutas.",
    ),
    r"pydantic\.errors\.(PydanticUserError|ConfigError)": _(
        "class M(BaseModel):\n    model_config = {}  # incompatible v1/v2",
        "Seguí model_config de Pydantic v2 o docs de tu versión",
        "Modelo mal definido o opción incompatible.",
        "Guía de migración v1→v2 y `model_config`.",
    ),
    r"sqlalchemy\.exc\.(OperationalError|ProgrammingError|DatabaseError)": _(
        "session.execute(text('SELECT ...'))  # SQL inválido",
        "echo=True en engine, URL y pool_pre_ping",
        "Driver rechazó query o perdió conexión.",
        "Cadena del engine, reconexión, SQL exacto en logs.",
    ),
    r"sqlalchemy\.exc\.(NoReferencedTableError|InvalidRequestError|ArgumentError)": _(
        "ForeignKey('otra.id') sin mapear Otra",
        "Declará todas las tablas en Base.metadata en orden coherente",
        "FK a tabla no mapeada o relación mal declarada.",
        "`relationship`, `back_populates`, orden de imports de modelos.",
    ),
    r"sqlalchemy\.orm\.exc\.(DetachedInstanceError|ObjectDeletedError|StaleDataError)": _(
        "session.close()\nprint(obj.attr)",
        "session.merge(obj) o no cierres antes de leer",
        "Objeto ORM fuera de sesión, borrado o concurrencia optimista.",
        "`expire_on_commit`, `refresh`, transacciones acotadas.",
    ),
    r"alembic\.util\.exc\.CommandError": _(
        "alembic upgrade head  # falla",
        "alembic heads; merge; revisá env.py",
        "Comando Alembic falló (heads múltiples, branch).",
        "`script_location`, revisiones y merge.",
    ),
    r"celery\.exceptions\.|billiard\.exceptions\.": _(
        "# worker Celery caído o task falló",
        "Broker URL, result_backend, logs del worker",
        "Worker, broker o pool reportó error.",
        "Redis/Rabbit arriba; `task_always_eager` en tests.",
    ),
    r"kombu\.exceptions\.|amqp\.exceptions\.": _(
        "# conexión AMQP rechazada",
        "vhost, usuario, firewall, versión del broker",
        "Cola de mensajes rechazó conexión o formato.",
        "Credenciales y conectividad al broker.",
    ),
    r"redis\.exceptions\.(ConnectionError|TimeoutError|BusyLoadingError)": _(
        "r = redis.Redis(); r.get('k')  # sin servidor",
        "redis-cli ping; maxclients; retry",
        "Redis inalcanzable, timeout o cargando dataset.",
        "Conexión estable y límites del servidor.",
    ),
    r"httpx\.(ConnectError|ReadTimeout|HTTPStatusError|LocalProtocolError)": _(
        "httpx.get(url, timeout=0.001)",
        "Timeouts razonables; raise_for_status() con manejo",
        "Cliente HTTP falló al conectar, leer o código inesperado.",
        "URL, TLS, `verify`, timeouts explícitos.",
    ),
    r"requests\.exceptions\.(ConnectionError|HTTPError|Timeout|SSLError|ChunkedEncodingError)": _(
        "requests.get(url, timeout=1)",
        "Reintentos, verify según entorno, stream si cuerpo grande",
        "Red, TLS, timeout o cuerpo corrupto en Requests.",
        "`response.raise_for_status()`, SSL, proxies.",
    ),
    r"pymongo\.errors\.(DuplicateKeyError|ServerSelectionTimeoutError|ConfigurationError)": _(
        "coll.insert_one({'_id': 1}); coll.insert_one({'_id': 1})",
        "Índice único y datos; connection string y replicaSet",
        "MongoDB: clave duplicada, sin servidor o URI inválida.",
        "Índices, string de conexión y topología.",
    ),
    r"pytest\.fixture|fixture.*not found|PytestDeprecationWarning.*fixture": _(
        "def test_x(missing_fixture): pass",
        "def missing_fixture(): return 1\n# o conftest.py en path",
        "Fixture inexistente o plugin no cargado.",
        "Nombre del argumento = nombre del fixture; `conftest.py`.",
    ),
    r"_pytest\.(config|runner)\.|ERROR at setup|ERROR at teardown": _(
        "# fallo en fixture autouse",
        "Traceback completo arriba; yield fixture con cleanup",
        "Error en setup/teardown de pytest.",
        "Fixture con `yield` y excepciones en hooks.",
    ),
    r"gunicorn\.errors\.|WORKER TIMEOUT|Worker failed to boot": _(
        "# worker Gunicorn muere al boot",
        "--log-level debug; revisá import de wsgi:application",
        "Worker timeout o fallo al cargar la app WSGI.",
        "Imports en `wsgi.py`, timeouts y número de workers.",
    ),
    r"werkzeug\.exceptions\.(BadRequest|Unauthorized|Forbidden|InternalServerError)": _(
        "abort(400)",
        "Validá input del cliente o credenciales",
        "Flask/Werkzeug mapeó a código HTTP concreto.",
        "`abort(code)` y manejo de errores en la vista.",
    ),
}

__all__ = ["CAPSULES_PYTHON_PRIORITY"]
