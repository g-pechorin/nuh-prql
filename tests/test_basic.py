from pathlib import Path

import nuh_prql

data = Path(__file__).parent / "data" / Path(__file__).stem


def test_foo(tmp_path: Path):

    sql = nuh_prql.translate(data / "test_foo.prql", data, tmp_path)

    assert sql.read_text() == (data / "test_foo.sql-expected").read_text()


def test_from_text(tmp_path: Path):

    sql = nuh_prql.translate(data / "test_from_text.prql", data, tmp_path)

    assert sql.read_text() == (data / "test_from_text.sql-expected").read_text()


def test_substitute():
    import textwrap

    src = textwrap.dedent("""
    from a = `abc.csv` select { invoice_id, total }
    derive {
        d = b + c,
        answer = 20 * 2 + 2,
    }
    """)

    sub = nuh_prql.bind_csvs(src, data)

    assert sub == textwrap.dedent('''
    from a = (from_text """
    a,b,c
    1,2,3
    4,5,6
    """) select { invoice_id, total }
    derive {
        d = b + c,
        answer = 20 * 2 + 2,
    }
    ''')


def test_example(tmp_path: Path):

    sql = nuh_prql.translate(data / "test_example.prql", data, tmp_path)

    assert sql.read_text() == (data / "test_example.sql-expected").read_text()


def test_example_big(tmp_path: Path):

    sql = nuh_prql.translate(data / "test_example_big.prql", data, tmp_path)

    assert sql.read_text() == (data / "test_example_big.sql-expected").read_text()
