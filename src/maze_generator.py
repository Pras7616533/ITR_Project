import random
from collections import deque

def bfs_path_exists(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([start])
    visited[start[1]][start[0]] = True

    while queue:
        x, y = queue.popleft()
        if (x, y) == goal:
            return True
        for dx, dy in [(0,1), (1,0), (-1,0), (0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if not visited[ny][nx] and maze[ny][nx] != 'W':
                    visited[ny][nx] = True
                    queue.append((nx, ny))
    return False

def safe_place_wall(maze, path_start, path_end, max_walls):
    placed = 0
    rows, cols = len(maze), len(maze[0])
    while placed < max_walls:
        x, y = random.randint(1, cols-2), random.randint(1, rows-2)
        if maze[y][x] == ' ':
            maze[y][x] = 'W'
            if bfs_path_exists(maze, path_start, path_end):
                placed += 1
            else:
                maze[y][x] = ' '  # rollback

def place_items_reachable(maze, symbol, count, start_pos):
    reachable_positions = get_reachable_positions(maze, start_pos)
    empty_positions = [pos for pos in reachable_positions if maze[pos[1]][pos[0]] == ' ']
    random.shuffle(empty_positions)

    for i in range(min(count, len(empty_positions))):
        x, y = empty_positions[i]
        maze[y][x] = symbol

def get_reachable_positions(maze, start):
    rows, cols = len(maze), len(maze[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    queue = deque([start])
    visited[start[1]][start[0]] = True
    reachable = []

    while queue:
        x, y = queue.popleft()
        reachable.append((x, y))
        for dx, dy in [(0,1), (1,0), (-1,0), (0,-1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if not visited[ny][nx] and maze[ny][nx] == ' ':
                    visited[ny][nx] = True
                    queue.append((nx, ny))
    return reachable

def generate_maze(rows, cols, level=1):
    max_attempts = 100
    for _ in range(max_attempts):
        # Initialize empty maze
        maze = [[' ' for _ in range(cols)] for _ in range(rows)]

        # Add outer walls
        for x in range(rows):
            maze[x][0] = maze[x][cols - 1] = 'W'
        for y in range(cols):
            maze[0][y] = maze[rows - 1][y] = 'W'

        # Place player and crystal with path
        for attempt in range(100):
            px, py = random.randint(1, cols-2), random.randint(1, rows-2)
            cx, cy = random.randint(1, cols-2), random.randint(1, rows-2)
            if (px, py) != (cx, cy):
                maze[py][px] = 'P'
                maze[cy][cx] = 'C'
                if bfs_path_exists(maze, (px, py), (cx, cy)):
                    break
                maze[py][px] = maze[cy][cx] = ' '
        else:
            continue  # retry whole maze

        # Place safe walls
        num_walls = 20 + level * 4
        safe_place_wall(maze, (px, py), (cx, cy), num_walls)

        # Place other elements
        num_traps = 3 + level
        num_keys = int(1 + level // 2)
        num_healths = num_traps // 3 if level <= 3 else num_traps // 2

        place_items_reachable(maze, 'T', num_traps, (px, py))
        place_items_reachable(maze, 'K', num_keys, (px, py))
        place_items_reachable(maze, 'H', num_healths, (px, py))

        return maze

    raise ValueError("Failed to generate valid maze after several attempts")
