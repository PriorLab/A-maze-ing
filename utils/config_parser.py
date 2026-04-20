# WIDTH=20
# HEIGHT=15
# ENTRY=0,0
# EXIT=19,14
# OUTPUT_FILE=maze.txt
# PERFECT=True
# 1.Verificacao se o ficheiro existe
# 2.Ignorar linhas comecadas com # ou vazias
# 3.Verificar se alguma linha nao tem =
# 4.Extrair chave e valor da linha
# 5.Ler todas as linhas e devolver dicionario com chave/valor em funcao raw
# 6.Verificar Chaves Obrigatorias nas linhas validas [WIDTH, HEIGHT, etc]
# 7.Verificar se algum dos valores e invalido e converter
# 8.Verificar se o labirinto e perfeito
# 9.Verificar e converter as coordenadas e se estao fora do labirinto
# 10.Converter Entry e Exit com verificacao para nao serem ==
# 11.Retornar a configuracao final do maze

from typing import TypedDict, TextIO

from exceptions import (
    ConfigFileNotFoundError,
    ConfigMissingKeyError,
    ConfigSyntaxError,
    ConfigValueError,
)


class MazeConfig(TypedDict):
    """Validated maze configuration returned by parse_config."""

    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool


KEYS: list[str] = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT"
]


def open_file(
        filepath: str) -> TextIO:
    """Open the configuration file or raise an error if not found."""
    try:
        return open(filepath, "r")
    except FileNotFoundError:
        raise ConfigFileNotFoundError(
            f"File not found: '{filepath}'."
        )


def check_is_ignorable(
        line: str) -> bool:
    """Return True if the line is empty or a comment."""
    return not line or line.startswith("#")


def check_has_equals(
        line: str, linenumb: int) -> None:
    """Raise an error if the line does not contain '='."""
    if "=" not in line:
        raise ConfigSyntaxError(
            f"Syntax error found in line {linenumb}."
        )


def extract_key_value(
        line: str) -> tuple[str, str]:
    """Extract and return the key and value from a KEY=VALUE line."""
    key, separator, value = line.partition("=")
    return key.strip().upper(), value.strip()


def make_raw_dict(
        file: TextIO) -> dict[str, str]:
    """Read all valid lines from the file and return a key-value dictionary."""
    raw: dict[str, str] = {}
    i = 1
    for line in file:
        line = line.strip()
        if check_is_ignorable(line):
            i += 1
            continue
        check_has_equals(line, i)
        key, value = extract_key_value(line)
        raw[key] = value
        i += 1
    return raw


def check_keys(
        raw: dict[str, str]) -> None:
    """Raise an error if any mandatory key is missing from the config."""
    for key in KEYS:
        if key not in raw:
            raise ConfigMissingKeyError(
                f"Missing '{key}' a mandatory key."
            )


def convert_width_height(
        raw: dict[str, str]) -> tuple[int, int]:
    """Convert WIDTH and HEIGHT to integers and validate their values."""
    try:
        width = int(raw["WIDTH"])
        height = int(raw["HEIGHT"])
    except ValueError:
        raise ConfigValueError(
            "WIDTH and HEIGHT must be integers."
        )
    if width < 2 or height < 2:
        raise ConfigValueError(
            "WIDTH or HEIGHT must be bigger than 2. "
            f"Current width={width} and height={height}."
        )
    return width, height


def check_perfect(
        raw: dict[str, str]) -> bool:
    """Convert PERFECT to a boolean and validate its value."""
    if raw["PERFECT"].upper() not in ("TRUE", "FALSE"):
        raise ConfigValueError(
            f"PERFECT must be true or false, found '{raw['PERFECT']}'."
        )
    return raw["PERFECT"].upper() == "TRUE"


def convert_coord(
        coord: str,
        key: str,
        width: int,
        height: int
) -> tuple[int, int]:
    """Convert a 'x,y' string to a tuple and validate it is within bounds."""
    parts = coord.split(",")

    if len(parts) != 2:
        raise ConfigValueError(
            f"'{key}' should be in the format 'x,y',"
            f" it was found '{coord}'."
        )

    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError:
        raise ConfigValueError(
            f"'{key}' must have numbers, found '{coord}'."
        )

    if x < 0 or x >= width or y < 0 or y >= height:
        raise ConfigValueError(
            f"'{key}'='{x},{y}' is out of bounds '{width}x{height}'."
        )

    return x, y


def convert_entry_exit(
        raw: dict[str, str],
        width: int,
        height: int
) -> tuple[tuple[int, int], tuple[int, int]]:
    """Convert ENTRY and EXIT coordinates and verify they are different."""
    entry = convert_coord(raw["ENTRY"], "ENTRY", width, height)
    exit_ = convert_coord(raw["EXIT"], "EXIT", width, height)
    if entry == exit_:
        raise ConfigValueError(
            "Entry and Exit cannot have the same coordinates."
        )
    return entry, exit_


def parse_config(
        filepath: str) -> MazeConfig:
    """Parse and validate the config file and return the maze configuration."""
    file = open_file(filepath)
    with file:
        raw = make_raw_dict(file)
    check_keys(raw)
    width, height = convert_width_height(raw)
    perfect = check_perfect(raw)
    entry, exit_ = convert_entry_exit(raw, width, height)

    return MazeConfig(
        WIDTH=width,
        HEIGHT=height,
        ENTRY=entry,
        EXIT=exit_,
        OUTPUT_FILE=raw["OUTPUT_FILE"],
        PERFECT=perfect,
    )
