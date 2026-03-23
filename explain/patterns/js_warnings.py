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
    r"bun (warn|warning)|Bun\.v": {
        "titulo": "Advertencia de Bun",
        "explicacion": "El runtime Bun avisa de compatibilidad o resolución distinta a Node.",
        "soluciones": ["Leé el mensaje", "Probá con node para comparar"],
    },
    r"deno (warn|WARNING)": {
        "titulo": "Advertencia de Deno",
        "explicacion": "Deno reporta permisos, imports o deprecaciones.",
        "soluciones": ["Flags --allow-* si aplica", "deno.json imports"],
    },
    r"source map|Failed to parse source map": {
        "titulo": "Source map",
        "explicacion": "Herramienta no pudo cargar o parsear .map para el bundle.",
        "soluciones": ["Generá maps en build", "Ignorá en prod si no depurás ahí"],
    },
    r"corepack (warn|WARNING)|Corepack is about to download": {
        "titulo": "Corepack",
        "explicacion": "Corepack gestiona pnpm/yarn según packageManager; puede descargar un runtime.",
        "soluciones": ["Activá corepack explícito", "Fijá versión en package.json"],
    },
    r"WARN.*\[turbo\]|turbo.*WARN": {
        "titulo": "Turborepo warning",
        "explicacion": "Turbo avisa de caché, pipeline o dependencias entre paquetes.",
        "soluciones": ["Revisá turbo.json y workspaces", "Documentación del mensaje"],
    },
}
