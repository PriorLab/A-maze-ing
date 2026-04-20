import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "..", "utils"))

from config_parser import parse_config
from exceptions import (
    ConfigFileNotFoundError,
    ConfigMissingKeyError,
    ConfigSyntaxError,
    ConfigValueError,
)


def run(name: str, content: str, expected_error) -> None:
    with open("tmp.txt", "w") as f:
        f.write(content)
    try:
        parse_config("tmp.txt")
        if expected_error is None:
            print(f"[OK] {name}")
        else:
            print(f"[FAIL] {name} — esperava {expected_error.__name__} mas nao houve erro")
    except Exception as e:
        if expected_error and isinstance(e, expected_error):
            print(f"[OK] {name} — {type(e).__name__}: {e}")
        else:
            print(f"[FAIL] {name} — erro inesperado: {type(e).__name__}: {e}")


def run_no_file(name: str, filepath: str, expected_error) -> None:
    try:
        parse_config(filepath)
        print(f"[FAIL] {name} — esperava {expected_error.__name__} mas nao houve erro")
    except Exception as e:
        if expected_error and isinstance(e, expected_error):
            print(f"[OK] {name} — {type(e).__name__}: {e}")
        else:
            print(f"[FAIL] {name} — erro inesperado: {type(e).__name__}: {e}")


print("=== TESTES MENSAGENS DE ERRO ===\n")

run_no_file(
    "ficheiro nao existe",
    "fantasma.txt",
    ConfigFileNotFoundError
)

run(
    "linha sem =",
    "WIDTH=20\nHEIGHT 15\nENTRY=0,0\nEXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=True\n",
    ConfigSyntaxError
)

run(
    "chave em falta",
    "WIDTH=20\nENTRY=0,0\nEXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=True\n",
    ConfigMissingKeyError
)

run(
    "WIDTH nao e numero",
    "WIDTH=abc\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=True\n",
    ConfigValueError
)

run(
    "WIDTH menor que 2",
    "WIDTH=1\nHEIGHT=15\nENTRY=0,0\nEXIT=0,14\nOUTPUT_FILE=maze.txt\nPERFECT=True\n",
    ConfigValueError
)

run(
    "PERFECT invalido",
    "WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=maybe\n",
    ConfigValueError
)

run(
    "ENTRY fora dos limites",
    "WIDTH=20\nHEIGHT=15\nENTRY=99,99\nEXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=True\n",
    ConfigValueError
)

run(
    "ENTRY igual a EXIT",
    "WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=0,0\nOUTPUT_FILE=maze.txt\nPERFECT=True\n",
    ConfigValueError
)

run(
    "ENTRY formato errado",
    "WIDTH=20\nHEIGHT=15\nENTRY=0\nEXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=True\n",
    ConfigValueError
)

run(
    "ENTRY com letras",
    "WIDTH=20\nHEIGHT=15\nENTRY=a,b\nEXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=True\n",
    ConfigValueError
)

run(
    "config valida",
    "WIDTH=20\nHEIGHT=15\nENTRY=0,0\nEXIT=19,14\nOUTPUT_FILE=maze.txt\nPERFECT=True\n",
    None
)

print("\n=== FIM ===")