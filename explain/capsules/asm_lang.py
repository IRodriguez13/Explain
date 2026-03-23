# Cápsulas --man para explain/patterns/assembly.py y assembly_warnings.py (claves regex idénticas).

from __future__ import annotations

from typing import Any


def _a(
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


# gas/clang AT&T x86-64 de ejemplo; ARM/A64 en comentarios cuando el mensaje es multi-ISA.
CAPSULES_ASM_HANDWRITTEN: dict[str, dict[str, Any]] = {
    r"Error: no such instruction|invalid instruction mnemonic|bad instruction|unknown opcode": _a(
        """# x86-64 AT&T
movxq %rax, %rbx   # mnemónico inventado / typo""",
        """movq %rax, %rbx
# o: revisá .arch / -march para ARM (p. ej. vadd en CPU sin NEON)""",
        "El backend no reconoce el mnemónico o no existe en el modo CPU (-m32 vs -m64, ARM vs Thumb, etc.).",
        "Compará con el manual de la ISA; unificá sintaxis AT&T vs Intel (.intel_syntax); ajustá -march=/-mcpu=.",
    ),
    r"operand size mismatch|incorrect operand|operand type mismatch|mismatch between operand sizes": _a(
        """movl %eax, %rax   # mezcla 32/64 mal según modo y sintaxis""",
        """movq %rax, %rbx
# ARM: cuidado W vs X (32 vs 64 bits) en A64""",
        "Los operandos no encajan en ancho (8/16/32/64) o registro vs memoria incompatible.",
        "Usá sufijos explícitos en AT&T (b/w/l/q); en A64 elegí Wn o Xn coherentemente.",
    ),
    r"relocation truncated to fit|relocation R_|cannot apply relocation|relocation out of range": _a(
        """jmp etiqueta_muy_lejana   # salto relativo que no cabe en el campo""",
        """# cadena de saltos, thunk/veneer, o -fPIC / modelo de código medio/grande
# ARM: B + BL intermedio según alcance""",
        "La relocalización o el offset de branch no cabe (PIC, distancia, modelo de código).",
        "Revisá -fPIC, thunks del linker, y límites de branch en el manual (x86/ARM/A64).",
    ),
    r"undefined symbol|undefined local symbol|undefined reference.*\.s:": _a(
        """call funcion_externa
# sin .globl ni .o que la defina""",
        """.globl mi_simbolo
mi_simbolo:
  ret
# o linkeá el .o que define la etiqueta""",
        "La etiqueta o símbolo externo no está definido en esta unidad ni resuelto en el enlace.",
        "Declará `.globl` / `.weak` según corresponda; incluí todos los .o en el comando de ld/gcc.",
    ),
    r"expected comma|parse error|syntax error.*\.s|junk at end of line": _a(
        """movq %rax %rbx   # falta coma en AT&T entre operandos""",
        """movq %rax, %rbx""",
        "Sintaxis gas: orden AT&T `op src, dst`, comas, o basura al final de línea.",
        "Consultá la sintaxis de tu arquitectura; comentarios `#` y continuaciones de línea.",
    ),
    r"can't open.*for reading|Assembler messages": _a(
        """# as boot.s  pero el archivo está en src/boot.s""",
        """as -o boot.o src/boot.s""",
        "No se encontró el .s o la ruta en el Makefile/cmake es incorrecta.",
        "Verificá cwd, rutas relativas y dependencias del build.",
    ),
    r"macro.*redefinition|endm|\.macro": _a(
        """.macro foo
nop
.macro foo
nop
.endm""",
        """.macro foo
nop
.endm""",
        "Macro duplicada o `.endm` faltante / desbalanceado.",
        "Un nombre por macro; cerrá con `.endm`; evitá incluir dos veces la misma definición.",
    ),
    r"\.type|\.size|STT_FUNC": _a(
        """.type main, @object   # tipo incorrecto para una función""",
        """.type main, @function
.size main, .-main""",
        "Las directivas `.type`/`.size` describen el símbolo para ELF y depuración.",
        "Para función: `@function`; tamaño `.size nombre, .-nombre` tras el cuerpo.",
    ),
    r"LLVM-MC|llvm-as|clang:.*error:.*\.s:": _a(
        """# mismo .s pero clang -cc1as es más estricto que gas en algún detalle""",
        """# probá: clang -c -fno-integrated-as archivo.s  # usar gas
# o corregí según el mensaje de columna que da MC""",
        "Clang usa el ensamblador integrado LLVM-MC; el diagnóstico puede diferir de gas.",
        "Alineá triple/tune flags; compará con gas o simplificá la línea que marca el error.",
    ),
    r"bad register name|unknown register|invalid register.*%e|%invalid.*32-bit mode": _a(
        """movl %rax, %ebx   # %rax no existe en modo IA-32""",
        """movl %eax, %ebx   # en -m32""",
        "Nombre de registro inválido para el modo (p. ej. RAX en 32 bits).",
        "En IA-32 usá EAX–EDI; en x86-64 podés usar R8–R15; revisá el modo del objeto.",
    ),
    r"not supported in 32-bit mode|invalid.*in 32-bit|32-bit mode.*64-bit operand|only supported in 64-bit mode": _a(
        """pushq %rax   # en objeto ensamblado como i386""",
        """# ensamblá con -m64 o usá pushl en .code32""",
        "Instrucción u operando de 64 bits en ensamblado de 32 bits (o conflicto inverso).",
        "Unificá el target: `gcc -m64` / `.code64` o reescribí con instrucciones de 32 bits.",
    ),
    r"RIP-relative|RIP addressing|invalid.*rip|%rip": _a(
        """# en -m32:  movl etiqueta(%eip), %eax  # RIP-relative no aplica igual""",
        """# en x86-64:  movq etiqueta(%rip), %rax""",
        "RIP-relative es propio de x86-64; en 32 bits se usa otro modelo (GOT, etc.).",
        "Compilá como 64 bits si necesitás `%rip`; en 32 bits usá tabla GOT o direccionamiento válido.",
    ),
    r"push.*64-bit|pop.*64-bit.*32|stack.*32-bit.*pushq": _a(
        """# mezcla pushl/pushq rompiendo alineación o ABI""",
        """# mantené tamaño de stack coherente con el modo (l vs q) y la ABI Sys V""",
        "push/pop de tamaño incompatible con el modo de código o la convención de pila.",
        "Seguí la ABI: en x86-64 alineación 16 bytes antes de `call`; no mezcles q/l al azar.",
    ),
    r"red zone|stack must be aligned|16-byte align|ABI.*x86": _a(
        """# omitís alineación 16-byte antes de call a función variádica / SIMD""",
        """# prólogo que hace sub $8,%rsp ... call  # ajustá para múltiplo de 16 en el call""",
        "Sys V x86-64 exige RSP mod 16 == 0 en el instante del `call`; existe red zone bajo RSP.",
        "Revisá prólogos/epílogos generados o manuales; documentación ABI oficial.",
    ),
    r"xmm|ymm|zmm|SSE|AVX|requires.*SSE|requires.*AVX": _a(
        """vmovaps (%rax), %ymm0   # con -march sin AVX""",
        """# gcc -mavx2 -c ...   o sustituí por movaps SSE2""",
        "La instrucción SIMD no está permitida en el -march/-mcpu configurado.",
        "Subí el nivel de CPU (`-mavx2`, etc.) o reemplazá por secuencia compatible.",
    ),
    r"bad register name.*%r(8|9|1[0-5])\b|`r(8|9|1[0-5])'.*invalid|extended register.*32-bit|R8.*R15.*64-bit": _a(
        """movl %r8d, %eax   # en target i386 R8 no existe""",
        """# usá -m64 o registros EAX–EDI en 32 bits""",
        "R8–R15 son solo modo largo (x86-64).",
        "Ensamblá como x86_64 o evitá esos registros en código de 32 bits.",
    ),
    r"addressing mode.*invalid|invalid combination of prefixes|lock.*invalid": _a(
        """lock addl $1, (%esp)   # combinación no válida según modR/M""",
        """# simplificá el modo de direccionamiento; LOCK solo en ops atómicas admitidas""",
        "ModR/M o prefijos LOCK/REP no válidos para esa instrucción.",
        "Consultá manual Intel/AMD para la forma legal del operando.",
    ),
    r"selected processor does not support|instruction not supported|extension not supported.*arm": _a(
        """# .cpu cortex-m0 + instrucción que requiere ARMv7-M DSP""",
        """.cpu cortex-m4
# o bajá a instrucciones soportadas por el núcleo elegido""",
        "El perfil `.cpu`/`-mcpu` no incluye esa extensión (NEON, IDIV, etc.).",
        "Subí el perfil de CPU o reemplazá por secuencia portable documentada en ARM ARM.",
    ),
    r"cannot assemble.*in.*Thumb|Thumb-2|not supported in ARM state|BX.*Thumb": _a(
        """# mnemónico solo Thumb en estado ARM""",
        """.thumb
.thumb_func main
main:
  ...""",
        "Mezcla de estado ARM (A32) y Thumb (T32) sin transición correcta.",
        "Usá `.syntax unified`, `.thumb`/`.arm`, y BX con LSB correcto al cambiar estado.",
    ),
    r"conditional branch out of range|branch out of range|relocation.*ARM.*jump": _a(
        """b.eq destino_a_1MB   # B condicional de alcance limitado""",
        """# invertí condición + b lejano; o cadena de saltos; veneer del linker""",
        "El offset del branch relativo no cabe en el encoding.",
        "Técnicas: opuesto condicional + B sin condición, trampolines, o reorganizar código.",
    ),
    r"unpredictable|UNPREDICTABLE|deprecated instruction": _a(
        """# uso que el manual ARM marca UNPREDICTABLE (p. ej. PC como Rn en ciertos casos)""",
        """# reescribí con la secuencia recomendada en la documentación oficial""",
        "El manual declara resultado impredecible u obsoleto para ese encoding.",
        "No confíes en comportamiento; cambiá a la forma arquitecturalmente definida.",
    ),
    r"ldr.*literal|literal pool|out of range for.*literal": _a(
        """ldr r0, =constante_lejana
# sin .ltorg cercano""",
        """ldr r0, =label
.ltorg
# o movw/movt""",
        "La constante cargada vía literal pool queda demasiado lejos.",
        "Colocá `.ltorg` a tiempo; o usá movw/movt; acortá distancia PC→pool.",
    ),
    r"IT block|it instruction|Thumb.*IT": _a(
        """it eq
addeq r0, r1  # mal formado respecto al IT""",
        """itete
addeq r0, r1
subne r2, r3
# sintaxis IT correcta para el número de instrucciones condicionales""",
        "En Thumb-2 las instrucciones condicionales cortas van tras `IT`.",
        "Revisá ARM ARM: máscara IT y hasta 4 instrucciones siguientes.",
    ),
    r"(Error|error):.*aarch64|invalid operand.*aarch64|aarch64.*:.*(Error|error)|ARM64.*(Error|error)|unsupported.*for aarch64": _a(
        """mov x0, #0x1234567890ABCD  # inmediato ilegal de una sola instrucción""",
        """movz x0, #0xABCD, lsl 16
movk x0, #0x7890, lsl 32
# o cargá desde literal con adrp+add+ldr""",
        "A64 tiene reglas estrictas para inmediatos lógicos y tipos de operando.",
        "Descomponé con movz/movk/adrp; distinguí Wn (32) vs Xn (64).",
    ),
    r"immediate out of range|shift amount out of range|invalid shift": _a(
        """lsl x0, x1, #70   # shift fuera de ancho""",
        """lsl x0, x1, #3""",
        "El inmediato o la cantidad de desplazamiento no es encodable.",
        "Ajustá al rango del manual (ARM/x86); partí en varias instrucciones.",
    ),
    r"ADRP|adrp.*relocation|page out of range": _a(
        """adrp x0, simbolo_lejano
add x0, x0, :lo12:simbolo_lejano
# símbolo fuera de rango de página 4 KiB""",
        """# modelo de código/PIC; o tabla de GOT; o variante de acceso a datos""",
        "ADRP solo fija bits altos relativos a PC en páginas de 4 KiB; el símbolo puede estar fuera de alcance.",
        "Revisá `-fPIC`, distancia al símbolo, y pares adrp+add correctos.",
    ),
    r"(Error|error):.*\b(xzr|wzr)\b|invalid.*\bsp\b.*aarch64|same register.*sp.*xzr": _a(
        """add sp, sp, xzr, lsl #0   # combinación no permitida según instrucción""",
        """# usá add sp, sp, #imm legal o mov con registro permitido""",
        "SP y XZR/WZR tienen restricciones: no todas las ops aceptan SP como operando.",
        "Consultá la tabla de la instrucción en el manual A64.",
    ),
    r"Scalable Vector Extension|SVE.*not supported|predicate register p[0-9]+|unsupported SVE": _a(
        """ptrue p0.s
# toolchain o -mcpu sin SVE""",
        """# -march=armv8-a+sve o CPU con SVE; o evitá instrucciones SVE""",
        "SVE requiere CPU y binutils/clang con soporte explícito.",
        "Activá flags de arquitectura adecuados o mantené código NEON/ASIMD estándar.",
    ),
    r"section|\.section|changed section flags|alignment not a power": _a(
        """.section .text,"awx"   # flags incoherentes o typo""",
        """.section .text,"ax",@progbits
.balign 4""",
        "Directiva `.section`/`.align` mal formada o flags ELF inconsistentes.",
        "Revisá sintaxis gas: permisos a/w/x, @progbits, y potencias de 2 en alineación.",
    ),
    r"\.err encountered|Assembler message:.*\.err|user error.*assembler": _a(
        """.if 0
.err
.endif""",
        """# quitá .err o corregí la condición del .if/.macro""",
        "`.err` fuerza fallo de ensamblado (assert en macros).",
        "Ajustá la macro o la configuración que dispara `.err`.",
    ),
    r"TLS descriptor|TLS relocation|undefined reference.*__tls": _a(
        """# acceso a thread-local sin modelo TLS correcto en el enlace""",
        """# usá el modelo que espera el linker (-ftls-model); definí símbolos TLS según toolchain""",
        "Relocalización TLS o referencia a runtime TLS mal enlazada.",
        "Revisá `-pthread`, modelo inicial-exec/global-dynamic, y documentación del linker.",
    ),
    r"CFI directive|\.cfi_|dwarf CFI": _a(
        """.cfi_startproc
# olvidás .cfi_endproc""",
        """.cfi_startproc
  ...
.cfi_endproc""",
        "Las directivas Call Frame Information deben balancearse con el prólogo real.",
        "Preferí dejar que `gcc -S` genere CFI; si escribís a mano, seguí el manual `.cfi_*`.",
    ),
    # --- Warnings asm (misma clave que assembly_warnings.py) ---
    r"warning:.*shift count|Warning:.*shift": _a(
        """# desplazamiento con inmediato cuestionable según el ensamblador""",
        """# verificá rango vs ancho del operando; máscara explícita si es intencional""",
        "El conteo de bits del shift puede ser inválido o sospechoso para esa ISA.",
        "Contrastá con el manual; en código mezclado con C, shifts inválidos en C siguen siendo UB allí.",
    ),
    r"warning:.*implementation defined|warning:.*implementation-defined|Warning:.*unspecified": _a(
        """# construcción cuyo resultado depende del ensamblador o modo""",
        """# fijá .syntax unified / .code32/.code64 y probá en el hardware objetivo""",
        "No es siempre UB de C, pero el resultado puede variar por implementación.",
        "Documentá el modo y el target; no asumas comportamiento entre toolchains.",
    ),
    r"warning:.*end of file|Warning:.*end of file": _a(
        """/*
comentario sin cerrar""",
        """/* comentario cerrado */
# o cerrá .macro / cadenas""",
        "EOF inesperado: comentario, macro o string abierto.",
        "Cerrá `*/`, comillas y `.endm` antes del final del archivo.",
    ),
    r"warning:.*alignment|Warning:.*align|alignment larger than": _a(
        """.balign 65536""",
        """.balign 16""",
        "Alineación excesiva o incompatible con la sección.",
        "Usá valores razonables para la ISA y el linker script.",
    ),
    r"warning:.*signed overflow|overflow in expression": _a(
        """.word 0x7FFFFFFF + 1   # en evaluación del ensamblador""",
        """.word 0x80000000
# o tipo/ancho explícito""",
        "Constante o expresión en tiempo de ensamblado desborda.",
        "Partí en varias directivas o usá masking explícito.",
    ),
    r"warning:.*deprecated|Deprecated instruction|obsolete mnemonic": _a(
        """# mnemónico antiguo sugerido por el manual del fabricante""",
        """# sustituí por la forma recomendada que indica el mensaje""",
        "Instrucción marcada obsoleta; puede eliminarse en futuras versiones.",
        "Seguí la recomendación del warning o del manual actualizado.",
    ),
    r"warning:.*changing section|section flags.*changed": _a(
        """# el flujo del .s mueve código entre secciones de forma confusa""",
        """# orden explícito .text / .data; revisá permisos NX""",
        "Cambio de sección o flags; a veces informativo, a veces riesgo W^X.",
        "Revisá orden de `.section` y políticas de seguridad del binario.",
    ),
    r"warning:.*x86-64.*32-bit|32-bit.*x86-64|mismatch.*mode": _a(
        """.code32
# dentro de objeto pensado como x86-64""",
        """# unificá .code32/.code64 con el target del link final""",
        "Mezcla sospechosa de modos 32/64 bits.",
        "Alineá directivas con `-m32`/`-m64` del driver.",
    ),
    r"warning:.*AVX|SSE.*transition|vzeroupper": _a(
        """# rutina AVX mezclada con código SSE sin transición""",
        """# vzeroupper al salir de rutinas AVX hacia ABI que usa SSE legacy""",
        "Transición AVX↔SSE puede penalizar o fallar en algunas CPUs.",
        "Aislar rutinas SIMD o seguir guías de ABI del compilador/kernel.",
    ),
    r"warning:.*ARM.*Thumb|Thumb.*warning|unified syntax": _a(
        """# gas sugiere .syntax unified""",
        """.syntax unified
.thumb""",
        "Modo ARM vs Thumb y sintaxis unificada.",
        "Poné `.syntax unified` y `.thumb_func` en etiquetas de entrada cuando toque.",
    ),
    r"warning:.*literal pool|ltorg|pool may be out of range": _a(
        """# ldr =sym lejos sin .ltorg""",
        """.ltorg
# antes de saltos que alejan el PC del pool""",
        "El pool de literales puede quedar inalcanzable.",
        "Colocá `.ltorg` estratégicamente o reordená el flujo.",
    ),
    r"warning:.*aarch64|AArch64.*warning|Wn.*asm": _a(
        """# aviso genérico del front A64""",
        """# leé el texto completo; -Wa, o detalle de codificación""",
        "Clang/gas emitió advertencia específica de AArch64.",
        "Leé el mensaje completo; ajustá flags `-Wa` o el mnemónico señalado.",
    ),
    r"warning:.*indirect.*call|retpoline|spectre|speculation": _a(
        """# llamada indirecta sin thunk de mitigación en política estricta""",
        """# flags -mindirect-branch=thunk o guías de tu distro/kernel""",
        "Toolchain sugiere mitigación especulativa (retpoline, IBT, etc.).",
        "Seguí la documentación de seguridad del kernel o del proyecto.",
    ),
    r"note:.*while assembling|note:.*instantiated from": _a(
        """# nota de traza de macro/.include""",
        """# subí en el log al error real (línea citada arriba/abajo)""",
        "Nota contextual: macro o archivo incluido.",
        "Seguí la cadena de `.include`/`.macro` hasta el error raíz.",
    ),
    r"warning:.*suggest.*use of|warning:.*did you mean": _a(
        """mov %ax, %bx   # typo cercano a otro mnemónico""",
        """# aplicá la sugerencia del ensamblador o verificá el manual""",
        "Sugerencia de mnemónico u operando.",
        "Corregí según la sugerencia si es correcta para tu ISA.",
    ),
    r"warning:.*for subroutine|warning:.*stack frame": _a(
        """# desbalance aparente de marco de pila""",
        """# equilibrá push/pop; revisá ABI de la plataforma""",
        "Aviso sobre tamaño o forma del stack frame.",
        "Verificá prólogo/epílogo y alineación requerida por la ABI.",
    ),
}

__all__ = ["CAPSULES_ASM_HANDWRITTEN"]
