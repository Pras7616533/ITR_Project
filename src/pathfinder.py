from collections import deque
import config

def find_path_to_nearest_key():
    visited = set()
    queue = deque()
    came_from = {}

    start = tuple(config.player_pos)
    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()

        if current in config.keys:
            # Reconstruct path
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (x + dx, y + dy)
            if (0 <= neighbor[0] < config.COLS and 0 <= neighbor[1] < config.ROWS
                and neighbor not in visited
                and neighbor not in config.walls):
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
    
    return []  # No path found

def find_path_to_crystal():
    visited = set()
    queue = deque()
    came_from = {}

    start = tuple(config.player_pos)
    goal = config.crystal
    if not goal:
        return []

    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()

        if current == goal:
            # Reconstruct path
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (x + dx, y + dy)
            if (0 <= neighbor[0] < config.COLS and 0 <= neighbor[1] < config.ROWS
                and neighbor not in visited
                and neighbor not in config.walls):
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    return []  # No path found
