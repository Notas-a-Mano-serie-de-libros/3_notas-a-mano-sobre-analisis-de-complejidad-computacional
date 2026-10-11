from desarrollo.scripts.validate_book_structure import validate


def test_pages_preserva_la_estructura_declarada_del_libro():
    assert validate() == []
