#WIDTH=20
#HEIGHT=15 
#ENTRY=0,0
#EXIT=19,14
#OUTPUT_FILE=maze.txt
#PERFECT=True
#1.Verificacao se o ficheiro existe
#2.Ignorar linhas comecadas com # ou vazias
#3.Verificar se alguma linha nao tem =
#4.Extrair chave e valor da linha
#5.Ler todas as linhas e devolver dicionario com chave/valor em funcao raw
#6.Verificar Chaves Obrigatorias nas linhas validas [WIDTH, HEIGHT, ENTRY, EXIT]
#7.Verificar se algum dos valores e invalido e converter
#8.Verificar se o labirinto e perfeito
#9.Verificar e converter as coordenadas e se estao fora do labirinto
#10.Converter Entry e Exit com verificacao para nao serem ==
#11.Retornar a configuracao final do maze

#Importei Erros configurados em excepions.py
from exceptions import(
    ConfigFileNotFoundError,
    ConfigMissingKeyError,
    ConfigSyntaxError,
    ConfigValueError,
)
#Defini os parametros de saida do parsing
from typing import TypedDict
class MazeConfig(TypedDict):
    WIDTH: int
    HEIGHT: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
#Defini os nomes das chaves que sao obrigatorias para procurar valores
KEYS: list[str] = [
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT"
]

#1.Verificacao se o ficheiro existe
def open_file(filepath: str):
    try:
        return open(filepath, "r")
    except FileNotFoundError:
        raise ConfigFileNotFoundError(
            f"File not found: '{filepath}'."
        )
#2.Ignorar linhas comecadas com # ou vazias
def check_is_ignorable(line:str) -> bool:
    return not line or line.startswith("#")
#3.Verificar se alguma linha nao tem =
def check_has_equals (line: str, linenumb: int) -> None:
    if "=" not in line:
        raise ConfigSyntaxError(
            f"Syntax error found in line {linenumb}."
        )
#4.Extrair chave e valor da linha
def extract_key_value(line: str) -> tuple[str, str]:
    key, separator, value = line.partition("=")
    return key.strip().upper(), value.strip()
#5.Ler todas as linhas e devolver dicionario com chave/valor
def make_raw_dict(file) -> dict[str, str]:
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
        i+=1
    return raw
#6.Verificar Chaves Obrigatorias nas linhas validas [WIDTH, HEIGHT, ENTRY, EXIT]
def check_keys(raw: dict[str, str]) -> None:
    for key in KEYS:
        if key not in raw:
            raise ConfigMissingKeyError(
                f"Missing'{key}' a mandatory key."
            )
#7.Verificar se algum dos valores e invalido e converter
def convert_width_height(raw: dict[str, str]) -> tuple[int, int]:
    try:
        width = int(raw["WIDTH"])
        height = int(raw["HEIGHT"])
    except ValueError:
        raise ConfigValueError(
            f" WIDTH and HEIGHT must be intengers."
        )
    if width < 2 or height < 2:
        raise ConfigValueError(
            f"WIDTH or HEIGHT must be bigger than 2. Current width={width} and height={height}."
        )
    return width, height
#8.Verificar se o labirinto e perfeito
def check_perfect(raw: dict[str, str]) -> bool:
    if raw ["PERFECT"].upper() not in ("TRUE", "FALSE"):
        raise ConfigValueError(
            f"PERFECT  must be true or false, found '{raw['PERFECT']}'."
        )
    return raw["PERFECT"].upper() == "TRUE"
#9.Verificar e converter as coordenadas e se estao fora do labirinto
def convert_coord(coord:str, key:str, width:int, height:int) -> tuple[int, int]:
    parts = coord.split(",")

    if len(parts) != 2:
        raise ConfigValueError(
            f"'{key}' should be in the format 'x,y', it was found '{coord}'."
        )
    
    try:
        x = int(parts[0].strip())
        y = int(parts[1].strip())
    except ValueError:
        raise ConfigValueError(
            f"'{key}' must have numbers, found '{coord}'."
        )
    
    if x<0 or x>= width or y<0 or y>= height:
        raise ConfigValueError(
            f"'{key}'='{x},{y} is out of bounds '{width}x{height}'."
        )
    
    return x,y
#10.Converter Entry e Exit usando 9
def convert_entry_exit(raw:dict[str,str], width:int, height:int) -> tuple[tuple[int, int], tuple[int,int]]:
    entry = convert_coord(raw["ENTRY"], "ENTRY", width, height)
    exit_ = convert_coord(raw["EXIT"], "EXIT", width, height)
    if entry == exit_:
        raise ConfigValueError(
            f"Entry and Exit cannot have the same coordinates."
        )
    return entry, exit_
#11.Retornar a configuracao final do maze
def parse_config(filepath: str) -> MazeConfig:
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
