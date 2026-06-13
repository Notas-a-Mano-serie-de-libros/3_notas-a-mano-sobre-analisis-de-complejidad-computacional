from capitulo5.recurrence_methods_animation import Recurrence, analyze, render_method_panels


def test_division_relation_applies_iterative_tree_and_master():
    result = analyze(Recurrence("division", (2,), (0.5,), "linear"), depth=2)
    assert "C(n)=2C\\left(0.5n\\right)+n" in result["equation"]
    assert result["iterative"].count("Aplica") == 1
    assert "<svg" in result["tree"]
    assert "Variante básico" in result["master"]
    assert "No aplica" in result["characteristic"]


def test_mixed_relation_uses_generalized_master():
    result = analyze(Recurrence("division", (1, 1), (1 / 3, 2 / 3), "quadratic"), depth=2)
    assert "Akra-Bazzi" in result["master"]
    assert "No aplica" in result["iterative"]
    assert "desbalanceado" in result["tree"]


def test_linear_order_two_uses_characteristic_equation():
    result = analyze(Recurrence("linear", (1, 1), (1, 2), "zero"))
    assert "x^2-1x-1=0" in result["characteristic"]
    assert "No aplica" in result["master"]
    assert "No aplica" in result["tree"]


def test_original_tree_interface_receives_synchronized_method_panels():
    markup = render_method_panels("division", (2,), (0.5,), "linear", 4)
    assert "recursion-info-section" in markup
    assert "Sustitución iterativa" in markup
    assert "Teorema maestro" in markup
    assert "Ecuación característica" in markup
    assert "Árbol de recurrencia - solución" in markup
    assert "Hallar el último nivel" in markup
    assert "Acumular todos los niveles" in markup
    assert r"\Theta\left(n\log n\right)" in markup


def test_master_variant_can_reject_an_incompatible_choice():
    markup = render_method_panels(
        "division", (1, 1), (1 / 3, 2 / 3), "quadratic", 4,
        group="master", master_variant="basic",
    )
    assert "Teorema maestro básico" in markup
    assert "No aplica" in markup
    assert "un solo tamaño de subproblema" in markup
