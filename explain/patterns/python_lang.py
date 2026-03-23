"""Errores e excepciones frecuentes de Python."""

ERRORES_PYTHON = {
    r"NameError: name '.*' is not defined": {
        "titulo": "Nombre no definido",
        "explicacion": "El identificador no existe en ese scope o falta import.",
        "soluciones": ["import / from", "global nonlocal si aplica", "typo o orden de definición"],
    },
    r"UnboundLocalError:": {
        "titulo": "Local sin asignar previa",
        "explicacion": "Asignás a una variable local en la función pero leés antes de asignar.",
        "soluciones": ["Inicializá antes del branch", "global si debés usar el global"],
    },
    r"IndentationError:": {
        "titulo": "Indentación inválida",
        "explicacion": "Bloques mal alineados o mezcla tabs/espacios.",
        "soluciones": ["Solo espacios, 4 por nivel", "Editor: mostrar whitespace"],
    },
    r"TabError:": {
        "titulo": "Tabs y espacios mezclados",
        "explicacion": "Inconsistencia de indentación.",
        "soluciones": ["Convertir archivo a espacios"],
    },
    r"SyntaxError: invalid syntax": {
        "titulo": "Sintaxis inválida",
        "explicacion": "Construcción ilegal; a veces el error marca la línea siguiente.",
        "soluciones": ["Paréntesis/llaves", "Dos puntos en def/if/for/class", "await solo en async"],
    },
    r"SyntaxError:.*EOL|unterminated string": {
        "titulo": "Cadena sin cerrar",
        "explicacion": "Comillas o triple-comillas sin cerrar.",
        "soluciones": ["Cerrá comillas", "Raw string r\"\" si hay backslashes"],
    },
    r"SyntaxError:.*future feature": {
        "titulo": "Feature futura no disponible",
        "explicacion": "from __future__ o sintaxis de versión más nueva que tu intérprete.",
        "soluciones": ["Subí versión de Python", "Quita el import future si no aplica"],
    },
    r"TypeError: unsupported operand type": {
        "titulo": "Operación entre tipos",
        "explicacion": "Operador no definido para esa combinación de tipos.",
        "soluciones": ["int()/str()/float()", "isinstance antes de operar"],
    },
    r"TypeError:.*takes .* positional argument": {
        "titulo": "Cantidad de argumentos",
        "explicacion": "Más o menos args que la firma.",
        "soluciones": ["help(f)", "self en métodos de instancia"],
    },
    r"TypeError:.*not callable": {
        "titulo": "No es invocable",
        "explicacion": "Llamás () sobre algo que no es función/clase callable.",
        "soluciones": ["No pongas () si es un valor", "Revisá si pisaste el nombre"],
    },
    r"TypeError:.*must be str|not bytes": {
        "titulo": "str vs bytes",
        "explicacion": "Mezclás texto Unicode con bytes sin decodificar.",
        "soluciones": [".decode()", ".encode()", "open(..., encoding=)"],
    },
    r"AttributeError:.*has no attribute": {
        "titulo": "Atributo inexistente",
        "explicacion": "El objeto no tiene ese nombre (typo, versión, None).",
        "soluciones": ["dir(obj)", "Chequeá None", "Documentación de la versión"],
    },
    r"KeyError:": {
        "titulo": "Clave ausente en dict",
        "explicacion": "dict[k] sin k presente.",
        "soluciones": [".get(k, default)", "k in d"],
    },
    r"IndexError:.*out of range|list index out of range": {
        "titulo": "Índice fuera de rango",
        "explicacion": "Lista/tupla/string indexada fuera de len.",
        "soluciones": ["len()", "Índice negativo válido solo si -len<=i<-1", "lista vacía"],
    },
    r"ValueError:": {
        "titulo": "Valor incorrecto",
        "explicacion": "Tipo correcto pero valor ilegal (int('a'), unpack, etc.).",
        "soluciones": ["Validá entrada", "try/except con mensaje claro"],
    },
    r"ZeroDivisionError:": {
        "titulo": "División por cero",
        "explicacion": "/ o % con divisor cero.",
        "soluciones": ["Guarda if d != 0"],
    },
    r"ModuleNotFoundError: No module named": {
        "titulo": "Módulo no encontrado",
        "explicacion": "pip/venv/path incorrecto.",
        "soluciones": ["pip install", "PYTHONPATH", "venv activado"],
    },
    r"ImportError: cannot import name": {
        "titulo": "Import de nombre fallido",
        "explicacion": "El módulo existe pero no exporta ese símbolo.",
        "soluciones": ["Revisá __all__ y versión del paquete", "import módulo; módulo.x"],
    },
    r"ImportError: attempted relative import": {
        "titulo": "Import relativo fuera de paquete",
        "explicacion": "from .x sin ser paquete o ejecutás script como archivo suelto.",
        "soluciones": ["python -m paquete.modulo", "Estructura con __init__.py"],
    },
    r"RecursionError: maximum recursion depth": {
        "titulo": "Recursión demasiado profunda",
        "explicacion": "Stack overflow lógico o falta caso base.",
        "soluciones": ["Caso base", "Iterativo", "sys.setrecursionlimit solo si sabés"],
    },
    r"StopIteration": {
        "titulo": "StopIteration",
        "explicacion": "Fin del iterador; en generators suele ser normal; en 3.7+ dentro de generator mal manejado.",
        "soluciones": ["No captures StopIteration manualmente en generators PEP 479 context"],
    },
    r"AssertionError:": {
        "titulo": "Assert falló",
        "explicacion": "Condición de assert False en desarrollo/tests.",
        "soluciones": ["Corregí invariante o datos de test", "No uses assert para validar entrada de usuario (puede desactivarse con -O)"],
    },
    r"FileNotFoundError:": {
        "titulo": "Archivo no encontrado",
        "explicacion": "Ruta incorrecta o cwd distinto.",
        "soluciones": ["pathlib / os.path.exists", "Ruta absoluta o relativa al cwd correcto"],
    },
    r"PermissionError:": {
        "titulo": "Permiso denegado",
        "explicacion": "Sin permiso de lectura/escritura/ejecución.",
        "soluciones": ["chmod", "No escribir en / sin sudo", "cerrar archivo abierto"],
    },
    r"IsADirectoryError|NotADirectoryError": {
        "titulo": "Es/no es directorio",
        "explicacion": "open en directorio o operación de dir en archivo.",
        "soluciones": ["Revisá path", "os.path.isdir"],
    },
    r"UnicodeDecodeError:": {
        "titulo": "Decodificación Unicode",
        "explicacion": "Bytes no válidos para el encoding declarado.",
        "soluciones": ["encoding='utf-8', errors='replace'", "Detectá encoding (chardet)"],
    },
    r"UnicodeEncodeError:": {
        "titulo": "Codificación Unicode",
        "explicacion": "Caracteres no representables en el encoding de salida.",
        "soluciones": ["UTF-8 en consola", "encode con errors"],
    },
    r"json\.JSONDecodeError|Expecting value": {
        "titulo": "JSON inválido",
        "explicacion": "Texto no es JSON válido o está truncado.",
        "soluciones": ["Validá fuente", "loads vs load"],
    },
    r"OSError:.*Address already in use": {
        "titulo": "Puerto en uso",
        "explicacion": "socket.bind en puerto ocupado.",
        "soluciones": ["Otro puerto", "Matar proceso previo"],
    },
    r"BrokenPipeError|ConnectionResetError|ConnectionRefusedError": {
        "titulo": "Error de red/conexión",
        "explicacion": "Peer cerró o rechazó conexión.",
        "soluciones": ["Servidor arriba", "Firewall", "Reintentos"],
    },
    r"TimeoutError:": {
        "titulo": "Timeout",
        "explicacion": "Operación I/O o concurrent.futures excedió tiempo.",
        "soluciones": ["Aumentá timeout", "Red más estable"],
    },
    r"MemoryError:": {
        "titulo": "Sin memoria",
        "explicacion": "El proceso no pudo asignar más RAM.",
        "soluciones": ["Generadores en vez de listas enormes", "Revisá fugas", "64-bit"],
    },
    r"RuntimeError:.*asyncio|Event loop is closed": {
        "titulo": "asyncio / event loop",
        "explicacion": "Loop cerrado o coroutine mal await-eada.",
        "soluciones": ["asyncio.run(main())", "No mezcles loops en threads sin cuidado"],
    },
    r"GeneratorExit|asyncio\.CancelledError": {
        "titulo": "Cancelación / cierre generador",
        "explicacion": "Tarea o generador cancelado.",
        "soluciones": ["Manejo en finally", "Revisá shutdown limpio"],
    },
    r"pickle\.|PicklingError|UnpicklingError": {
        "titulo": "pickle",
        "explicacion": "Objeto no serializable o clase no encontrada al cargar.",
        "soluciones": ["json para datos simples", "Registrá clase o mismo código"],
    },
    r"sqlite3\.|OperationalError: no such table": {
        "titulo": "SQLite",
        "explicacion": "Tabla o SQL incorrecto.",
        "soluciones": ["CREATE TABLE", "Nombre de tabla/columna"],
    },
    r"subprocess\.|CalledProcessError": {
        "titulo": "Subproceso falló",
        "explicacion": "Comando hijo retornó código distinto de 0.",
        "soluciones": ["Revisá stderr del hijo", "check=False si es esperado"],
    },
    r"yaml\.|YAMLError": {
        "titulo": "YAML",
        "explicacion": "Sintaxis YAML incorrecta.",
        "soluciones": ["Indentación en YAML", "Validador online"],
    },
    r"tomllib\.|tomli": {
        "titulo": "TOML",
        "explicacion": "Archivo .toml inválido (Python 3.11+ tomllib).",
        "soluciones": ["Comas y secciones [table]", "Comillas"],
    },
    r"pkg_resources\.(DistributionNotFound|VersionConflict)|metadata.*(failed|invalid)": {
        "titulo": "Dependencia / setuptools",
        "explicacion": "Paquete instalado requiere otra versión o metadata corrupta.",
        "soluciones": ["pip install -r requirements", "venv limpio", "pip check"],
    },
    r"DeprecationWarning|PendingDeprecationWarning": {
        "titulo": "API obsoleta",
        "explicacion": "Uso de API que se eliminará.",
        "soluciones": ["Migrá a API nueva según mensaje", "warnings.filter solo si temporal"],
    },
    r"UserWarning|RuntimeWarning": {
        "titulo": "Advertencia de librería",
        "explicacion": "numpy/pandas/etc. avisa de uso dudoso.",
        "soluciones": ["Leé el texto del warning", "Docs de la versión"],
    },
    r"IndentationError: expected an indented block": {
        "titulo": "Falta bloque indentado",
        "explicacion": "Después de : debe haber línea indentada.",
        "soluciones": ["pass si está vacío", "Corpo del if/def"],
    },
    r"SyntaxError:.*await outside async": {
        "titulo": "await fuera de async",
        "explicacion": "await solo en función async.",
        "soluciones": ["async def", "asyncio.run"],
    },
    r"TypeError:.*missing .* required": {
        "titulo": "Argumento requerido faltante",
        "explicacion": "Callable requiere keyword o posicional obligatorio.",
        "soluciones": ["Revisá firma y valores por defecto"],
    },
    r"BufferError|buffer": {
        "titulo": "Buffer / memoryview",
        "explicacion": "Operación inválida sobre buffer exportable.",
        "soluciones": ["Sincronización de vistas", "bytes inmutable"],
    },
    r"EOFError:": {
        "titulo": "EOF inesperado",
        "explicacion": "input() o read sin datos.",
        "soluciones": ["Comprobar fin de archivo", "Pipelines vacíos"],
    },
    r"FloatingPointError|OverflowError": {
        "titulo": "Overflow numérico",
        "explicacion": "Resultado fuera de rango representable.",
        "soluciones": ["decimal.Decimal", "numpy dtypes"],
    },
    r"SystemExit:": {
        "titulo": "sys.exit",
        "explicacion": "Salida explícita del intérprete.",
        "soluciones": ["Código de retorno intencional en CLI"],
    },
    r"KeyboardInterrupt": {
        "titulo": "Interrupción por teclado",
        "explicacion": "Ctrl+C.",
        "soluciones": ["Manejo en try/except si necesitás cleanup"],
    },
    r"ssl\.SSLError|SSLCertVerificationError|CERTIFICATE_VERIFY_FAILED": {
        "titulo": "SSL/TLS",
        "explicacion": "Handshake fallido, certificado inválido o cadena no confiable.",
        "soluciones": ["Actualizá certifi/ca bundle", "verify= en requests solo con criterio", "Fecha del sistema"],
    },
    r"BlockingIOError:|InterruptedError:": {
        "titulo": "E/S no bloqueante / interrupción",
        "explicacion": "Operación no bloqueante sin datos, o syscall interrumpida por señal.",
        "soluciones": ["select/poll", "Reintentar en EINTR", "fcntl O_NONBLOCK con cuidado"],
    },
    r"asyncio\.(CancelledError|TimeoutError|InvalidStateError)": {
        "titulo": "asyncio — cancelación o estado",
        "explicacion": "Tarea cancelada, wait_for expiró o Future en estado inválido.",
        "soluciones": ["asyncio.wait_for timeout", "try/except CancelledError", "shield si aplica"],
    },
    r"configparser\.(Error|NoSectionError|NoOptionError|InterpolationError)": {
        "titulo": "configparser (.ini)",
        "explicacion": "Archivo INI mal formado, sección u opción inexistente.",
        "soluciones": ["Revisá secciones [ ] y claves", "defaults en ConfigParser", "RawConfigParser si % conflictúa"],
    },
    r"xml\.etree\.ElementTree\.ParseError|ExpatError:": {
        "titulo": "XML mal formado",
        "explicacion": "Parser XML rechazó el documento (cierre de tag, encoding).",
        "soluciones": ["Validá contra un esquema", "encoding= explícito", "Entidad & escapada"],
    },
    r"zipfile\.(BadZipFile|LargeZipFile)": {
        "titulo": "ZIP inválido o demasiado grande",
        "explicacion": "Archivo corrupto, no es zip, o supera límites de zipfile.",
        "soluciones": ["Comprobá integridad del archivo", "zipfile.ZIP64 si aplica"],
    },
    r"csv\.Error:": {
        "titulo": "csv.Error",
        "explicacion": "Línea mal formada para el dialecto (comillas, delimitador).",
        "soluciones": ["Dialect y quoting", "errors='replace' en open si encoding"],
    },
    r"struct\.error:": {
        "titulo": "struct — empaquetado binario",
        "explicacion": "struct.pack/unpack: tamaño, alineación o tipos no coinciden con el formato.",
        "soluciones": ["Revisá la cadena de formato y len de bytes", "Endianness explícito (< > =)"],
    },
    r"ImportError:.*DLL load failed|ImportError:.*dynamic module": {
        "titulo": "DLL / extensión nativa",
        "explicacion": "Extensión C/Rust no carga: falta .so/.dll, ABI incompatible o dependencia del sistema.",
        "soluciones": ["Misma versión de Python que al compilar", "ldd / Dependencies", "Reinstalá wheel del paquete"],
    },
    r"dataclasses\.FrozenInstanceError": {
        "titulo": "dataclass frozen",
        "explicacion": "Instancia con frozen=True; no se pueden asignar campos.",
        "soluciones": ["dataclasses.replace()", "Nueva instancia en lugar de mutar"],
    },
    r"importlib\.metadata\.PackageNotFoundError": {
        "titulo": "Paquete no instalado (metadata)",
        "explicacion": "version()/metadata() no encuentra el dist en el entorno actual.",
        "soluciones": ["pip install del paquete", "Mismo venv que ejecuta el script"],
    },
    r"zoneinfo\.ZoneInfoNotFoundError|No time zone found with key": {
        "titulo": "Zona horaria IANA",
        "explicacion": "No hay datos tzdata para esa clave o el sistema no los expone.",
        "soluciones": ["Instalá tzdata (paquete del SO o pip)", "Clave IANA correcta (America/...)"],
    },
    r"concurrent\.futures\.(BrokenProcessPool|BrokenExecutor|BrokenThreadPool)": {
        "titulo": "Executor roto",
        "explicacion": "Un worker murió (pickle, crash, OOM) o el pool se cerró.",
        "soluciones": ["Revisá logs del hijo", "Serialización de args en ProcessPool", "Recreá el executor"],
    },
    r"http\.client\.(IncompleteRead|BadStatusLine|RemoteDisconnected|CannotSendRequest)": {
        "titulo": "Cliente HTTP (stdlib)",
        "explicacion": "Respuesta truncada, línea de estado inválida o conexión cerrada por el servidor.",
        "soluciones": ["Reintentos con backoff", "HTTP/1.1 keep-alive y timeouts", "Servidor estable"],
    },
    r"urllib\.error\.(HTTPError|URLError)": {
        "titulo": "urllib — HTTP o URL",
        "explicacion": "Código HTTP de error o fallo de conexión/DNS/certificado.",
        "soluciones": ["urlopen con contexto SSL", "User-Agent y red", "except HTTPError y leer code"],
    },
    r"requests\.exceptions\.(ConnectionError|ConnectTimeout|ReadTimeout|HTTPError|SSLError|ChunkedEncodingError)": {
        "titulo": "requests — red o HTTP",
        "explicacion": "Timeout, TLS, cierre brusco o status 4xx/5xx según raise_for_status.",
        "soluciones": ["timeout=(connect, read)", "verify= y certifi", "response.raise_for_status()"],
    },
    r"socket\.(gaierror|herror)": {
        "titulo": "socket — DNS / host",
        "explicacion": "getaddrinfo/gethostbyname falló (nombre, red o /etc/hosts).",
        "soluciones": ["Typo en hostname", "Conectividad", "IPv6 vs IPv4"],
    },
    r"argparse\.(ArgumentError|ArgumentTypeError)": {
        "titulo": "argparse",
        "explicacion": "Conflicto de flags, tipo de conversión o valor inválido para type=.",
        "soluciones": ["add_argument sin nombres duplicados", "type= int con try en custom"],
    },
    r"ChildProcessError:|ProcessLookupError:": {
        "titulo": "Proceso hijo",
        "explicacion": "PID inexistente, señal a proceso ajeno o wait en hijo ya reaped.",
        "soluciones": ["Revisá pid y permisos", "os.waitpid con cuidado"],
    },
    r"tarfile\.(ReadError|CompressionError|StreamError)": {
        "titulo": "tarfile",
        "explicacion": "Archivo corrupto, truncado o compresión no soportada.",
        "soluciones": ["Integridad del .tar/.gz", "Modo correcto (r:gz, etc.)"],
    },
    r"shelve\.Error|dbm\.error|gdbm\.error": {
        "titulo": "shelve / dbm",
        "explicacion": "Base clave-valor corrupta, formato o bloqueo.",
        "soluciones": ["Cerrá el shelve correctamente", "Misma implementación dbm en todos los hosts"],
    },
    r"email\.errors\.(MessageError|MessageParseError|HeaderParseError)": {
        "titulo": "email — parseo",
        "explicacion": "Cabecera o mensaje MIME mal formado.",
        "soluciones": ["policy=compat32 vs default", "BytesParser para raw bytes"],
    },
    r"ctypes\.ArgumentError": {
        "titulo": "ctypes — argumento",
        "explicacion": "Tipo o valor de arg no coincide con argtypes/restype del foreign function.",
        "soluciones": ["argtypes/restype explícitos", "POINTER y estructuras alineadas"],
    },
    r"multiprocessing\.(AuthenticationError|BufferTooShort)": {
        "titulo": "multiprocessing — auth o buffer",
        "explicacion": "Clave de conexión incorrecta o recv de bytes más corto que esperado.",
        "soluciones": ["Misma authkey entre procesos", "recv_bytes con tamaño acordado"],
    },
    r"NotImplementedError:": {
        "titulo": "No implementado",
        "explicacion": "Código alcanzó raise NotImplementedError o método abstracto sin override real.",
        "soluciones": ["Implementá el método", "ABC con @abstractmethod consciente"],
    },
    r"ExceptionGroup:|BaseExceptionGroup:": {
        "titulo": "ExceptionGroup (3.11+)",
        "explicacion": "Varias excepciones agrupadas (asyncio.TaskGroup, except*).",
        "soluciones": ["except* Tipo", "eg.exceptions y traceback"],
    },
    r"StopAsyncIteration": {
        "titulo": "StopAsyncIteration",
        "explicacion": "Fin del async iterator; similar a StopIteration en async for.",
        "soluciones": ["Manejo en agen", "No confundir con GeneratorExit"],
    },
    r"tokenize\.TokenError:": {
        "titulo": "tokenize — token inválido",
        "explicacion": "tokenize.generate_tokens encontró cadena o bracket mal cerrado.",
        "soluciones": ["Fuente Python sintácticamente válida", "encode en UTF-8"],
    },
    r"getopt\.GetoptError:": {
        "titulo": "getopt",
        "explicacion": "Opción desconocida o falta argumento para opción con parámetro.",
        "soluciones": ["String de opciones correcto", "sys.argv real"],
    },
    r"shutil\.(SameFileError|Error|SpecialFileError)": {
        "titulo": "shutil — copia/movimiento",
        "explicacion": "Origen y destino son el mismo, disco lleno, o archivo especial.",
        "soluciones": ["copy2 vs move", "Espacio en disco", "Permisos"],
    },
    r"gzip\.BadGzipFile|EOFError.*gzip": {
        "titulo": "gzip",
        "explicacion": "Archivo no es gzip válido o está truncado.",
        "soluciones": ["Magic bytes", "Descarga completa"],
    },
    r"bz2\.(BZ2Compressor|BZ2Decompressor)|OSError.*bz2": {
        "titulo": "bz2",
        "explicacion": "Datos comprimidos corruptos o stream incompleto.",
        "soluciones": ["Integridad del archivo", "Modo correcto r/w"],
    },
    r"lzma\.LZMAError|lzma\.error": {
        "titulo": "lzma / .xz",
        "explicacion": "Flujo xz/lzma corrupto o filtros incompatibles.",
        "soluciones": ["Archivo completo", "format= auto"],
    },
    r"decimal\.(InvalidOperation|DivisionByZero|Overflow|Underflow|ConversionSyntax)": {
        "titulo": "decimal",
        "explicacion": "Operación decimal inválida según context (precisión, traps).",
        "soluciones": ["localcontext()", "traps y precisión", "Validá strings con Decimal()"],
    },
    r"statistics\.StatisticsError:": {
        "titulo": "statistics",
        "explicacion": "median/mode/variance con datos insuficientes o multimodal ambiguo.",
        "soluciones": ["Lista no vacía", "Revisá mode con empates"],
    },
    r"weakref\.ReferenceError:": {
        "titulo": "weakref",
        "explicacion": "Referencia débil ya invalidada al objeto recolectado.",
        "soluciones": ["Comprobá ref() antes de usar", "No confíes en weakref para lógica crítica sin lock"],
    },
    r"locale\.Error:": {
        "titulo": "locale",
        "explicacion": "setlocale con nombre de locale no disponible en el SO.",
        "soluciones": ["locale -a", "C.UTF-8 fallback", "LANG en entorno"],
    },
    r"codecs\.(LookupError|CodecRegistryError|CodecEncodeError|CodecDecodeError)": {
        "titulo": "codecs",
        "explicacion": "Encoding desconocido o codec falló al codificar/decodificar.",
        "soluciones": ["encoding válido", "errors='replace'", "Registrar codec custom"],
    },
    r"graphlib\.CycleError:": {
        "titulo": "graphlib — ciclo",
        "explicacion": "TopologicalSorter encontró ciclo en el grafo de dependencias.",
        "soluciones": ["Romper ciclo en datos", "Detectar SCC antes"],
    },
    r"sqlite3\.(IntegrityError|OperationalError|ProgrammingError|DatabaseError)": {
        "titulo": "sqlite3 — SQL",
        "explicacion": "Constraint, BD bloqueada, SQL inválido o API mal usada.",
        "soluciones": ["timeout= en connect", "PRAGMA busy_timeout", "SQL y placeholders"],
    },
    r"smtplib\.(SMTPException|SMTPAuthenticationError|SMTPServerDisconnected)": {
        "titulo": "smtplib",
        "explicacion": "Servidor SMTP rechazó auth, TLS o cerró conexión.",
        "soluciones": ["starttls()", "Puerto 587/465", "Credenciales y app password"],
    },
    r"ftplib\.(error_perm|error_temp|error_reply)": {
        "titulo": "ftplib",
        "explicacion": "Código de respuesta FTP 4xx/5xx o protocolo inesperado.",
        "soluciones": ["Usuario/pass correctos", "Modo PASV", "Firewall"],
    },
    r"imaplib\.IMAP4\.error|poplib\.error_proto": {
        "titulo": "imaplib / poplib",
        "explicacion": "Servidor de correo respondió fuera de protocolo o error de auth.",
        "soluciones": ["SSL context", "OAuth2 si el proveedor lo exige"],
    },
    r"nntplib\.(NNTPTemporaryError|NNTPPermanentError|NNTPReplyError)": {
        "titulo": "nntplib (NNTP)",
        "explicacion": "Servidor de noticias rechazó comando o grupo inexistente.",
        "soluciones": ["Puerto y TLS", "Nombre de grupo exacto"],
    },
    r"plistlib\.InvalidFileException": {
        "titulo": "plistlib",
        "explicacion": "Archivo plist binario/XML corrupto o no es plist.",
        "soluciones": ["Validá con plutil en macOS", "Origen del archivo"],
    },
    r"Unable to configure (formatter|handler)|dictConfig|fileConfig.*ValueError": {
        "titulo": "logging — configuración",
        "explicacion": "fileConfig/dictConfig: sección faltante, clase de handler inexistente o nivel inválido.",
        "soluciones": ["disable_existing_loggers", "Clase calificada en handlers", "Probar dict mínimo"],
    },
    r"asyncio\.(QueueFull|QueueEmpty|IncompleteReadError|LimitOverrunError)": {
        "titulo": "asyncio — cola o stream",
        "explicacion": "Cola llena/vacía, lectura incompleta o línea demasiado larga en StreamReader.",
        "soluciones": ["maxsize y backpressure", "readuntil con limit", "Separador de líneas"],
    },
    r"pathlib\.UnsupportedOperation:": {
        "titulo": "pathlib — operación no soportada",
        "explicacion": "symlink, hardlink u operación no disponible en el SO o filesystem.",
        "soluciones": ["Comprobá os.name", "Alternativa sin symlink"],
    },
    r"badly formed hexadecimal UUID string|InvalidUUIDError": {
        "titulo": "uuid",
        "explicacion": "String no cumple formato UUID.",
        "soluciones": ["UUID() con string válido", "Versión y variant correctos"],
    },
    r"array\.error:": {
        "titulo": "array",
        "explicacion": "Tipocode o tamaño de elemento incompatible al append/frombytes.",
        "soluciones": ["typecode correcto", "len de bytes múltiplo del itemsize"],
    },
    r"tempfile\.(FileExistsError|NotADirectoryError).*mkdtemp|Unable to create": {
        "titulo": "tempfile",
        "explicacion": "No se pudo crear archivo/dir temporal (permisos, disco, colisión).",
        "soluciones": ["TMPDIR escribible", "prefix único"],
    },
    r"mmap\.(error|OSError).*mmap": {
        "titulo": "mmap",
        "explicacion": "Archivo vacío, tamaño 0, o acceso mmap inválido.",
        "soluciones": ["Archivo con tamaño >0", "ACCESS_WRITE coherente"],
    },
    r"ipaddress\.(AddressValueError|NetmaskValueError)": {
        "titulo": "ipaddress",
        "explicacion": "IPv4/IPv6 o máscara mal formada.",
        "soluciones": ["ip_address('x') con string válido", "strict=False si aplica"],
    },
    r"secrets\.token_|binascii\.Error": {
        "titulo": "binascii / datos binarios",
        "explicacion": "Base64/hex mal formado en a2b_base64 u operación similar.",
        "soluciones": ["Padding correcto en base64", "Datos no truncados"],
    },
    r"doctest\.(DocTestFailure|UnexpectedException)": {
        "titulo": "doctest",
        "explicacion": "Salida del ejemplo en docstring no coincide o el ejemplo lanzó.",
        "soluciones": ["Actualizá expected o el código", "NORMALIZE_WHITESPACE"],
    },
    r"unittest\.case\.SkipTest|unittest\.SkipTest": {
        "titulo": "unittest — skip",
        "explicacion": "Test marcado skip o @skipUnless condición.",
        "soluciones": ["Es intencional; revisá condición de skip"],
    },
    r"subprocess\.SubprocessError|subprocess\.TimeoutExpired": {
        "titulo": "subprocess — timeout",
        "explicacion": "communicate(timeout=) expiró o pipe roto.",
        "soluciones": ["kill() del proceso hijo", "timeout mayor o None"],
    },
    r"pickle\.(UnpicklingError|PicklingError)": {
        "titulo": "pickle — serialización",
        "explicacion": "Stream corrupto, clase no importable, o protocolo incompatible al unpickle.",
        "soluciones": ["Misma versión de clases y módulos", "No unpicklear datos no confiables"],
    },
    r"ssl\.SSLError|SSL: CERTIFICATE_VERIFY_FAILED|certificate verify failed": {
        "titulo": "SSL / TLS",
        "explicacion": "Handshake falló: certificado inválido, cadena rota, hostname o reloj del sistema.",
        "soluciones": ["Actualizá CA bundle", "verify= con criterio (no desactivar en prod sin motivo)", "SNI y hostname correctos"],
    },
    r"queue\.(Full|Empty):": {
        "titulo": "queue — llena o vacía",
        "explicacion": "put(block=False) en cola llena o get en vacía según configuración.",
        "soluciones": ["block=True o timeout", "maxsize mayor", "Manejo explícito en consumidor"],
    },
    r"zlib\.error:|CompressionError:.*zlib": {
        "titulo": "zlib — datos comprimidos",
        "explicacion": "Flujo gzip/deflate corrupto o truncado.",
        "soluciones": ["Integridad del archivo", "wbits correcto en decompress"],
    },
}
