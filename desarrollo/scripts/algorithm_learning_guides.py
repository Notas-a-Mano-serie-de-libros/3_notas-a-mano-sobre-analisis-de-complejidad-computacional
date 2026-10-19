"""Perfiles pedagógicos canónicos para búsquedas y ordenamientos clásicos."""

from __future__ import annotations

from html import escape

PROFILES = {
    (7, "1-busqueda-secuencial"): {
        "objective": "Trazar un recorrido lineal y justificar sus costos temporal y espacial.",
        "prerequisite": "Arreglos, índices y comparación de valores; los datos no necesitan estar ordenados.",
        "invariant": "Antes de revisar la posición i, ninguna posición anterior contiene el objetivo.",
        "use": "Úsela con colecciones pequeñas, desordenadas o cuando solo se hará una búsqueda.",
        "avoid": "Evítela para muchas consultas sobre un conjunto grande que pueda indexarse u ordenarse.",
        "properties": "Funciona sobre datos desordenados, conserva los datos y utiliza espacio auxiliar constante.",
        "mistake": "Confundir la detención temprana de un arreglo ordenado con una mejora del peor caso.",
        "questions": ("¿Qué posiciones ya pueden descartarse?", "¿Qué entrada produce el peor caso?"),
    },
    (7, "2-busqueda-binaria"): {
        "objective": "Actualizar correctamente los límites de búsqueda y explicar el crecimiento logarítmico.",
        "prerequisite": "Arreglos ordenados, índices y división entera.",
        "invariant": "Si el objetivo existe, permanece dentro del intervalo cerrado entre a y b.",
        "use": "Úsela para consultas repetidas sobre datos ordenados con acceso aleatorio.",
        "avoid": "No la aplique directamente a datos desordenados ni a estructuras sin acceso eficiente al medio.",
        "properties": "No modifica el arreglo y reduce al menos a la mitad el rango activo en cada iteración.",
        "mistake": "Actualizar a o b con m en vez de m + 1 o m - 1 y dejar el ciclo sin progreso.",
        "questions": ("¿Por qué puede descartarse una mitad completa?", "¿Qué condición indica que el objetivo no existe?"),
    },
    (7, "3-busqueda-interpolacion"): {
        "objective": "Relacionar la estimación de posición con la distribución de los valores.",
        "prerequisite": "Datos numéricos ordenados, búsqueda binaria y proporciones.",
        "invariant": "El objetivo, si existe, permanece dentro del rango cuyos extremos también acotan su valor.",
        "use": "Úsela cuando los valores numéricos ordenados se distribuyen de manera aproximadamente uniforme.",
        "avoid": "Evítela con datos muy sesgados, repetidos o sin una escala numérica significativa.",
        "properties": "Puede superar a la búsqueda binaria en distribuciones uniformes, pero su peor caso es lineal.",
        "mistake": "Suponer que la fórmula garantiza una buena estimación sin comprobar el denominador y los límites.",
        "questions": ("¿Qué ocurre si los extremos tienen el mismo valor?", "¿Cómo afecta una distribución sesgada a p?"),
    },
    (7, "4-busqueda-saltos"): {
        "objective": "Distinguir la fase de saltos de la exploración lineal del bloque.",
        "prerequisite": "Arreglos ordenados, raíz cuadrada y búsqueda secuencial.",
        "invariant": "Los bloques terminados antes de anterior no contienen el objetivo.",
        "use": "Úsela en datos ordenados cuando avanzar por bloques sea más conveniente que consultar puntos medios.",
        "avoid": "Evítela si los datos no están ordenados o si la búsqueda binaria tiene acceso aleatorio barato.",
        "properties": "Con saltos cercanos a la raíz de n equilibra los saltos y el recorrido final.",
        "mistake": "Contar solo los saltos y omitir el costo de la búsqueda lineal dentro del bloque.",
        "questions": ("¿Por qué se elige un salto cercano a √n?", "¿Qué bloque debe inspeccionarse linealmente?"),
    },
    (7, "5-busqueda-exponencial"): {
        "objective": "Construir un intervalo por duplicación y completar la búsqueda de forma binaria.",
        "prerequisite": "Datos ordenados, búsqueda binaria y potencias de dos.",
        "invariant": "Tras la expansión, el objetivo queda acotado entre el último índice válido y el nuevo límite.",
        "use": "Úsela cuando se desconoce el tamaño efectivo o el objetivo suele estar cerca del inicio.",
        "avoid": "Evítela sobre datos desordenados o cuando una búsqueda binaria directa ya conoce todo el rango.",
        "properties": "Combina una fase exponencial con otra binaria y mantiene costo logarítmico.",
        "mistake": "Usar el índice duplicado sin limitarlo al último índice del arreglo.",
        "questions": ("¿Cuándo termina la fase exponencial?", "¿Por qué la segunda fase sigue siendo logarítmica?"),
    },
    (7, "6-busqueda-ternaria"): {
        "objective": "Descartar dos tercios del intervalo mediante dos puntos de comparación.",
        "prerequisite": "Arreglos ordenados, intervalos cerrados y división entera.",
        "invariant": "Si el objetivo existe, se conserva dentro de uno de los tres intervalos delimitados.",
        "use": "Úsela con datos ordenados para estudiar estrategias de reducción por tercios.",
        "avoid": "No asuma que supera a la búsqueda binaria: realiza más comparaciones por iteración.",
        "properties": "No modifica los datos, usa espacio constante iterativamente y tiene costo logarítmico.",
        "mistake": "Crear intervalos solapados o no reducirlos por errores en m₁ y m₂.",
        "questions": ("¿Qué comparaciones seleccionan el tercio central?", "¿Por qué más divisiones no implican siempre mayor velocidad?"),
    },
    (8, "1-ordenamiento-burbuja"): {
        "objective": "Relacionar comparaciones adyacentes, intercambios y crecimiento cuadrático.",
        "prerequisite": "Arreglos, ciclos anidados e intercambio de valores.",
        "invariant": "Al terminar cada pasada, el extremo procesado contiene un elemento en su posición definitiva.",
        "use": "Úselo con fines didácticos o en entradas pequeñas y casi ordenadas con detención temprana.",
        "avoid": "Evítelo para colecciones grandes o cuando se requiera buen rendimiento general.",
        "properties": "Es estable, in situ y adaptativo cuando detecta una pasada sin intercambios.",
        "mistake": "Analizar solamente la versión sin detención temprana y atribuirle el mismo mejor caso.",
        "questions": ("¿Qué elemento queda fijado tras una pasada?", "¿Cuándo puede detenerse anticipadamente?"),
    },
    (8, "2-ordenamiento-seleccion"): {
        "objective": "Seguir la selección del candidato y diferenciar comparaciones de escrituras.",
        "prerequisite": "Arreglos, búsqueda de extremos e intercambio de valores.",
        "invariant": "La zona ya ubicada contiene los elementos extremos en sus posiciones definitivas.",
        "use": "Úselo en entradas pequeñas cuando convenga reducir el número de intercambios.",
        "avoid": "Evítelo si se necesita estabilidad o adaptación a datos casi ordenados.",
        "properties": "Es in situ, normalmente no estable y realiza un número cuadrático de comparaciones.",
        "mistake": "Confundir pocas escrituras con pocas comparaciones.",
        "questions": ("¿Qué representa el candidato actual?", "¿Por qué el mejor caso continúa siendo cuadrático?"),
    },
    (8, "3-ordenamiento-insercion"): {
        "objective": "Mantener un prefijo ordenado e insertar cada clave en su posición.",
        "prerequisite": "Arreglos, desplazamientos y comparación de elementos.",
        "invariant": "Antes de cada iteración, el prefijo anterior a i está ordenado.",
        "use": "Úselo con entradas pequeñas, casi ordenadas o como caso base de algoritmos híbridos.",
        "avoid": "Evítelo como estrategia única para entradas grandes y desordenadas.",
        "properties": "Es estable, in situ y adaptativo; la inserción binaria reduce comparaciones, no desplazamientos.",
        "mistake": "Contar la búsqueda de posición e ignorar el costo de desplazar elementos.",
        "questions": ("¿Qué parte permanece ordenada?", "¿Por qué la variante binaria no elimina el peor caso cuadrático?"),
    },
    (8, "4-ordenamiento-shell"): {
        "objective": "Explicar cómo los saltos reducen desplazamientos antes de la inserción final.",
        "prerequisite": "Ordenamiento por inserción y secuencias decrecientes de saltos.",
        "invariant": "Después de procesar un salto h, cada subsecuencia separada por h queda ordenada.",
        "use": "Úselo como alternativa in situ para tamaños medianos cuando una implementación sencilla sea prioritaria.",
        "avoid": "Evítelo cuando se necesiten estabilidad o garantías asintóticas independientes de la secuencia de saltos.",
        "properties": "Es in situ, no estable y su complejidad depende de la secuencia de saltos.",
        "mistake": "Asignar una única complejidad a Shell sin indicar qué secuencia de saltos se analiza.",
        "questions": ("¿Qué significa que el arreglo esté h-ordenado?", "¿Por qué la última pasada usa h = 1?"),
    },
    (8, "5-ordenamiento-mezcla"): {
        "objective": "Distinguir las fases de división y combinación y derivar su costo log-lineal.",
        "prerequisite": "Recursión, subarreglos y combinación de secuencias ordenadas.",
        "invariant": "Durante la combinación, la salida escrita contiene los menores elementos ya procesados en orden.",
        "use": "Úselo cuando se requieran estabilidad, rendimiento predecible o procesamiento secuencial de datos.",
        "avoid": "Evítelo si la memoria auxiliar es muy limitada y existe una alternativa in situ adecuada.",
        "properties": "Es estable, garantiza tiempo log-lineal y normalmente requiere espacio auxiliar lineal.",
        "mistake": "Confundir la profundidad logarítmica con el trabajo lineal realizado en cada nivel.",
        "questions": ("¿Cuándo termina la división?", "¿Qué condición mantiene ordenada la salida durante la combinación?"),
    },
    (8, "6-ordenamiento-rapido"): {
        "objective": "Trazar una partición y explicar el efecto del pivote sobre la profundidad recursiva.",
        "prerequisite": "Recursión, particiones e intercambio de valores.",
        "invariant": "Tras particionar, cada región cumple la relación definida respecto al pivote.",
        "use": "Úselo para ordenamiento interno general cuando importen localidad y buen rendimiento promedio.",
        "avoid": "Evítelo sin una estrategia de pivote segura si el peor caso es crítico o se exige estabilidad.",
        "properties": "Suele ser in situ, no estable y rápido en promedio; particiones desequilibradas producen tiempo cuadrático.",
        "mistake": "Suponer que elegir cualquier pivote produce siempre dos mitades equilibradas.",
        "questions": ("¿Qué garantiza la partición aunque el pivote no quede centrado?", "¿Qué entradas pueden generar el peor caso?"),
    },
    (8, "7-ordenamiento-radix"): {
        "objective": "Seguir las fases de distribución y reconstrucción preservando el orden relativo.",
        "prerequisite": "Representación posicional, conteo estable y arreglos auxiliares.",
        "invariant": "Después de la pasada i, los elementos están ordenados por los i dígitos procesados.",
        "use": "Úselo con claves de longitud acotada que puedan descomponerse en dígitos o caracteres.",
        "avoid": "Evítelo si las claves no admiten una representación adecuada o la memoria auxiliar es restrictiva.",
        "properties": "No compara claves entre sí, necesita una distribución estable y usa espacio auxiliar proporcional a n más la base.",
        "mistake": "Reconstruir los buckets sin estabilidad y destruir el orden obtenido en pasadas anteriores.",
        "questions": ("¿Por qué la distribución debe ser estable?", "¿Cómo cambian tiempo y memoria al aumentar la base?"),
    },
}


def render_learning_guide(chapter: int, slug: str) -> str:
    """Renderiza la guía semántica de una página de algoritmo."""

    profile = PROFILES.get((chapter, slug))
    if profile is None:
        return ""
    guide_id = f"guia-{slug}"
    questions = "".join(f"<li>{escape(question)}</li>" for question in profile["questions"])
    return f'''<!-- algorithm-learning-guide:start -->
<section class="algorithm-learning-guide" aria-labelledby="{guide_id}">
  <h2 id="{guide_id}">Guía de aprendizaje</h2>
  <dl>
    <dt>Objetivo</dt><dd>{escape(profile["objective"])}</dd>
    <dt>Prerrequisitos</dt><dd>{escape(profile["prerequisite"])}</dd>
    <dt>Invariante que debe observar</dt><dd>{escape(profile["invariant"])}</dd>
    <dt>Cuándo usarlo</dt><dd>{escape(profile["use"])}</dd>
    <dt>Cuándo evitarlo</dt><dd>{escape(profile["avoid"])}</dd>
    <dt>Propiedades</dt><dd>{escape(profile["properties"])}</dd>
    <dt>Error frecuente</dt><dd>{escape(profile["mistake"])}</dd>
  </dl>
  <h3>Compruebe su comprensión</h3>
  <ol>{questions}</ol>
</section>
<!-- algorithm-learning-guide:end -->'''


__all__ = ["PROFILES", "render_learning_guide"]
