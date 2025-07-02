from collections import deque
import config

def find_path_to_nearest_key():
    # Set to keep track of visited positions
    visited = set()
    # Queue for BFS
    queue = deque()
    # Dictionary to reconstruct the path
    came_from = {}

    # Start position (player's current position)
    start = tuple(config.player_pos)
    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()

        # Check if current position is a key
        if current in config.keys:
            # Reconstruct the path from start to the key
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        # Explore neighbors (up, down, left, right)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (x + dx, y + dy)
            # Check if neighbor is within bounds, not visited, and not a wall
            if (0 <= neighbor[0] < config.COLS and 0 <= neighbor[1] < config.ROWS
                and neighbor not in visited
                and neighbor not in config.walls):
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)
    
    return []  # No path found

def find_path_to_crystal():
    # Set to keep track of visited positions
    visited = set()
    # Queue for BFS
    queue = deque()
    # Dictionary to reconstruct the path
    came_from = {}

    # Start position (player's current position)
    start = tuple(config.player_pos)
    # Goal position (crystal)
    goal = config.crystal
    if not goal:
        return []

    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()

        # Check if current position is the crystal
        if current == goal:
            # Reconstruct the path from start to the crystal
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        x, y = current
        # Explore neighbors (up, down, left, right)
        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            neighbor = (x + dx, y + dy)
            # Check if neighbor is within bounds, not visited, and not a wall
            if (0 <= neighbor[0] < config.COLS and 0 <= neighbor[1] < config.ROWS
                and neighbor not in visited
                and neighbor not in config.walls):
                visited.add(neighbor)
                came_from[neighbor] = current
                queue.append(neighbor)

    return []  # No path found
