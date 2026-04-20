import sys
from dataclasses import dataclass
from typing import Any
from random import randint


@dataclass
class Config:
    width: int
    height: int
    entry: tuple
    exit: tuple
    output_file: str
    perfect: bool


class Maze():
    def __init__(self, config: Config) -> None:
        self.width = config.width
        self.height = config.height
        self.entry = config.entry
        self.exit = config.exit
        self.output = config.output_file
        self.perfect = config.perfect
        self.grid: list[list[int]] = []

    def maze_length(self) -> tuple:
        return self.width, self.height

    def gen_maze(self) -> list:
        i: int = 0
        while i < self.width:
            row: list[int] = []
            j = 0
            while j < self.height:
                row.append(0xF)
                j += 1
            self.grid.append(row)
            print(f"[{i}]", end=" ")
            print(f"{row}")
            i += 1
        return self.grid

    def print_maze(self) -> list:
        i: int = 0
        for row in self.grid:
            print(f"[{i}]", end="")
            print(row)
            i += 1
        return self.grid

    pass

# Ler o ficheiro de configuração


def get_conf() -> str:
    content: str = ""
    args = sys.argv
    for data in args:
        if data == "config/default_config.txt":
            content = str(data)
        print(content)
    return content


def open_wall(grid: list[list[int]], len_x: int, len_y: int) -> list:

    for y in range(len(grid)):
        for x in range(len(grid[y])):
            # Open East and South
            if (y == 0) and (x == 0):
                for i in 1, 2:
                    grid[y][x] &= ~(1 << i)

            # Open East, North and West
            if (y == 0) and (x != 0):
                for i in range(randint(1, 3)):
                    grid[y][x] &= ~(1 << i)

            # Open East, North and South
            if (y != 0) and (x == 0):
                for i in 3, 3:
                    grid[y][x] &= ~(1 << i)

            # Open East, North and South
            if (y == 0) and (x == len_x):
                for i in 2, 3:
                    grid[y][x] &= ~(1 << i)

            # Open East, North and South
            if (y != 0) and (x == len_x):
                for i in 2, 3:
                    grid[y][x] &= ~(1 << i)

            # Open East, North and South
            if (y == len_y) and (x != 0):
                for i in range(randint(0, 1)):
                    grid[y][x] &= ~(1 << i)
                # print(f"{grid[y][x]}")
    return grid


def map_conf(file: str) -> Config:
    content: list = []
    conf: dict[str, Any] = {}
    with open(file, "r") as f:
        content = f.readlines()
        f.close()
    for data in content:
        if "=" not in data:
            continue
        key, _, value = data.partition("=")
        key = key.strip()
        value = value.strip()

        if not key:
            continue
        if key == "WIDTH":
            conf[key.lower()] = (int(value))
        if key == "HEIGHT":
            conf[key.lower()] = (int(value))
        if key == "ENTRY":
            coords0, coords1 = map(int, value.split(","))
            conf[key.lower()] = (coords0, coords1)
        if key == "EXIT":
            coords0, coords1 = map(int, value.split(","))
            conf[key.lower()] = (coords0, coords1)
        if key == "OUTPUT_FILE":
            conf[key.lower()] = (value.strip("\n"))
        if key == "PERFECT":
            conf[key.lower()] = value.strip("\n") == "True"
    return Config(**conf)


# Criar a grid


# Implementar o algoritimo


def main() -> int:
    # Encontrar o ficheiro
    conf: str = get_conf()
    # Mapear o ficheiro
    data_conf: Config = map_conf(conf)

    # Criar o maze
    maze = Maze(data_conf)
    print(f"Retornando configurações: {data_conf}")

    grid = maze.gen_maze()
    len_x, len_y = maze.maze_length()
    open_wall(grid, (len_x - 1), (len_y - 1))
    print(f"Tamanho da grid: {len(grid)}")
    maze.print_maze()
    return 0


if __name__ == "__main__":
    main()
