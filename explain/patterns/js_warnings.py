# Advertencias de Node, ESLint, TypeScript (no error). Español fijo.

WARNINGS_JS = {
    r"^\(node:\d+\) Warning:": {
        "titulo": "Advertencia de Node.js",
        "explicacion": "El runtime de Node emitió un aviso (deprecación, ExperimentalWarning, etc.).",
        "soluciones": ["Lee el texto completo; actualiza flags o API según la versión de Node."],
    },
    r"ExperimentalWarning:": {
        "titulo": "ExperimentalWarning (Node)",
        "explicacion": "Usas una API marcada como experimental; puede cambiar o desaparecer.",
        "soluciones": ["Evita en producción crítica o fija versión de Node y revisa notas de versión."],
    },
    r"\d+:\d+\s+warning\s+": {
        "titulo": "ESLint: warning",
        "explicacion": "La regla ESLint está en nivel warn: el código viola un estilo o buena práctica.",
        "soluciones": ["Corrige el código o ajusta la regla en .eslintrc si es intencional."],
    },
    r"Warning: The 'NO_COLOR'": {
        "titulo": "Aviso de entorno (ej. NO_COLOR)",
        "explicacion": "Mensaje informativo de herramienta CLI sobre variables de entorno.",
        "soluciones": ["Ignora o configura según la documentación de la herramienta."],
    },
    r"npm WARN": {
        "titulo": "Advertencia de npm",
        "explicacion": "npm informa de dependencias desactualizadas, peer deps, scripts, etc.",
        "soluciones": ["Lee el WARN concreto; npm audit / actualizar paquetes si aplica."],
    },
    r"yarn warning": {
        "titulo": "Advertencia de Yarn",
        "explicacion": "Yarn avisa de resolución de versiones o configuración.",
        "soluciones": ["Revisa el mensaje y package.json / yarn.lock."],
    },
    r"tsconfig.*extends.*not found": {
        "titulo": "tsconfig: extends no encontrado",
        "explicacion": "El archivo base referenciado en extends no existe en la ruta esperada.",
        "soluciones": ["Corrige la ruta o instala el paquete que provee ese tsconfig."],
    },
}
