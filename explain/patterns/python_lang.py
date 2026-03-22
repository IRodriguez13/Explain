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
}
