"""Programas Java del libro y entradas parametrizadas para CheerpJ."""

import hashlib
import re
import textwrap


def example_key(listing):
    return hashlib.sha256((str(listing["folio"]) + listing["code"]).encode()).hexdigest()[:12]


def java_example(listing):
    key = example_key(listing)
    name = "Ejemplo" + key
    code = listing["code"]
    folio = listing["folio"]
    inputs = []
    for match in re.finditer(r"(\w+) = (\[\[.*?\]\]|\[.*?\]|-?\d+)", listing["example"]):
        value = match[2].replace("[", "{").replace("]", "}")
        kind = "int[][]" if match[2].startswith("[[") else "int[]" if match[2].startswith("[") else "int"
        inputs.append((kind, match[1], value))
    helpers = ""
    setup = ""
    if folio == 148:
        inputs += [("int[][]", "m", "{{1, 2}, {3, 4}}"), ("int", "j", "1")]
        code = """public static void acceder(int[] arr, int i, int[][] m, int j) {
    System.out.println("arr[i]: " + arr[i]);
    System.out.println("m[i][j]: " + m[i][j]);
}"""
    if folio in (170, 171, 172, 173):
        inputs = [("int", "n", "3"), ("boolean", "var", "false"), ("boolean", "gValor", "false"), ("boolean", "hValor", "true")]
        helpers = """private static boolean gValor, hValor;
private static boolean g(int n) { return gValor; }
private static boolean h(int n) { return hValor; }
private static void r(int n) { System.out.println("Se ejecuta la alternativa r(n)"); }
private static void s(int n) { System.out.println("Se ejecuta la alternativa s(n)"); }"""
        code = "public static void evaluar(int n, boolean var) {\n" + textwrap.indent(code, "    ") + "\n}"
        setup = f"{name}.gValor = gValor;\n{name}.hValor = hValor;\n"
    if folio in (161, 166):
        helpers = """private static void foo1() { throw new UnsupportedOperationException("El libro no define foo1; depende del problema analizado."); }
private static void foo2() { throw new UnsupportedOperationException("El libro no define foo2; depende del problema analizado."); }
private static void foo(int n) { throw new UnsupportedOperationException("El libro no define foo; depende del problema analizado."); }"""
    if folio == 254:
        inputs = [("int", "datoRaiz", "5"), ("int", "datoIzquierdo", "3"), ("int", "valor", "3")]
        helpers = """public static class Nodo {
    int dato;
    Nodo izquierdo, derecho;
    Nodo(int dato) { this.dato = dato; }
}"""
        setup = "Nodo raiz = new Nodo(datoRaiz);\nraiz.izquierdo = new Nodo(datoIzquierdo);\n"
    method = re.search(r"public\s+(static\s+)?([\w\[\]]+)\s+(\w+)\(([^)]*)\)", code)
    if not method:
        raise ValueError(f"No method: {folio}")
    static, result_type, method_name, parameters = method.groups()
    args = ", ".join(param.strip().split()[-1] for param in parameters.split(",") if param.strip())
    call = (name if static else f"new {name}()") + "." + method_name + "(" + args + ")"
    declarations = []
    editable = []
    for index, (kind, variable, literal) in enumerate(inputs):
        parser = {"int": "entero", "boolean": "logico", "int[]": "arreglo", "int[][]": "matriz"}[kind]
        default = ("new " + kind + " " if kind.endswith("[]") else "") + literal
        declaration = f"{kind} {variable} = Entradas.{parser}(args, {index}, {default});"
        declarations.append(declaration)
        editable.append((declaration, literal, kind, variable))
    if method_name == "ordenar":
        finish = (
            'System.out.println("Arreglo inicial: " + Arrays.toString(arr));\n' + call + ';\nSystem.out.println("Arreglo ordenado: " + Arrays.toString(arr));'
        )
    elif result_type == "void":
        finish = call + ';\nSystem.out.println("Ejemplo finalizado");'
    elif result_type == "int[][]":
        finish = 'System.out.println("Resultado: " + Arrays.deepToString(' + call + "));"
    else:
        finish = 'System.out.println("Resultado: " + ' + call + ");"
    main = "public static void main(String[] args) {\n" + textwrap.indent("\n".join(declarations) + "\n\n" + setup + finish, "    ") + "\n}"
    source = (
        "import java.util.*;\nimport java.math.*;\nimport ejemplos.Entradas;\n\npublic class "
        + name
        + " {\n"
        + textwrap.indent(code + "\n\n" + main + ("\n\n" + helpers if helpers else ""), "    ")
        + "\n}\n"
    )
    return source, editable, name
