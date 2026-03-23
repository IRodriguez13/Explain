# Cápsulas didácticas (--man / --man-all) para lenguajes fuera de la familia C.
# Claves = regex exactas de explain/patterns/*.py (mismo string que la clave del dict de patrones).

from __future__ import annotations

from typing import Any

from explain.capsules.csharp_capsules import CAPSULES_CSHARP_HANDWRITTEN
from explain.capsules.js_priority_capsules import CAPSULES_JS_PRIORITY
from explain.capsules.python_priority_capsules import CAPSULES_PYTHON_PRIORITY
from explain.capsules.rust_capsules import CAPSULES_RUST_HANDWRITTEN

# --- Python (vanilla + warnings) ---
CAPSULES_PYTHON_EXTRA: dict[str, dict[str, Any]] = {
    r"NameError: name '.*' is not defined": {
        "codigo_incorrecto": """def main():
    print(x)  # x nunca se definió en este scope

main()""",
        "codigo_correcto": """x = 42

def main():
    print(x)

main()""",
        "que_paso": (
            "Python evalúa `x` y no encuentra un nombre enlazado en el scope actual "
            "(local, luego global, luego builtins). Suele ser un typo, falta de `import`, "
            "o usar una variable antes de asignarla en la misma función."
        ),
        "regla": "Definí o importá el nombre antes de usarlo; en funciones, asigná antes de leer si no usás `global`/`nonlocal` a propósito.",
    },
    r"KeyError:": {
        "codigo_incorrecto": """d = {"a": 1}
v = d["clave_inexistente"]""",
        "codigo_correcto": """d = {"a": 1}
v = d.get("clave_inexistente", None)
# o: if "clave_inexistente" in d: v = d["clave_inexistente"]""",
        "que_paso": (
            "Accedés a `dict[k]` con una clave que no está en el diccionario. "
            "A diferencia de `.get()`, el subíndice lanza `KeyError`."
        ),
        "regla": "Usá `.get(k, default)`, `k in d`, o manejá la ausencia con try/except según el contrato de tu API.",
    },
    r"IndentationError:": {
        "codigo_incorrecto": """def f():
print("mal")  # sin indentar bajo def""",
        "codigo_correcto": """def f():
    print("bien")""",
        "que_paso": (
            "Los bloques (`def`, `if`, `for`, `class`, etc.) exigen una nueva línea indentada. "
            "Mezclar tabs y espacios también provoca errores de indentación."
        ),
        "regla": "Mantené una sola convención (recomendado: 4 espacios por nivel) y alineá todo el bloque.",
    },
    r"TypeError:.*takes .* positional argument": {
        "codigo_incorrecto": """def saluda(nombre, titulo):
    print(nombre, titulo)

saluda("Ana")  # falta un argumento""",
        "codigo_correcto": """def saluda(nombre, titulo=""):
    print(nombre, titulo)

saluda("Ana")
saluda("Ana", "Ing.")""",
        "que_paso": (
            "La llamada no coincide con la firma: demasiados o muy pocos argumentos posicionales. "
            "En métodos de instancia, el primer parámetro suele ser `self`."
        ),
        "regla": "Compará la llamada con `def` (o la documentación); usá valores por omisión o argumentos nombrados.",
    },
    r"AttributeError:.*has no attribute": {
        "codigo_incorrecto": """s = "hola"
s.append("!")  # str no tiene append""",
        "codigo_correcto": """s = "hola"
s = s + "!"
# o lista: items = []; items.append("!")""",
        "que_paso": (
            "El objeto no expone ese nombre de atributo o método. A veces es typo, "
            "a veces el objeto es `None` y el error aparece como falta de atributo."
        ),
        "regla": "Verificá el tipo real (`type(x)`, `repr`), la documentación del tipo, y que no sea `None`.",
    },
    r"DeprecationWarning:": {
        "codigo_incorrecto": """import warnings
warnings.warn("api vieja", DeprecationWarning)
# consumo de API marcada obsoleta en la lib""",
        "codigo_correcto": """# migrar a la API recomendada en el mensaje o en la doc de la versión actual""",
        "que_paso": (
            "Una API que usás está marcada para eliminación o cambio en versiones futuras. "
            "El warning no detiene la ejecución pero conviene planificar el cambio."
        ),
        "regla": "Leé el texto del warning y la documentación de la versión; actualizá código o fijá una fecha de migración.",
    },
    r"UnboundLocalError:": {
        "codigo_incorrecto": """x = 1
def f():
    print(x)
    x = 2  # Python trata x como local en toda la función
f()""",
        "codigo_correcto": """x = 1
def f():
    global x
    print(x)
    x = 2""",
        "que_paso": (
            "Si asignás a un nombre en una función, Python lo marca como local en **toda** la función; "
            "un `print(x)` antes de la asignación falla."
        ),
        "regla": "Reordená (asigná antes de leer), usá `global`/`nonlocal` si corresponde, o otro nombre.",
    },
    r"SyntaxError: invalid syntax": {
        "codigo_incorrecto": """def f()
    pass""",
        "codigo_correcto": """def f():
    pass""",
        "que_paso": (
            "El parser no puede armar el AST: falta `:`, paréntesis, o el error real está en la línea anterior."
        ),
        "regla": "Revisá `def`/`if`/`for`/`class` con `:`; en f-strings y expresiones anidadas mirá el contexto completo.",
    },
    r"SyntaxError:.*EOL|unterminated string": {
        "codigo_incorrecto": """msg = "hola
mundo" """,
        "codigo_correcto": """msg = "hola\\nmundo"
# o triple comillas \"\"\" ... \"\"\" """,
        "que_paso": "Cadena literal sin cerrar o salto de línea dentro de comillas simples/dobles no escapado.",
        "regla": "Cerrá comillas; usá `\\n`, triple-quoted strings o raw strings (`r\"...\"`) según backslashes.",
    },
    r"TabError:": {
        "codigo_incorrecto": "# Mezcla de tab y espacios en el mismo bloque (ilegal en Python 3)",
        "codigo_correcto": "# Convertí el archivo a solo espacios (p. ej. editor: 'Indent using spaces')",
        "que_paso": "Indentación mezcla tabs y espacios de forma inconsistente.",
        "regla": "Elegí una sola convención; PEP 8 recomienda espacios.",
    },
    r"TypeError: unsupported operand type": {
        "codigo_incorrecto": """n = 3
s = "x"
print(n + s)""",
        "codigo_correcto": """n = 3
s = "x"
print(str(n) + s)""",
        "que_paso": "El operador no está definido para esa pareja de tipos (p. ej. int + str sin conversión).",
        "regla": "Convertí explícitamente o cambiá el diseño; no confundas `+` entre listas vs entre tipos distintos.",
    },
    r"TypeError:.*not callable": {
        "codigo_incorrecto": """x = 3
x()""",
        "codigo_correcto": """def x():
    pass
x()""",
        "que_paso": "Usás `()` sobre un objeto que no es función/clase callable (a veces pisaste el nombre de una función).",
        "regla": "Verificá qué es realmente el nombre (`print(repr(x))`) y no llames si es un dato.",
    },
    r"TypeError:.*must be str|not bytes": {
        "codigo_incorrecto": """b = b"hi"
print("msg: " + b)""",
        "codigo_correcto": """b = b"hi"
print("msg: " + b.decode("utf-8"))""",
        "que_paso": "Mezclás `str` y `bytes` en una operación que exige un solo tipo de texto.",
        "regla": "Decodificá bytes a str o codificá str a bytes con encoding explícito.",
    },
    r"IndexError:.*out of range|list index out of range": {
        "codigo_incorrecto": """a = [1, 2]
print(a[5])""",
        "codigo_correcto": """a = [1, 2]
if len(a) > 5:
    print(a[5])""",
        "que_paso": "Índice ≥ len o índice negativo fuera de rango en secuencia.",
        "regla": "Comprobá `len`, usá slicing seguro, o `.get` en estructuras adecuadas.",
    },
    r"ValueError:": {
        "codigo_incorrecto": """int("12a")""",
        "codigo_correcto": """int("12")""",
        "que_paso": "El tipo es razonable pero el valor no (conversión, desempaquetado, dominio del problema).",
        "regla": "Validá entrada; leé el mensaje (suele decir qué valor falló).",
    },
    r"ZeroDivisionError:": {
        "codigo_incorrecto": """x = 0
print(1 / x)""",
        "codigo_correcto": """x = 0
print(1 / x if x != 0 else float("inf"))""",
        "que_paso": "División entera o flotante o `%` con divisor cero.",
        "regla": "Guardá con `if d != 0` o manejá el caso de negocio antes de dividir.",
    },
    r"ModuleNotFoundError: No module named": {
        "codigo_incorrecto": """import paquete_inexistente""",
        "codigo_correcto": """# pip install paquete
import requests""",
        "que_paso": (
            "El intérprete no encuentra el paquete en sys.path (venv equivocado, nombre distinto en PyPI, o typo)."
        ),
        "regla": "Activá el venv correcto, `pip install`, y verificá nombre del import vs nombre del paquete.",
    },
    r"ImportError: cannot import name": {
        "codigo_incorrecto": """from os import no_existe""",
        "codigo_correcto": """from os import path""",
        "que_paso": "El módulo existe pero no exporta ese símbolo (versión distinta, typo, o API renombrada).",
        "regla": "Inspeccioná `dir(modulo)`, la doc de la versión instalada, o importá el módulo y usá `modulo.attr`.",
    },
    r"ImportError: attempted relative import": {
        "codigo_incorrecto": "# Ejecutás directamente un archivo que hace from .sub import x",
        "codigo_correcto": "# python -m paquete.modulo desde la raíz del proyecto",
        "que_paso": "Import relativo (`from .`) solo tiene sentido dentro de un paquete; al correr el .py como script falla.",
        "regla": "Usá `python -m`, estructura con `__init__.py` (si aplica), o imports absolutos desde la raíz en PYTHONPATH.",
    },
    r"FileNotFoundError:": {
        "codigo_incorrecto": """open("datos.csv")  # archivo no está en cwd""",
        "codigo_correcto": """from pathlib import Path
p = Path(__file__).parent / "datos.csv"
open(p)""",
        "que_paso": "La ruta no existe desde el directorio de trabajo actual o la ruta relativa es incorrecta.",
        "regla": "Usá rutas absolutas o `Path` relativas al archivo; comprobá `exists()` antes.",
    },
    r"json\.JSONDecodeError|Expecting value": {
        "codigo_incorrecto": """import json
json.loads("")""",
        "codigo_correcto": """import json
json.loads("{}")""",
        "que_paso": "El texto no es JSON válido (vacío, HTML de error, coma final, encoding corrupto).",
        "regla": "Imprimí/revisá el string crudo; validá con linter; `loads` vs `load` del archivo correcto.",
    },
    r"RecursionError: maximum recursion depth": {
        "codigo_incorrecto": """def f():
    return f()
f()""",
        "codigo_correcto": """def f(n):
    if n <= 0:
        return 0
    return n + f(n - 1)""",
        "que_paso": "Recursión sin caso base o profundidad desmedida para el límite de Python.",
        "regla": "Añadí caso base; preferí bucle para profundidad grande; `sys.setrecursionlimit` solo si sabés el riesgo.",
    },
    r"RuntimeError:.*asyncio|Event loop is closed": {
        "codigo_incorrecto": "# Llamás asyncio.run() anidado o usás loop cerrado desde otro hilo",
        "codigo_correcto": """import asyncio
async def main():
    await asyncio.sleep(0)
asyncio.run(main())""",
        "que_paso": "El event loop ya se cerró o hay mezcla de loops entre hilos / múltiples `run` incorrectos.",
        "regla": "Un solo `asyncio.run(main())` en programa; en libs async usá `await` coherente sin cerrar el loop prematuramente.",
    },
    r"ResourceWarning:": {
        "codigo_incorrecto": """f = open("x.txt")
# olvidás f.close() — el GC puede avisar ResourceWarning""",
        "codigo_correcto": """with open("x.txt") as f:
    data = f.read()""",
        "que_paso": "Archivo, socket u otro recurso no cerrado explícitamente (a veces visible con `-W default`).",
        "regla": "Usá `with` / context managers; cerrá en `finally` si manejás a mano.",
    },
    r"UserWarning:": {
        "codigo_incorrecto": """import warnings
warnings.warn("revisa esto", UserWarning)""",
        "codigo_correcto": "# Corregí la condición que la librería te marca; o filtrá el warning solo en tests si es conocido.",
        "que_paso": "Una biblioteca o tu código emitió `UserWarning` (no es error, pero indica uso dudoso).",
        "regla": "Leé el mensaje y la documentación; no silencies sin entender.",
    },
}

# --- Python frameworks (subset) ---
CAPSULES_PYTHON_FW_EXTRA: dict[str, dict[str, Any]] = {
    r"django\.urls\.exceptions\.NoReverseMatch": {
        "codigo_incorrecto": """# urls.py: path('items/', views.lista, name='item_list')
from django.urls import reverse
reverse('item-lst')  # nombre mal escrito""",
        "codigo_correcto": """reverse('item_list')
# reverse('app:item_list')  # si usás namespace en include()""",
        "que_paso": (
            "Django no encuentra una ruta con ese `name`, o faltan kwargs obligatorios "
            "para construir la URL (p. ej. pk)."
        ),
        "regla": "Verificá el string de `name=` en `path()`/`re_path()`, namespaces y los kwargs que pide la ruta.",
    },
    r"rest_framework\.exceptions\.|rest_framework\.serializers\.ValidationError": {
        "codigo_incorrecto": """# Serializer con campo obligatorio; POST sin ese campo → 400 ValidationError""",
        "codigo_correcto": """# Enviá todos los campos required; o marcalos read_only/required=False con criterio.""",
        "que_paso": (
            "DRF rechazó datos: serializer, parser o permiso devolvió error de validación. "
            "El cuerpo de respuesta suele detallar el campo."
        ),
        "regla": "Inspeccioná `serializer.errors` en la vista o la respuesta JSON; alineá el payload con el serializer.",
    },
    r"django\.core\.exceptions\.ImproperlyConfigured": {
        "codigo_incorrecto": """# INSTALLED_APPS con string mal escrito o variable de entorno faltante en settings""",
        "codigo_correcto": """# Revisá settings.py: INSTALLED_APPS, MIDDLEWARE, DATABASES y variables que leés con os.environ""",
        "que_paso": "Django detectó configuración inválida al arrancar o al cargar apps.",
        "regla": "Seguí el traceback: suele indicar qué setting o app falló; contrastá con un proyecto `django-admin startproject` limpio.",
    },
    r"django\.core\.exceptions\.ValidationError": {
        "codigo_incorrecto": """# Model.clean() o Form.is_valid() == False sin manejar errores""",
        "codigo_correcto": """# if form.is_valid(): ... else: return render con form.errors""",
        "que_paso": "Datos no pasaron validación de modelo, formulario o campo.",
        "regla": "Inspeccioná `error_dict` / `form.errors`; alineá el POST con campos required y validators.",
    },
    r"\.DoesNotExist:\s*$|DoesNotExist:\s|matching query does not exist": {
        "codigo_incorrecto": """obj = MyModel.objects.get(pk=999)  # no hay fila""",
        "codigo_correcto": """obj = get_object_or_404(MyModel, pk=999)
# o: MyModel.objects.filter(pk=999).first()""",
        "que_paso": "`get()` exige exactamente una fila; si no hay ninguna, lanza DoesNotExist.",
        "regla": "Usá `get_object_or_404`, `filter().first()`, o `try/except Model.DoesNotExist` según el flujo.",
    },
    r"django\.db\.utils\.IntegrityError": {
        "codigo_incorrecto": """# Dos filas con mismo unique=True; o FK a id inexistente""",
        "codigo_correcto": """# Validá antes de save; usá get_or_create; revisá migraciones y constraints""",
        "que_paso": "La BD rechazó la operación: UNIQUE, FOREIGN KEY, CHECK, etc.",
        "regla": "Leé el mensaje SQL del error; corregí datos duplicados o referencias rotas; usá transacciones atómicas.",
    },
    r"werkzeug\.routing\.exceptions\.(NotFound|BuildError|MethodNotAllowed)": {
        "codigo_incorrecto": """# url_for('vista_inexistente') o GET a ruta solo POST""",
        "codigo_correcto": """# Registrá @app.route con el mismo endpoint; pasá todos los args a url_for""",
        "que_paso": "Flask/Werkzeug: ruta no registrada, `url_for` sin endpoint, o método HTTP no permitido.",
        "regla": "Listá rutas (`flask routes`); unificá nombres de endpoint y `methods=[...]` en la vista.",
    },
    r"fastapi\.exceptions\.(HTTPException|RequestValidationError|WebSocketRequestValidationError)": {
        "codigo_incorrecto": """# Body JSON no cumple el modelo Pydantic del parámetro""",
        "codigo_correcto": """# Ajustá el schema; en 422 mirá el detalle en /docs (OpenAPI) o response body""",
        "que_paso": "Lanzaste `HTTPException` o FastAPI rechazó query/body/WebSocket según el modelo.",
        "regla": "Para 422: revisá `RequestValidationError` en logs; alineá tipos, Optional y campos requeridos.",
    },
    r"pydantic_core\._pydantic_core\.ValidationError|pydantic\.error_wrappers\.ValidationError": {
        "codigo_incorrecto": """from pydantic import BaseModel
class M(BaseModel):
    n: int
M.model_validate({"n": "no"})""",
        "codigo_correcto": """from pydantic import BaseModel
class M(BaseModel):
    n: int
M.model_validate({"n": 1})""",
        "que_paso": "Los datos no encajan en el modelo (tipos, rangos, campos extra prohibidos).",
        "regla": "En v2 usá `.model_validate` y leé `e.errors()`; revisá `model_config` y `Optional`/`Annotated`.",
    },
    r"sqlalchemy\.exc\.IntegrityError": {
        "codigo_incorrecto": """# session.add(obj duplicado unique); commit() → IntegrityError""",
        "codigo_correcto": """# merge / get primero; session.rollback(); corregí datos antes de reintentar""",
        "que_paso": "El driver SQL devolvió violación de restricción al hacer flush/commit.",
        "regla": "Inspeccioná el texto SQL del error; validá unicidad y FKs antes de persistir.",
    },
    r"jinja2\.(exceptions\.|TemplateError|TemplateSyntaxError|UndefinedError)": {
        "codigo_incorrecto": """{# {{ variable_inexistente }} sin pasarla al render #}""",
        "codigo_correcto": """{# render_template("x.html", variable_inexistente=valor) #}""",
        "que_paso": "Sintaxis de plantilla, variable no definida, o error al evaluar filtro/macro.",
        "regla": "Pasá todas las variables al `Environment`/`render`; revisá bloques `{% %}` y filtros `|`.",
    },
    r"uvicorn\.errors\.|ERROR:.*\[uvicorn\]|Failed to start uvicorn": {
        "codigo_incorrecto": """# Puerto 8000 ocupado o import app falla en factory ASGI""",
        "codigo_correcto": """# uvicorn main:app --port 8001  # o arreglá el ImportError en el traceback""",
        "que_paso": "No pudo enlazar el socket o falló al importar/cargar la aplicación ASGI.",
        "regla": "Leé el traceback completo; probá otro puerto; verificá `module:attr` del target.",
    },
}

# --- JavaScript / TypeScript (vanilla) ---
CAPSULES_JS_EXTRA: dict[str, dict[str, Any]] = {
    r"TS2322:|not assignable to type": {
        "codigo_incorrecto": """let x: string = 123;""",
        "codigo_correcto": """let x: string = String(123);
// o: let x: number = 123;""",
        "que_paso": (
            "TypeScript no puede asignar el valor al tipo anotado. Suele ser un desajuste entre "
            "lo que devuelve una función y lo que declaraste."
        ),
        "regla": "Ajustá el tipo, estrechá con guards (`typeof`, `in`), o corregí la fuente del valor; evitá `as` solo para silenciar.",
    },
    r"TS2307:|Cannot find module": {
        "codigo_incorrecto": """import { z } from "no-existe";""",
        "codigo_correcto": """// npm install paquete
import { z } from "zod";""",
        "que_paso": (
            "El resolvedor no encuentra el módulo: paquete no instalado, path mal escrito, "
            "o configuración `moduleResolution` / extensiones `.js` en ESM."
        ),
        "regla": "Instalá dependencias, revisá `tsconfig` paths/baseUrl, y extensiones en imports relativos si usás NodeNext.",
    },
    r"TS2339:|Property .* does not exist on type": {
        "codigo_incorrecto": """type U = { id: number };
const u: U = { id: 1 };
console.log(u.nombre);""",
        "codigo_correcto": """type U = { id: number; nombre?: string };
const u: U = { id: 1 };
console.log(u.nombre ?? "");""",
        "que_paso": "El tipo estático no declara esa propiedad (typo, API distinta, o valor `any`/`unknown` mal usado).",
        "regla": "Corregí el nombre, usá optional chaining `?.`, o extendé el tipo/interfaz con criterio.",
    },
    r"TS2554:|Expected .* arguments, but got": {
        "codigo_incorrecto": """function f(a: number, b: number) {}
f(1);""",
        "codigo_correcto": """function f(a: number, b: number = 0) {}
f(1);""",
        "que_paso": "Menos o más argumentos de los que la firma declara (incluye opcionales y sobrecargas).",
        "regla": "Completá args, poné defaults en la definición, o elegí la sobrecarga correcta.",
    },
    r"TS2532:|Object is possibly 'undefined'|Object is possibly 'null'": {
        "codigo_incorrecto": """let x: string | undefined;
console.log(x.length);""",
        "codigo_correcto": """let x: string | undefined;
if (x) console.log(x.length);
// o: console.log(x?.length);""",
        "que_paso": "Con `strictNullChecks`, podría ser `null`/`undefined` y no podés acceder a miembros sin comprobar.",
        "regla": "Guardas (`if`, `?.`, discriminantes); `!` solo si tenés garantía real.",
    },
    r"ReferenceError:\s*": {
        "codigo_incorrecto": """console.log(noDeclarada);""",
        "codigo_correcto": """const noDeclarada = 1;
console.log(noDeclarada);""",
        "que_paso": "En runtime el identificador no existe en el scope (TDZ con `let`, typo, o script sin módulo).",
        "regla": "Declará antes de usar; en módulos ESM usá import/export; en browser revisá orden de `<script>`.",
    },
    r"TypeError: Cannot read propert(y|ies) of (undefined|null)": {
        "codigo_incorrecto": """const u = undefined;
console.log(u.algo);""",
        "codigo_correcto": """const u = { algo: 1 };
console.log(u?.algo);""",
        "que_paso": "Accedés a una propiedad de `undefined` o `null` (cadena de accesos sin valor intermedio).",
        "regla": "Usá optional chaining `?.`, valores por defecto, o validá antes de leer.",
    },
    r"TypeError:.*is not a function": {
        "codigo_incorrecto": """const x = 3;
(x as any)();""",
        "codigo_correcto": """function x() {}
x();""",
        "que_paso": "Llamás como función algo que no lo es (default export mal importado, typo, o dato en vez de callback).",
        "regla": "Verificá `typeof fn === 'function'`; en CJS/ESM unificá default vs named import.",
    },
    r"MODULE_NOT_FOUND|Error: Cannot find module": {
        "codigo_incorrecto": """const m = require("paquete-que-no-esta");""",
        "codigo_correcto": """// npm install paquete-que-no-esta
const m = require("paquete-que-no-esta");""",
        "que_paso": "Node no resolvió el módulo (node_modules, path, o `exports` del package.json).",
        "regla": "`npm i`, revisá mayúsculas en Linux, y `type: module` vs `require`.",
    },
    r"UnhandledPromiseRejection|unhandled rejection": {
        "codigo_incorrecto": """async function f() { throw new Error("x"); }
f(); // sin await ni .catch()""",
        "codigo_correcto": """async function f() { throw new Error("x"); }
f().catch((e) => console.error(e));
// o: void (async () => { await f(); })();""",
        "que_paso": "Una promesa rechazada no tuvo `.catch()` ni `try/await` en un async caller.",
        "regla": "Siempre encadená `.catch` o usá try/finally con await; en event handlers no dejes promesas flotando.",
    },
}

# --- JavaScript frameworks ---
CAPSULES_JS_FW_EXTRA: dict[str, dict[str, Any]] = {
    r"Hydration failed|hydration mismatch|did not match|Hydration.*error": {
        "codigo_incorrecto": """// SSR: HTML con fecha/ID aleatorio; cliente render distinto
export default function Page() {
  return <div>{Date.now()}</div>;
}""",
        "codigo_correcto": """// Mismo árbol servidor y cliente en 1er render; datos aleatorios en useEffect o suppressHydrationWarning puntual
"use client";
import { useEffect, useState } from "react";
export default function Page() {
  const [t, setT] = useState<number | null>(null);
  useEffect(() => setT(Date.now()), []);
  return <div>{t ?? "…"}</div>;
}""",
        "que_paso": (
            "React en el cliente esperaba el mismo resultado que el HTML generado en el servidor. "
            "Cualquier diferencia (hora, random, locale, extensiones del navegador) rompe la hidratación."
        ),
        "regla": "Hacé determinístico el primer render; mové lo no determinístico a `useEffect` o cargá solo en cliente.",
    },
    r"Invalid hook call|Hooks can only be called": {
        "codigo_incorrecto": """// Hook dentro de if o fuera de componente
if (cond) {
  const [x, setX] = useState(0);
}""",
        "codigo_correcto": """function C({ cond }: { cond: boolean }) {
  const [x, setX] = useState(0);
  if (!cond) return null;
  return <button onClick={() => setX(x + 1)}>{x}</button>;
}""",
        "que_paso": (
            "Los Hooks deben llamarse en el mismo orden en cada render, solo en el nivel superior "
            "de un componente funcional o custom hook. También falla si hay dos copias de `react` en node_modules."
        ),
        "regla": "No condiciones/loops alrededor de hooks; resolvé duplicados de React en monorepo (`npm dedupe`, aliases).",
    },
    r"Maximum update depth exceeded|Too many re-renders": {
        "codigo_incorrecto": """// setState en render o useEffect sin deps que vuelve a disparar el mismo setState
useEffect(() => setCount(c => c + 1));""",
        "codigo_correcto": """useEffect(() => {
  setCount(1);
}, []); // deps correctas: solo cuando debe correr""",
        "que_paso": "React entró en un ciclo: cada render o efecto dispara un estado nuevo que vuelve a renderizar al infinito.",
        "regla": "No actualices estado durante el render puro; en `useEffect` poné dependencias completas y estables (`useCallback`).",
    },
    r"\[vite\].*Failed to resolve|Could not resolve.*from|Rollup failed to resolve": {
        "codigo_incorrecto": """// import Foo from "foo" pero el paquete no está instalado o el alias falla""",
        "codigo_correcto": """// npm i foo; o en vite.config: resolve.alias { "@": path.resolve(__dirname, "src") }""",
        "que_paso": "Vite/Rollup no pudo resolver el specifier a un archivo en disco.",
        "regla": "Instalá deps, configurá `alias`, y en monorepos `server.fs.allow` / `optimizeDeps.include` si aplica.",
    },
    r"PrismaClientKnownRequestError|P20\d{2}:|PrismaClientValidationError|PrismaClientInitializationError": {
        "codigo_incorrecto": """// prisma.user.create({ data: { email: duplicado } }) → P2002""",
        "codigo_correcto": """// upsert o manejo de unique; DATABASE_URL correcta para InitializationError""",
        "que_paso": "Prisma mapeó un fallo de BD (código P20xx), validación del cliente, o conexión/schema (`prisma generate`).",
        "regla": "Buscá el código P20xx en prisma.io/docs; `npx prisma migrate dev` y `generate` tras cambios de schema.",
    },
    r"Error occurred prerendering|prerender.*error|NEXT_RUNTIME|next/dist": {
        "codigo_incorrecto": """// getStaticProps lanza o fetch en build falla sin try/catch""",
        "codigo_correcto": """// Manejo de error en datos; o marcá la ruta como dynamic si no puede SSG""",
        "que_paso": "Next falló en build o request al prerenderizar (SSG/RSC según versión).",
        "regla": "Leé la página/archivo en el stack; probá `next dev`; usá `dynamic = 'force-dynamic'` solo si corresponde.",
    },
    r"only works in a Client Component|You're importing a component that needs (useEffect|useState|useRef)": {
        "codigo_incorrecto": """// Server Component importa hijo que usa useState sin 'use client'""",
        "codigo_correcto": """'use client';
import { useState } from "react";
export function Cliente() { ... }""",
        "que_paso": "En App Router, el servidor no puede ejecutar hooks; el módulo debe ser Client Component.",
        "regla": "Poné `'use client'` en el archivo que usa estado/efectos o mové esa parte a un hijo cliente.",
    },
    r"NG\d+:|angular.*compiler.*error|Error occurs in the template of component": {
        "codigo_incorrecto": """<!-- template: propiedad mal escrita o pipe inexistente -->""",
        "codigo_correcto": """<!-- corregí binding, imports del standalone component, strictTemplates -->""",
        "que_paso": "El compilador AOT o el template del componente reportó NGxxxx o error de enlace.",
        "regla": "Buscá NGxxxx en angular.io/errors; revisá `imports` del componente standalone y tipos en plantilla.",
    },
}

HANDWRITTEN_BY_LANG: dict[str, dict[str, dict[str, Any]]] = {
    "Python": {**CAPSULES_PYTHON_EXTRA, **CAPSULES_PYTHON_PRIORITY, **CAPSULES_PYTHON_FW_EXTRA},
    "JavaScript": {**CAPSULES_JS_EXTRA, **CAPSULES_JS_PRIORITY, **CAPSULES_JS_FW_EXTRA},
    "Rust": dict(CAPSULES_RUST_HANDWRITTEN),
    "C#": dict(CAPSULES_CSHARP_HANDWRITTEN),
}

__all__ = ["HANDWRITTEN_BY_LANG"]
