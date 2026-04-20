# solver_bfs.py
# Encontra o caminho mais curto entre ENTRY e EXIT usando BFS
# Bits que representam as paredes de cada celula
# 1 = Norte, 2 = Este, 4 = Sul, 8 = Oeste

# 1. Verificar se uma celula tem parede numa direcao
# 2. Verificar se uma celula vizinha esta dentro dos limites do labirinto
# 3. Encontrar os vizinhos acessiveis de uma celula (sem parede entre elas)
# 4. Percorrer o came_from ao contrario para reconstruir o caminho
# 5. Loop principal do BFS
# 6. Funcao principal que junta tudo


def solve_maze(maze:list[list[int]], entry: tuple[int, int], exit_: tuple[int, int], width: int, height:int) -> list[str]:
    queue = [entry]
    visited = {entry}
    came_from = {}

    found = bfs_loop(maze, queue,visited, came_from, exit_, width, height)
    if not found:
        return[]
    
    return reconstruct_path(came_from, entry, exit_)