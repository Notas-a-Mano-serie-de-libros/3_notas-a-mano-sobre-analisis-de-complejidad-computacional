"""Ejemplos C visibles y conexión interna de sus entradas a WASI."""

import json
import re
import textwrap

try:
    from desarrollo.scripts.book_code_languages import translations
    from desarrollo.scripts.java_examples import example_key, format_java, java_example
except ModuleNotFoundError:
    from book_code_languages import translations
    from java_examples import example_key, format_java, java_example


def c_implementation(listing):
    f = listing["folio"]
    code = translations(listing)["C"]
    if f == 150:
        code = "#include <stdio.h>\n\nint sumar(int a, int b) {\n    return a + b;\n}"
    if f in (229, 234, 242, 167):
        code = re.sub(r"    if \(n < 0\) \{\n        abort\(\);\n    \}\n", "", code)
        code = re.sub(r"    if \(n > (12|46)\) \{\n        abort\(\);\n    \}\n", "", code)
    if f == 229:
        code = re.sub(r"int productoExacto\(.*?\n\}\n\n", "", code, flags=re.S)
        code = code.replace("productoExacto(n, factorial(n - 1))", "n * factorial(n - 1)")
    if f == 177:
        a = code.index("                int64_t producto =")
        b = code.index("\n            }", a)
        code = code[:a] + "                resultado[i][j] += a[i][k] * b[k][j];" + code[b:]
    if f == 278:
        code = code.replace("int64_t num = ((int64_t) b - a) * ((int64_t) x - arr[a]);", "int num = (b - a) * (x - arr[a]);").replace(
            "int64_t den = (int64_t) arr[b] - arr[a];", "int den = arr[b] - arr[a];"
        )
    if f == 290:
        code = code.replace("int paso = (int) floor(sqrt(n)), delta = paso;", "int paso = (int) sqrt(n);\n    int delta = paso;").replace(
            "delta = (int) minimo((int64_t) delta + paso, n);", "delta += paso;"
        )
    if f == 298:
        code = code.replace("i = (int) minimo((int64_t) i * 2, n);", "i *= 2;").replace(
            "        if (n == 0) {\n        return false;\n        }", "    if (n == 0) {\n        return false;\n    }"
        )
    if f == 243:
        code = """#include <stdlib.h>
#include <stdio.h>

double potencia(int a, int n) {
    if (n == 0)
        return 1;

    int absExponente = abs(n);
    double mitad = potencia(a, absExponente / 2);

    if (absExponente % 2 == 0)
        mitad = mitad * mitad;
    else
        mitad = mitad * mitad * a;

    return n < 0 ? 1.0 / mitad : mitad;
}"""
    if f == 363:
        code = """#include <stdlib.h>
#include <stdio.h>
#include <math.h>

void ordenarPorDigito(int arr[], int n, int i);

void ordenar(int arr[], int n) {
    int max = arr[0];
    for (int j = 1; j < n; j++) {
        if (arr[j] > max)
            max = arr[j];
    }

    int d = (int) floor(log10(max)) + 1;
    for (int i = 1; i <= d; i++)
        ordenarPorDigito(arr, n, i);
}

void ordenarPorDigito(int arr[], int n, int i) {
    int exp = (int) pow(10, i - 1);
    int conteo[10] = {0};
    int salida[n];

    for (int j = 0; j < n; j++)
        conteo[(arr[j] / exp) % 10]++;

    for (int j = 1; j < 10; j++)
        conteo[j] += conteo[j - 1];

    for (int j = n - 1; j >= 0; j--) {
        int d = (arr[j] / exp) % 10;
        salida[conteo[d] - 1] = arr[j];
        conteo[d]--;
    }

    for (int j = 0; j < n; j++)
        arr[j] = salida[j];
}"""
    if f == 167:
        code = (
            code.replace("#include <gmp.h>", '#include "mini-gmp.h"')
            .replace("mpz_inits(a, b, c, NULL);", "mpz_init(a);\n    mpz_init(b);\n    mpz_init(c);")
            .replace("mpz_clears(a, b, c, NULL);", "mpz_clear(a);\n    mpz_clear(b);\n    mpz_clear(c);")
        )
    if f == 148:
        code = """#include <stdio.h>

void acceder(int arr[], int i, int columnas, int m[][columnas], int j) {
    printf("arr[i]: %d\\n", arr[i]);
    printf("m[i][j]: %d\\n", m[i][j]);
}"""
    if f in (170, 171, 172, 173):
        code = (
            """#include <stdbool.h>
#include <stdio.h>

static bool gValor, hValor;
bool g(int n) { return gValor; }
bool h(int n) { return hValor; }
void r(int n) { printf("Se ejecuta la alternativa r(n)\\n"); }
void s(int n) { printf("Se ejecuta la alternativa s(n)\\n"); }

void evaluar(int n, bool var) {
"""
            + textwrap.indent(listing["code"], "    ")
            + "\n}"
        )
    if f in (161, 166):
        code += """\n
void foo1(void) { fprintf(stderr, "El libro no define foo1.\\n"); exit(1); }
void foo2(void) { fprintf(stderr, "El libro no define foo2.\\n"); exit(1); }
void foo(int n) { fprintf(stderr, "El libro no define foo.\\n"); exit(1); }"""
    return format_java(code)


def c_example(listing, *, runtime=False):
    code = c_implementation(listing)
    _, entries, _ = java_example(listing)
    declarations = []
    editable = []
    dimensions = {}
    for index, (_, literal, kind, name) in enumerate(entries):
        ckind = "bool" if kind == "boolean" else "int"
        if kind == "int[][]":
            values = json.loads(literal.replace("{", "[").replace("}", "]"))
            rows, cols = len(values), len(values[0])
            dimensions[name] = (rows, cols)
            declaration = f"int {name}[{rows}][{cols}] = {literal};"
            backend = f'Entrada {name}_entrada = entrada_arreglo(argc, argv, {index + 1}, "{literal}", 1);\nint (*{name})[{name}_entrada.columnas] = (int (*)[{name}_entrada.columnas]) {name}_entrada.valores;'
        elif kind == "int[]":
            values = json.loads(literal.replace("{", "[").replace("}", "]"))
            dimensions[name] = (len(values),)
            declaration = f"int {name}[] = {literal};"
            backend = f'Entrada {name}_entrada = entrada_arreglo(argc, argv, {index + 1}, "{literal}", 0);\nint *{name} = {name}_entrada.valores;'
        else:
            declaration = f"{ckind} {name} = {literal};"
            backend = f"{ckind} {name} = entrada_entero(argc, argv, {index + 1}, {literal});"
        declarations.append(backend if runtime else declaration)
        editable.append((declaration, literal, kind, name))
    f = listing["folio"]
    setup = []
    if "arr" in dimensions:
        setup.append("int n = arr_entrada.cantidad;" if runtime else "int n = sizeof(arr) / sizeof(arr[0]);")
    if f == 153:
        r, c = dimensions["matriz"]
        setup += [f"int m = {'matriz_entrada.filas' if runtime else r};", f"int n = {'matriz_entrada.columnas' if runtime else c};"]
    if f == 177:
        setup += [f"int n = {'a_entrada.filas' if runtime else dimensions['a'][0]};", "int resultado[n][n];"]
        if runtime:
            setup += [
                'if (a_entrada.filas != a_entrada.columnas || b_entrada.filas != n || b_entrada.columnas != n) entrada_error("Las matrices deben ser cuadradas y de igual dimensión.");'
            ]
    if f == 156:
        setup += ["int matriz[m][n];"]
    if f == 254:
        setup += ["Nodo izquierdo = {datoIzquierdo, NULL, NULL};", "Nodo raiz = {datoRaiz, &izquierdo, NULL};"]
    # En los predicados, las entradas son las variables globales de las auxiliares.
    if f in (170, 171, 172, 173):
        declarations = [d.replace("bool gValor =", "bool gEntrada =").replace("bool hValor =", "bool hEntrada =") for d in declarations]
        editable = [(d.replace("bool gValor =", "bool gEntrada =").replace("bool hValor =", "bool hEntrada ="), v, k, name) for d, v, k, name in editable]
        setup = ["gValor = gEntrada;", "hValor = hEntrada;"]
    if runtime:
        for matrix, shape in dimensions.items():
            if len(shape) == 2:
                rows, columns = shape
                setup.insert(
                    0,
                    f'if ({matrix}_entrada.filas != {rows} || {matrix}_entrada.columnas != {columns}) entrada_error("La matriz {matrix} debe tener {rows} filas y {columns} columnas, como en su declaración.");',
                )
        if "arr" in dimensions and any(name == "b" for _, _, _, name in entries):
            setup += ['if (a <= b && (a < 0 || b >= n)) entrada_error("El intervalo debe estar dentro del arreglo.");']
        if f == 148:
            setup += [
                'if (i < 0 || i >= n || i >= m_entrada.filas || j < 0 || j >= m_entrada.columnas) entrada_error("El índice debe estar dentro del arreglo y la matriz.");'
            ]
        if f == 156:
            setup.insert(0, 'if (m <= 0 || n <= 0 || (long long) m * n > 4096) entrada_error("Usa dimensiones positivas y como máximo 4096 elementos.");')
        if f == 158:
            setup.insert(0, 'if (m < 0 || n < 0 || (long long) m * n > 4096) entrada_error("Dimensiones inválidas o demasiado grandes.");')
        if f == 363:
            setup += [
                'if (!n) entrada_error("Radix requiere un arreglo no vacío.");',
                "int maximo = 0;",
                'for (int i = 0; i < n; i++) { if (arr[i] < 0) entrada_error("Radix requiere enteros no negativos."); if (arr[i] > maximo) maximo = arr[i]; }',
                'if (!maximo) entrada_error("Radix requiere al menos un valor positivo.");',
            ]
    methods = re.findall(r"^(?:int|double|bool|void)\s+(\w+)\(([^)]*)\)\s*\{", code, re.M)
    target = next(
        (
            m
            for m in methods
            if m[0]
            in (
                "buscar",
                "ordenar",
                "fibonacci",
                "factorial",
                "potencia",
                "sumar",
                "multiplicar",
                "inicializarMatriz",
                "imprimirMatriz",
                "imprimirElementos",
                "recorrerMatrizVacia",
                "cicloFijo",
                "iterar",
                "evaluar",
                "acceder",
                "fibonacciBigInteger",
            )
        ),
        None,
    )
    assert target, (f, code)
    name, params = target
    names = []
    for param in params.split(","):
        param = param.strip()
        if param in ("", "void"):
            continue
        words = re.findall(r"\w+", param.split("[")[0])
        names.append(words[-1])
    if f == 254:
        names[0] = "&raiz"
    if f == 148:
        names = ["arr", "i", "m_entrada.columnas" if runtime else str(dimensions["m"][1]), "m", "j"]
    if f == 167:
        setup += ["mpz_t resultado;", "mpz_init(resultado);"]
        names = ["n", "resultado"]
    call = name + "(" + ", ".join(names) + ")"
    if name == "ordenar":
        finish = call + ';\nprintf("Arreglo ordenado: [");\nfor (int i = 0; i < n; i++)\n    printf("%s%d", i ? ", " : "", arr[i]);\nprintf("]\\n");'
    elif f in (156, 177):
        finish = (
            call
            + ';\nprintf("Resultado: [");\nfor (int i = 0; i < '
            + ("m" if f == 156 else "n")
            + '; i++) {\n    printf("%s[", i ? ", " : "");\n    for (int j = 0; j < n; j++)\n        printf("%s%d", j ? ", " : "", '
            + ("matriz" if f == 156 else "resultado")
            + '[i][j]);\n    printf("]");\n}\nprintf("]\\n");'
        )
    elif f == 167:
        finish = call + ';\nchar *decimal = mpz_get_str(NULL, 10, resultado);\nprintf("Resultado: %s\\n", decimal);\nfree(decimal);\nmpz_clear(resultado);'
    elif name in ("buscar",):
        finish = 'printf("Resultado: %s\\n", ' + call + ' ? "true" : "false");'
    elif name in ("sumar", "fibonacci", "factorial"):
        finish = 'printf("Resultado: %d\\n", ' + call + ");"
    elif name == "potencia":
        finish = 'printf("Resultado: %.17g\\n", ' + call + ");"
    else:
        finish = call + ';\nprintf("Ejemplo finalizado\\n");'
    main = (
        "int main("
        + ("int argc, char **argv" if runtime else "void")
        + ") {\n"
        + textwrap.indent("\n".join(declarations) + "\n\n" + "\n".join(setup) + "\n\n" + finish + "\nreturn 0;", "    ")
        + "\n}"
    )
    includes = '\n#include "pages_inputs.h"\n' if runtime else ""
    source = "#include <stdbool.h>\n#include <stdio.h>\n#include <stdlib.h>\n" + includes + "\n" + code + "\n\n" + main
    headers = list(dict.fromkeys(re.findall(r"^#include .+$", source, re.M)))
    body = re.sub(r"^#include .+\n?", "", source, flags=re.M).lstrip()
    return format_java("\n".join(headers) + "\n\n" + body) + "\n", editable, example_key(listing)
