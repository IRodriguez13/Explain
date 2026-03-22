"""Ensamblador (gas, ld, nasm comunes cuando gcc/clang invoca el ensamblador)."""

ERRORES_ASM = {
    r"Error: no such instruction|invalid instruction mnemonic|bad instruction": {
        "titulo": "Instrucción inválida para la arquitectura",
        "explicacion": "El ensamblador no reconoce el mnemónico o no aplica a tu CPU (x86 vs x86-64, ARM).",
        "soluciones": ["Revisá -march/-mtune", "Sintaxis AT&T vs Intel (.intel_syntax)", "Manual de la ISA"],
    },
    r"operand size mismatch|incorrect operand|operand type mismatch": {
        "titulo": "Tamaño o tipo de operando",
        "explicacion": "Los operandos no coinciden en tamaño (8/16/32/64 bits) o tipo.",
        "soluciones": ["Sufijos b/w/l/q en AT&T", "Explicitá tamaño con movl/movq"],
    },
    r"relocation truncated to fit|relocation R_|cannot apply relocation": {
        "titulo": "Relocalización truncada",
        "explicacion": "El salto o dirección no entra en el campo (PIC, modelo de código lejano).",
        "soluciones": ["-fPIC para shared objects", "Modelo medium/large si aplica", "Thunk o GOT"],
    },
    r"undefined symbol|undefined local symbol": {
        "titulo": "Símbolo indefinido (asm/ld)",
        "explicacion": "Etiqueta o símbolo externo no definido o no exportado.",
        "soluciones": [".globl etiqueta", "Linkeá el .o que define el símbolo", "weak vs strong"],
    },
    r"alignment|\.align|balign|p2align": {
        "titulo": "Alineación",
        "explicacion": "Directiva de alineación incorrecta o datos mal alineados para la ISA.",
        "soluciones": ["Revisá .align argumento (bytes vs potencia de 2 según sintaxis)", "padding explícito"],
    },
    r"section|\.section|changed section flags": {
        "titulo": "Sección ELF inválida",
        "explicacion": "Atributos de sección (.text/.data/.bss) incompatibles.",
        "soluciones": ["Revisá flags a,w,x en .section", "Orden de directivas"],
    },
    r"expected comma|parse error|syntax error.*\.s": {
        "titulo": "Sintaxis del ensamblador",
        "explicacion": "Coma, orden de operandos o directiva mal escrita.",
        "soluciones": ["Manual de gas para tu arquitectura", "Compará con ejemplo mínimo"],
    },
    r"can't open.*for reading|Assembler messages": {
        "titulo": "Archivo .s no encontrado",
        "explicacion": "Ruta incorrecta en la regla del Makefile o cwd distinto.",
        "soluciones": ["Verificá rutas relativas", "Dependencias en Makefile"],
    },
    r"macro.*redefinition|endm|\.macro": {
        "titulo": "Macro de ensamblador",
        "explicacion": "Macro duplicada o sin cerrar .endm.",
        "soluciones": ["Nombres únicos", "Cerrá bloques macro"],
    },
    r"floating point|xmm|ymm|SSE|AVX": {
        "titulo": "Registros SIMD / FP",
        "explicacion": "Instrucción SIMD mal formada o requiere flags de CPU.",
        "soluciones": ["-msse4 -mavx2 según necesidad", "Verificá alineación de stack para calling convention"],
    },
    r"call.*clobbered|ABI|stack must be aligned": {
        "titulo": "Convención de llamada / ABI",
        "explicacion": "Stack o registros no respetan el ABI del sistema (red zone, alineación 16).",
        "soluciones": ["Documentación ABI x86-64 System V", "Prolog/epilogo correcto si mezclás C y asm"],
    },
    r"\.type|\.size|STT_FUNC": {
        "titulo": "Metadatos ELF del símbolo",
        "explicacion": "Directivas .type/.size ayudan al depurador y linker; error si inconsistente.",
        "soluciones": ["Patrón .type name, @function / .size name, .-name"],
    },
    r"LLVM-MC|llvm-as": {
        "titulo": "Ensamblador LLVM",
        "explicacion": "Clang usa MC; el mensaje viene de la capa de ensamblado.",
        "soluciones": ["Misma guía que gas/clang -c -S", "Revisá triple target"],
    },
}
