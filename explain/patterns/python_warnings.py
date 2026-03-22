# Advertencias de Python (warnings module, deprecations). Español fijo.

WARNINGS_PYTHON = {
    r"DeprecationWarning:": {
        "titulo": "DeprecationWarning",
        "explicacion": "Usas una API que el lenguaje o la biblioteca marcan como obsoleta; en versiones futuras puede eliminarse.",
        "soluciones": ["Lee el mensaje: suele indicar el reemplazo. Actualiza el código o filtra el warning solo si es transitorio."],
    },
    r"PendingDeprecationWarning:": {
        "titulo": "PendingDeprecationWarning",
        "explicacion": "Advertencia previa a una futura deprecación fuerte.",
        "soluciones": ["Planifica la migración antes de que pase a DeprecationWarning."],
    },
    r"ResourceWarning:": {
        "titulo": "ResourceWarning",
        "explicacion": "Recurso del sistema no cerrado explícitamente (archivos, sockets) detectado por el GC o -W default.",
        "soluciones": ["Usa with open(...) o .close() / context managers."],
    },
    r"SyntaxWarning:": {
        "titulo": "SyntaxWarning",
        "explicacion": "Construcción sintáctica dudosa o ambigua que podría cambiar de significado.",
        "soluciones": ["Ajusta la expresión según indica el mensaje (p. ej. tuplas, is vs ==)."],
    },
    r"BytesWarning:": {
        "titulo": "BytesWarning",
        "explicacion": "Mezcla o comparación dudosa entre str y bytes, o str() sobre bytes.",
        "soluciones": ["Decodifica o codifica con encoding conocido", "Literales b'...' coherentes"],
    },
    r"ImportWarning:": {
        "titulo": "ImportWarning",
        "explicacion": "Problema menor en el proceso de importación (p. ej. finders).",
        "soluciones": ["Revisa rutas de paquetes y __init__.py."],
    },
    r"UnicodeWarning:": {
        "titulo": "UnicodeWarning",
        "explicacion": "Operación Unicode potencialmente problemática en entornos mixtos.",
        "soluciones": ["Normaliza encoding (UTF-8) y maneja errores en decode/encode."],
    },
    r"UserWarning:": {
        "titulo": "UserWarning",
        "explicacion": "Una biblioteca o tu código emitió warnings.warn() genérico.",
        "soluciones": ["Lee el texto del warning y la documentación del módulo que lo lanza."],
    },
    r"RuntimeWarning:": {
        "titulo": "RuntimeWarning",
        "explicacion": "Situación sospechosa en tiempo de ejecución (p. ej. float overflow en numpy, división rara).",
        "soluciones": ["Revisa el stack y los datos de entrada."],
    },
    r"FutureWarning:": {
        "titulo": "FutureWarning",
        "explicacion": "El comportamiento cambiará en una versión futura; típico en NumPy/pandas.",
        "soluciones": ["Adapta el código a la API nueva indicada en el mensaje."],
    },
    r"EncodingWarning:": {
        "titulo": "EncodingWarning",
        "explicacion": "Python 3.10+ avisa si open() o io usa encoding implícito en entorno ambiguo.",
        "soluciones": ["encoding='utf-8' explícito en open()", "PYTHONWARNINGS=error solo en CI si querés forzar"],
    },
}
