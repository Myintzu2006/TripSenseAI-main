from prolog.generate_prolog import atom


def test_atom_keeps_simple_identifiers_unquoted():
    assert atom("Luang Prabang") == "luang_prabang"


def test_atom_quotes_and_escapes_apostrophes():
    assert atom("Cox's Bazar") == "'cox''s_bazar'"
    assert atom("Xi'an") == "'xi''an'"


def test_atom_quotes_non_ascii_identifiers():
    assert atom("Malé") == "'malé'"
