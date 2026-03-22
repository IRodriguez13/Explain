"""Ensamblador: gas/as, clang -integrated-as, ld; x86 (IA-32), x86-64, ARM (A32/T32), AArch64."""

# Errores genéricos + por familia de ISA (mensajes típicos de GNU as, clang, LLVM-MC).

ERRORES_ASM = {
    # --- Genéricos (cualquier backend) ---
    r"Error: no such instruction|invalid instruction mnemonic|bad instruction|unknown opcode": {
        "titulo": "Instrucción inválida para la arquitectura",
        "explicacion": "El ensamblador no reconoce el mnemónico o no existe en el modo CPU elegido (16/32/64 bits x86; ARM vs Thumb; AArch64).",
        "soluciones": ["Revisá -march/-mcpu y .arch/.cpu", "AT&T vs Intel (.intel_syntax)", "Manual de la ISA"],
    },
    r"operand size mismatch|incorrect operand|operand type mismatch|mismatch between operand sizes": {
        "titulo": "Tamaño o tipo de operando",
        "explicacion": "Los operandos no coinciden en tamaño (8/16/32/64 bits) o mezclan memoria/registro incompatible.",
        "soluciones": ["Sufijos b/w/l/q en AT&T (x86)", "movw/movl/movq explícitos", "En AArch64: W vs X registers"],
    },
    r"relocation truncated to fit|relocation R_|cannot apply relocation|relocation out of range": {
        "titulo": "Relocalización truncada o fuera de rango",
        "explicacion": "El salto, GOT o dirección no cabe en el campo (PIC, modelo de código, branch relativo en ARM).",
        "soluciones": ["-fPIC", "thunks / veneer en ARM largo salto", "medium/large model x86 si aplica"],
    },
    r"undefined symbol|undefined local symbol|undefined reference.*\.s:": {
        "titulo": "Símbolo indefinido (asm/ld)",
        "explicacion": "Etiqueta o símbolo externo no definido o no exportado.",
        "soluciones": [".globl / .global", "Linkeá el .o que define el símbolo", "weak vs strong"],
    },
    r"expected comma|parse error|syntax error.*\.s|junk at end of line": {
        "titulo": "Sintaxis del ensamblador",
        "explicacion": "Coma, orden de operandos, directiva o carácter sobrante.",
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
    r"\.type|\.size|STT_FUNC": {
        "titulo": "Metadatos ELF del símbolo",
        "explicacion": "Directivas .type/.size para el linker y depurador; error si inconsistente.",
        "soluciones": [".type name, @function / .size name, .-name"],
    },
    r"LLVM-MC|llvm-as|clang:.*error:.*\.s:": {
        "titulo": "Ensamblador LLVM (clang -cc1as)",
        "explicacion": "Clang usa MC; el mensaje viene del front de ensamblado.",
        "soluciones": ["--target= o triple correcto", "Misma línea en gas con -fno-integrated-as para comparar"],
    },
    # --- x86 IA-32 (i386/i686) ---
    r"bad register name|unknown register|invalid register.*%e|%invalid.*32-bit mode": {
        "titulo": "x86-32 — registro inválido",
        "explicacion": "Registro inexistente en IA-32 (p. ej. nombre mal escrito) o uso de registro de 64 bits en modo 32.",
        "soluciones": ["Solo EAX–EDI, segmentos y XMM según -march", "No uses R8–R15 ni RIP en 32 bits"],
    },
    r"not supported in 32-bit mode|invalid.*in 32-bit|32-bit mode.*64-bit operand|only supported in 64-bit mode": {
        "titulo": "x86 — mezcla 32 vs 64 bits",
        "explicacion": "Instrucción u operando de 64 bits en ensamblado de 32 bits, o al revés.",
        "soluciones": ["Ensamblá con -m64 / triple x86_64", "Usá operandos de 32 bits en .code32"],
    },
    r"RIP-relative|RIP addressing|invalid.*rip|%rip": {
        "titulo": "x86-64 — direccionamiento RIP-relative",
        "explicacion": "RIP-relative es propio de x86-64; en IA-32 no existe RIP como base así.",
        "soluciones": ["PIC en 32 bits usa GOT y EBX", "Cambiá a target 64 bits si necesitás RIP"],
    },
    r"push.*64-bit|pop.*64-bit.*32|stack.*32-bit.*pushq": {
        "titulo": "x86 — pila y tamaño de push/pop",
        "explicacion": "pushq/popq o manipulación de stack incompatible con el modo de código.",
        "soluciones": ["pushl vs pushq según modo", "Mantener alineación según ABI"],
    },
    r"red zone|stack must be aligned|16-byte align|ABI.*x86": {
        "titulo": "x86 — ABI / pila (Sys V)",
        "explicacion": "En x86-64 Sys V hay red zone bajo RSP y alineación 16 bytes antes de call.",
        "soluciones": ["Documentación ABI x86-64", "Prologo que respeta 16-byte alignment"],
    },
    r"xmm|ymm|zmm|SSE|AVX|requires.*SSE|requires.*AVX": {
        "titulo": "x86 — SIMD (SSE/AVX)",
        "explicacion": "Instrucción SIMD no disponible en el -march elegido o operandos mal alineados.",
        "soluciones": ["-msse4.2 -mavx2 -mavx512f según CPU", "Alineá datos a 16/32/64 bytes"],
    },
    # --- x86-64 (amd64) ---
    r"bad register name.*%r(8|9|1[0-5])\b|`r(8|9|1[0-5])'.*invalid|extended register.*32-bit|R8.*R15.*64-bit": {
        "titulo": "x86-64 — registros R8–R15",
        "explicacion": "R8–R15 solo existen en modo largo (64 bits); en IA-32 el ensamblador los rechaza.",
        "soluciones": ["Ensamblá con -m64 / triple x86_64", "En 32 bits usá solo EAX–EDI y equivalentes"],
    },
    r"addressing mode.*invalid|invalid combination of prefixes|lock.*invalid": {
        "titulo": "x86 — modo de direccionamiento o prefijos",
        "explicacion": "Combinación de prefijos LOCK/REP o modR/M no válida para la instrucción.",
        "soluciones": ["Revisá tablas de addressing en manual Intel/AMD", "Simplificá el operando"],
    },
    # --- ARM 32 bits (ARMv7, A32, Thumb, Thumb-2) ---
    r"selected processor does not support|instruction not supported|extension not supported.*arm": {
        "titulo": "ARM — CPU o extensión no soportada",
        "explicacion": "El .cpu/.arch o -mcpu no incluye la instrucción (NEON, Thumb-2, IDIV, etc.).",
        "soluciones": [".arch armv7-a + .thumb/.arm", "-mfpu=neon", "Subí el perfil de CPU en el toolchain"],
    },
    r"cannot assemble.*in.*Thumb|Thumb-2|not supported in ARM state|BX.*Thumb": {
        "titulo": "ARM — estado ARM vs Thumb",
        "explicacion": "Mnemónico solo válido en un modo (A32 vs T32); transición mal hecha.",
        "soluciones": [".thumb / .arm", "BX con bit LSB en destino", "Unified syntax .syntax unified"],
    },
    r"conditional branch out of range|branch out of range|relocation.*ARM.*jump": {
        "titulo": "ARM — salto relativo fuera de alcance",
        "explicacion": "B condicional o relocalización de branch no alcanza (±KB limitados).",
        "soluciones": ["Cadena de saltos o invertir condición", "B + BL lejano", "veneer del linker"],
    },
    r"unpredictable|UNPREDICTABLE|deprecated instruction": {
        "titulo": "ARM — comportamiento impredecible",
        "explicacion": "Encodings o usos que el manual ARM marca como impredecibles o obsoletos.",
        "soluciones": ["Reescribí con secuencia recomendada por ARM ARM", "Evitá PC como operando en ciertos casos"],
    },
    r"ldr.*literal|literal pool|out of range for.*literal": {
        "titulo": "ARM — literal pool (PC-relative load)",
        "explicacion": "Constante demasiado lejos del `ldr rd, =sym` o pool no alcanzable.",
        "soluciones": [".ltorg", "Mové el pool", "múltiples movw/movt"],
    },
    r"IT block|it instruction|Thumb.*IT": {
        "titulo": "ARM — bloque IT (Thumb-2)",
        "explicacion": "Instrucciones condicionales en Thumb requieren IT; mal formado o en ARM state.",
        "soluciones": ["Sintaxis IT{tee} correcta", "En A32 usá condiciones en el mnemónico"],
    },
    # --- AArch64 (ARMv8-A LP64, ILP32 en algunos entornos) ---
    r"(Error|error):.*aarch64|invalid operand.*aarch64|aarch64.*:.*(Error|error)|ARM64.*(Error|error)|unsupported.*for aarch64": {
        "titulo": "AArch64 — operando o sintaxis",
        "explicacion": "Sintaxis específica de 64 bits: registros Xn/Wn, SP, inmediatos con máscaras lógicas.",
        "soluciones": ["Revisá que el inmediato sea válido para movz/movk/orr", "W vs X según ancho"],
    },
    r"immediate out of range|shift amount out of range|invalid shift": {
        "titulo": "AArch64/ARM — inmediato o desplazamiento",
        "explicacion": "El inmediato no cumple las reglas de codificación (barrel shifter, UBFM, etc.).",
        "soluciones": ["Descomponé en varias instrucciones", "ldr desde literal pool (ARM32) o adrp+add (A64)"],
    },
    r"ADRP|adrp.*relocation|page out of range": {
        "titulo": "AArch64 — ADRP / página 4 KiB",
        "explicacion": "ADRP fija bits altos de la dirección; el par adrp+add debe referenciar el símbolo correcto.",
        "soluciones": ["Modelo PIC y -fPIC", "Revisá que el símbolo esté en rango de página"],
    },
    r"(Error|error):.*\b(xzr|wzr)\b|invalid.*\bsp\b.*aarch64|same register.*sp.*xzr": {
        "titulo": "AArch64 — XZR/WZR y SP",
        "explicacion": "Confusión entre registro cero y stack pointer; algunas instrucciones no permiten SP.",
        "soluciones": ["Manual: qué ops aceptan SP", "mov xn, #0 en lugar de usar zr donde no corresponda"],
    },
    r"Scalable Vector Extension|SVE.*not supported|predicate register p[0-9]+|unsupported SVE": {
        "titulo": "AArch64 — SVE / vectores escalables",
        "explicacion": "Instrucción SVE no soportada por -mcpu o toolchain sin la extensión.",
        "soluciones": ["-march=armv8-a+sve o similar", "CPU y binutils/clang con SVE"],
    },
    # --- Secciones / ELF (todas) ---
    r"section|\.section|changed section flags|alignment not a power": {
        "titulo": "Sección ELF o alineación",
        "explicacion": "Directiva .section/.align incorrecta o flags incompatibles.",
        "soluciones": [".balign/.p2align según sintaxis", "flags a,w,x en .section"],
    },
}
