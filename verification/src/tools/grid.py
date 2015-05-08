__all__ = ["fill_square", "find_route"]

from heapq import heappop, heappush
from .math import manhattan_distance
from itertools import product

SQRT_2 = round(2 ** 0.5, 3)
HEURISTIC = manhattan_distance

DIRS = (
    (-1, 0, 1),
    (1, 0, 1),
    (0, 1, 1),
    (0, -1, 1),
    # (-1, 1, SQRT_2),
    # (1, -1, SQRT_2),
    # (-1, -1, SQRT_2),
    # (1, 1, SQRT_2),
)


def fill_square(matrix: list, row: int, column: int, size: int, fill_element=1) -> list:
    height, width = len(matrix), len(matrix[0]) if matrix else 0
    for i in range(max(row, 0), min(row + size, height)):
        for j in range(max(column, 0), min(column + size, width)):
            matrix[i][j] = fill_element
    return matrix


def get_neighbours(grid: list, cell: tuple):
    x, y = cell
    max_x, max_y = len(grid), len(grid[0]) if grid else 0
    result = []
    for dx, dy, cost in DIRS:
        nx, ny = x + dx, y + dy
        if 0 <= nx < max_x and 0 <= ny < max_y and grid[nx][ny]:
            result.append(((nx, ny), cost))
    return result


def heuristic(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def find_possible_end(grid, goal):
    result = set()
    radius = 1
    while not result:
        for dx, dy in product(range(-radius, radius + 1), repeat=2):
            nx, ny = goal[0] + dx, goal[1] + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny]:
                result.add((nx, ny))
        radius += 1
    return result


def find_route(grid, start_cell, end_cell):
    heap = []
    end_cell = tuple(end_cell)
    if not grid[end_cell[0]][end_cell[1]]:
        goals = find_possible_end(grid, end_cell)
    else:
        goals = {tuple(end_cell)}
    # priority, distance, path, cell
    heappush(heap, (0, 0, (start_cell,), start_cell))
    visited = set()
    count = 0
    while heap:
        _, distance, path, current = heappop(heap)
        count += 1
        if current in visited:
            continue
        visited.add(current)
        if current in goals:
            return path
        for neighbour, cost in get_neighbours(grid, current):
            if neighbour in visited:
                continue
            priority = distance + HEURISTIC(neighbour, end_cell)
            heappush(heap, (priority, distance + cost, path + (neighbour,), neighbour))
    return ()


if __name__ == "__main__":
    from timeit import timeit

    test = (
        (1, 1, 1, 0, 0, 1, 1, 1),
        (1, 0, 1, 0, 0, 1, 1, 1),
        (1, 0, 1, 1, 1, 0, 0, 1),
        (1, 0, 1, 1, 1, 0, 1, 1),
        (1, 1, 1, 1, 1, 0, 1, 1),
        (1, 1, 1, 1, 1, 0, 1, 1),
    )
    print(find_route(test, (2, 0), (5, 6)))
    print(timeit("find_route(test, (2, 0), (5, 6))",
                 "from __main__ import find_route, test",
                 number=1))