from pathlib import Path

DIR = Path(__file__).parent

with open(DIR.joinpath("physdesc.sql")) as f:
    PHYSDESC_SQL = f.read()

with open(DIR.joinpath("physdesc_lang.sql")) as f:
    PHYSDESC_LANG_SQL = f.read()
