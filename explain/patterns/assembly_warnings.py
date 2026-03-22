# Advertencias del ensamblador (gas, clang -Wassembler, LLVM-MC) — x86, ARM, AArch64.

WARNINGS_ASM = {
    r"warning:.*shift count|Warning:.*shift": {
        "titulo": "Ensamblador — conteo de desplazamiento",
        "explicacion": "El desplazamiento puede exceder el ancho del operando o ser cero de forma sospechosa. En asm puro el manual de la ISA define qué pasa; mezclado con C, shifts inválidos en C siguen siendo UB en ese lado.",
        "soluciones": ["Verificá inmediato vs tamaño real", "Máscara explícita", "Documentá el comportamiento del modelo de CPU"],
    },
    r"warning:.*implementation defined|warning:.*implementation-defined|Warning:.*unspecified": {
        "titulo": "Asm — implementación definida / no especificado",
        "explicacion": "No siempre es UB del estándar C, pero el resultado puede depender del ensamblador, del modo (ARM/Thumb, 32/64) o del microarquitectura.",
        "soluciones": ["Fijá modo y directivas (.syntax, .code64)", "Probá en el target real", "Consultá el manual del fabricante"],
    },
    r"warning:.*end of file|Warning:.*end of file": {
        "titulo": "Ensamblador — archivo incompleto",
        "explicacion": "Comentario, cadena o macro sin cerrar antes del EOF.",
        "soluciones": ["Cerrá */ o comillas", "Revisá .macro/.endm"],
    },
    r"warning:.*alignment|Warning:.*align|alignment larger than": {
        "titulo": "Ensamblador — alineación dudosa",
        "explicacion": "Alineación muy grande o redundante respecto al segmento.",
        "soluciones": ["Valor razonable para la ISA", "Revisá documentación de .align"],
    },
    r"warning:.*signed overflow|overflow in expression": {
        "titulo": "Ensamblador — desbordamiento en expresión",
        "explicacion": "Constante o aritmética en tiempo de ensamblado desborda el rango.",
        "soluciones": ["Usá masking explícito", "Revisá tamaño del campo destino"],
    },
    r"warning:.*deprecated|Deprecated instruction|obsolete mnemonic": {
        "titulo": "Ensamblador — mnemónico obsoleto",
        "explicacion": "El fabricante o gas marca la forma antigua; puede desaparecer.",
        "soluciones": ["Sustituí por forma recomendada en el mensaje", "Manual actual"],
    },
    r"warning:.*changing section|section flags.*changed": {
        "titulo": "Ensamblador — cambio de sección",
        "explicacion": "Reubicación de código entre .text/.data o flags distintos; a veces solo informativo.",
        "soluciones": ["Orden explícito de .section", "Revisá si afecta permisos NX/W^X"],
    },
    r"warning:.*x86-64.*32-bit|32-bit.*x86-64|mismatch.*mode": {
        "titulo": "x86 — aviso de modo 32/64",
        "explicacion": "Mezcla sospechosa de convenciones o directivas .code32/.code64.",
        "soluciones": ["Unificá el modo del objeto", "Revisá startup y linker script"],
    },
    r"warning:.*AVX|SSE.*transition|vzeroupper": {
        "titulo": "x86 — transición SSE/AVX",
        "explicacion": "Llamada entre código AVX y no-AVX puede penalizar o fallar en algunas CPUs.",
        "soluciones": ["vzeroupper antes de ABI no-AVX", "Aislar rutas SIMD"],
    },
    r"warning:.*ARM.*Thumb|Thumb.*warning|unified syntax": {
        "titulo": "ARM — Thumb / sintaxis unificada",
        "explicacion": "Gas sugiere .syntax unified o advierte de modo ARM vs Thumb.",
        "soluciones": [".syntax unified al inicio", ".thumb_func en etiquetas de interrupción"],
    },
    r"warning:.*literal pool|ltorg|pool may be out of range": {
        "titulo": "ARM — literal pool",
        "explicacion": "El ensamblador avisa que un pool podría quedar lejos; en runtime puede fallar el acceso.",
        "soluciones": [".ltorg antes de saltos largos", "Reorganizá el flujo"],
    },
    r"warning:.*aarch64|AArch64.*warning|Wn.*asm": {
        "titulo": "AArch64 — aviso del ensamblador",
        "explicacion": "Clang/gas emitió -Wa, o detalle de codificación en 64 bits.",
        "soluciones": ["Leé el texto completo", "-Wno-error si es transitorio en migración"],
    },
    r"warning:.*indirect.*call|retpoline|spectre|speculation": {
        "titulo": "x86 — mitigación / llamada indirecta",
        "explicacion": "Toolchain sugiere retpoline, thunk o IBT por política de seguridad.",
        "soluciones": ["Flags -mindirect-branch", "Documentación del kernel o distro"],
    },
    r"note:.*while assembling|note:.*instantiated from": {
        "titulo": "Ensamblador — nota (macro/include)",
        "explicacion": "Traza de macro o archivo incluido; el error real suele estar arriba o abajo.",
        "soluciones": ["Seguí la cadena de .include/.macro", "Revisá la línea citada"],
    },
    r"warning:.*suggest.*use of|warning:.*did you mean": {
        "titulo": "Sugerencia de mnemónico",
        "explicacion": "El ensamblador sugiere otro mnemónico o tamaño de operando.",
        "soluciones": ["Seguí la sugerencia o consultá el manual de la ISA"],
    },
    r"warning:.*for subroutine|warning:.*stack frame": {
        "titulo": "Marco de pila / subrutina",
        "explicacion": "Aviso sobre tamaño de frame o alineación de función.",
        "soluciones": ["Revisá push/pop balanceados", "ABI de la plataforma"],
    },
}
