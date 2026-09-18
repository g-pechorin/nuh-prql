import re
from pathlib import Path

import pyprql


def translate(src: Path, csv: Path, dir: Path) -> Path:
    txt = src.read_text()

    txt = bind_csvs(txt, csv)

    sql = pyprql.compile(txt)

    out = dir / (src.stem + ".sql")

    out.write_bytes(sql.encode("utf8"))

    return out


pattern = re.compile(r"(.+)`([^`]+)`(.*)", re.DOTALL)


def bind_csvs(txt: str, csv: Path) -> str:

    # pattern = re.compile()
    # pattern = re.compile('(.*)`([^`]+)`(.*)')

    res = re.fullmatch(pattern, txt)
    # res = re.fullmatch(r"(.+)`([^`]+)`(.*)", txt, re.DOTALL)
    if not res:
        return txt

    text = (csv / res[2]).read_text().strip().removeprefix("\ufeff")

    return bind_csvs(f'{res[1]}(from_text """\n{text}\n"""){res[3]}', csv)
