# React, Next.js, Vue, Angular, Prisma, Vite, esbuild — mensajes típicos en consola / build.

ERRORES_JS_FW = {
    r"Hydration failed|hydration mismatch|did not match|Hydration.*error": {
        "titulo": "React — hidratación (SSR)",
        "explicacion": "El HTML del servidor no coincide con lo que React renderiza en el cliente (texto, atributos, estructura).",
        "soluciones": ["Evitá Date.now()/Math.random en primer render", "suppressHydrationWarning puntual", "Revisá extensiones del navegador"],
    },
    r"Maximum update depth exceeded|Too many re-renders": {
        "titulo": "React — bucle de renders",
        "explicacion": "setState o dispatch en render/useEffect sin dependencias correctas provoca actualizaciones infinitas.",
        "soluciones": ["Dependencias [] o completas", "No actualizar estado en render puro", "useCallback estable"],
    },
    r"Invalid hook call|Hooks can only be called": {
        "titulo": "React — reglas de Hooks",
        "explicacion": "Hook fuera de componente funcional, dos copias de React, o hook condicional.",
        "soluciones": ["Misma instancia de react en monorepo", "No hooks en if sin cuidado", "import desde 'react' único"],
    },
    r"Warning:.*validateDOMNesting|cannot appear as a child of": {
        "titulo": "React — DOM inválido",
        "explicacion": "Jerarquía HTML ilegal (p ej. <p> dentro de <p>).",
        "soluciones": ["Cambiá el wrapper a <div> o fragment", "Revisá componentes UI"],
    },
    r"Minified React error #|react\.dev/errors": {
        "titulo": "React — error minificado",
        "explicacion": "En producción el mensaje es corto; el número apunta a la doc de React.",
        "soluciones": ["Reproducí en build dev", "Buscá el código en react.dev/errors"],
    },
    r"createRoot\(\)|ReactDOM\.render is no longer supported": {
        "titulo": "React 18 — API de montaje",
        "explicacion": "createRoot reemplaza render en React 18.",
        "soluciones": ["createRoot(container).render(<App />)", "Guía de migración oficial"],
    },
    r"Error occurred prerendering|prerender.*error|NEXT_RUNTIME|next/dist": {
        "titulo": "Next.js — prerender / RSC",
        "explicacion": "Fallo en getStaticProps, SSR o Server Component durante el build o request.",
        "soluciones": ["Logs de la página concreta", "await fetch en servidor", "dynamic = 'force-dynamic' si aplica"],
    },
    r"invariant failed|Invariant:|NEXT_NOT_FOUND|NEXT_REDIRECT": {
        "titulo": "Next.js — invariant / navegación",
        "explicacion": "Next lanzó error interno o usaste notFound()/redirect() de forma que aborta el render.",
        "soluciones": ["Revisá rutas app/ vs pages/", "notFound en server components"],
    },
    r"\[Vue warn\]|Vue\.warn": {
        "titulo": "Vue — advertencia en runtime",
        "explicacion": "API deprecada, prop faltante o uso incorrecto del template.",
        "soluciones": ["Mensaje completo del warn", "Vue 2 vs 3 (Composition API)", "eslint-plugin-vue"],
    },
    r"Unknown custom element|Failed to resolve component": {
        "titulo": "Vue — componente no resuelto",
        "explicacion": "Tag no registrado globalmente o import olvidado en SFC.",
        "soluciones": ["components: { }", "app.component", "auto-import Nuxt"],
    },
    r"NG\d+:|angular.*compiler.*error|Error occurs in the template of component": {
        "titulo": "Angular — compilación / plantilla",
        "explicacion": "Error de template, binding o del compilador AOT.",
        "soluciones": ["NGxxxx en angular.io/errors", "strictTemplates", "imports del standalone component"],
    },
    r"PrismaClientKnownRequestError|P20\d{2}:|PrismaClientValidationError|PrismaClientInitializationError": {
        "titulo": "Prisma",
        "explicacion": "Código P2xxx: regla de BD, validación del cliente o conexión/schema.",
        "soluciones": ["prisma migrate dev", "DATABASE_URL", "Referencia P20xx en prisma.io/docs"],
    },
    r"@prisma/client did not initialize|Prisma schema validation": {
        "titulo": "Prisma — cliente o schema",
        "explicacion": "generate no corrido, schema inválido o engine incompatible.",
        "soluciones": ["npx prisma generate", "prisma validate", "binaryTargets en schema"],
    },
    r"\[vite\].*Failed to resolve|Could not resolve.*from|Rollup failed to resolve": {
        "titulo": "Vite / Rollup — resolución",
        "explicacion": "Import apunta a paquete o path que el bundler no encuentra.",
        "soluciones": ["npm i el paquete", "alias en vite.config", "optimizeDeps.include"],
    },
    r"\[vite\].*Internal server error|Transform failed": {
        "titulo": "Vite — transform / dev server",
        "explicacion": "Plugin o esbuild no pudo transformar el archivo (TS, JSX, CSS).",
        "soluciones": ["Stack del plugin", "tsconfig jsx", "extensiones en import"],
    },
    r"esbuild.*error|ERROR:.*esbuild": {
        "titulo": "esbuild",
        "explicacion": "Transpilación o bundling falló (sintaxis, import externo).",
        "soluciones": ["Sintaxis del archivo señalado", "external en config"],
    },
    r"Module not found:.*Can't resolve 'react'|Can't resolve 'react-dom'": {
        "titulo": "Bundler — React no instalado",
        "explicacion": "react o react-dom no están en node_modules o hay duplicados.",
        "soluciones": ["npm ls react", "resolutions/overrides", "una sola versión"],
    },
    r"only works in a Client Component|You're importing a component that needs (useEffect|useState|useRef)": {
        "titulo": "Next.js / RSC — componente cliente vs servidor",
        "explicacion": "En el App Router, un Server Component importó algo que usa estado o efectos solo válidos en cliente.",
        "soluciones": ["'use client' en el archivo hijo", "dynamic(..., { ssr: false }) si aplica", "Separá capas"],
    },
}
