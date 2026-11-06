import tkinter as tk
from tkinter import ttk
from collections import deque
from heapq import heappush, heappop

# =========================
# MAZE (MÊ CUNG)
# =========================

maze = [
    ['A', '.', '.', '.', '#', '.', '.'],
    ['#', '#', '.', '.', '#', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.'],
    ['.', '#', '#', '#', '#', '.', '.'],
    ['.', '.', '.', '.', '#', '.', '.'],
    ['.', '.', '.', '.', '.', '.', 'G']
]

ROWS = len(maze)
COLS = len(maze[0])

CELL = 70

# =========================
# TÌM START & GOAL
# =========================

START = None
GOAL = None

for r in range(ROWS):
    for c in range(COLS):
        if maze[r][c] == 'A':
            START = (r, c)
        elif maze[r][c] == 'G':
            GOAL = (r, c)

# =========================
# HÀM PHỤ
# =========================

def heuristic(pos):
    return abs(pos[0] - GOAL[0]) + abs(pos[1] - GOAL[1])

def get_neighbors(pos):
    r, c = pos

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    result = []

    for dr, dc in directions:
        nr = r + dr
        nc = c + dc

        if 0 <= nr < ROWS and 0 <= nc < COLS:
            if maze[nr][nc] != '#':
                result.append((nr, nc))

    return result

# =========================
# BFS
# =========================

def bfs():
    queue = deque([[START]])
    visited = {START}
    explored = []

    while queue:
        path = queue.popleft()
        node = path[-1]

        explored.append(node)

        if node == GOAL:
            return path, explored

        for nb in get_neighbors(node):
            if nb not in visited:
                visited.add(nb)
                queue.append(path + [nb])

    return [], explored

# =========================
# DFS
# =========================

def dfs():
    stack = [[START]]
    visited = set()
    explored = []

    while stack:
        path = stack.pop()
        node = path[-1]

        if node in visited:
            continue

        visited.add(node)
        explored.append(node)

        if node == GOAL:
            return path, explored

        for nb in reversed(get_neighbors(node)):
            stack.append(path + [nb])

    return [], explored

# =========================
# UCS
# =========================

def ucs():
    pq = []
    heappush(pq, (0, [START]))

    visited = {}
    explored = []

    while pq:
        cost, path = heappop(pq)
        node = path[-1]

        if node in visited:
            continue

        visited[node] = cost
        explored.append(node)

        if node == GOAL:
            return path, explored

        for nb in get_neighbors(node):
            heappush(pq, (cost + 1, path + [nb]))

    return [], explored

# =========================
# GREEDY
# =========================

def greedy():
    pq = []
    heappush(pq, (heuristic(START), [START]))

    visited = set()
    explored = []

    while pq:
        h, path = heappop(pq)
        node = path[-1]

        if node in visited:
            continue

        visited.add(node)
        explored.append(node)

        if node == GOAL:
            return path, explored

        for nb in get_neighbors(node):
            heappush(pq, (heuristic(nb), path + [nb]))

    return [], explored

# =========================
# A*
# =========================

def astar():
    pq = []
    heappush(pq, (heuristic(START), 0, [START]))

    visited = {}
    explored = []

    while pq:
        f, g, path = heappop(pq)
        node = path[-1]

        if node in visited:
            continue

        visited[node] = g
        explored.append(node)

        if node == GOAL:
            return path, explored

        for nb in get_neighbors(node):
            ng = g + 1
            nf = ng + heuristic(nb)
            heappush(pq, (nf, ng, path + [nb]))

    return [], explored

# =========================
# GIAO DIỆN TKINTER
# =========================

root = tk.Tk()
root.title("Maze Solver ")

canvas = tk.Canvas(
    root,
    width=COLS * CELL,
    height=ROWS * CELL,
    bg="white"
)
canvas.pack(pady=10)


def draw_maze():
    canvas.delete("all")

    for r in range(ROWS):
        for c in range(COLS):
            x1 = c * CELL
            y1 = r * CELL
            x2 = x1 + CELL
            y2 = y1 + CELL

            color = "white"
            if maze[r][c] == '#':
                color = "black"
            elif maze[r][c] == 'A':
                color = "green"
            elif maze[r][c] == 'G':
                color = "red"

            canvas.create_rectangle(
                x1, y1, x2, y2,
                fill=color,
                outline="gray"
            )

            text_color = "white" if maze[r][c] in ['#', 'A', 'G'] else "black"
            canvas.create_text(
                x1 + CELL / 2,
                y1 + CELL / 2,
                text=maze[r][c],
                fill=text_color,
                font=("Arial", 12, "bold")
            )


def show_result(path, explored):
    draw_maze()

    # Tô màu các ô đã duyệt qua (lightblue)
    for r, c in explored:
        if (r, c) != START and (r, c) != GOAL:
            x1 = c * CELL
            y1 = r * CELL
            canvas.create_rectangle(
                x1, y1,
                x1 + CELL, y1 + CELL,
                fill="lightblue",
                outline="gray"
            )

    # Tô màu đường đi tìm được (yellow)
    for r, c in path:
        if (r, c) != START and (r, c) != GOAL:
            x1 = c * CELL
            y1 = r * CELL
            canvas.create_rectangle(
                x1, y1,
                x1 + CELL, y1 + CELL,
                fill="yellow",
                outline="gray"
            )

    draw_special()

    path_length = len(path) - 1 if path else 0
    info.config(
        text=f"Path Length: {path_length} | Nodes Explored: {len(explored)}"
    )


def draw_special():
    sr, sc = START
    canvas.create_rectangle(
        sc * CELL, sr * CELL,
        sc * CELL + CELL, sr * CELL + CELL,
        fill="green",
        outline="gray"
    )
    canvas.create_text(
        sc * CELL + CELL / 2, sr * CELL + CELL / 2,
        text="A", fill="white", font=("Arial", 12, "bold")
    )

    gr, gc = GOAL
    canvas.create_rectangle(
        gc * CELL, gr * CELL,
        gc * CELL + CELL, gr * CELL + CELL,
        fill="red",
        outline="gray"
    )
    canvas.create_text(
        gc * CELL + CELL / 2, gr * CELL + CELL / 2,
        text="G", fill="white", font=("Arial", 12, "bold")
    )


def run_algorithm():
    algo = combo.get()
    path = []
    explored = []

    if algo == "BFS":
        path, explored = bfs()
    elif algo == "DFS":
        path, explored = dfs()
    elif algo == "UCS":
        path, explored = ucs()
    elif algo == "Greedy":
        path, explored = greedy()
    elif algo == "A*":
        path, explored = astar()

    show_result(path, explored)


frame = tk.Frame(root)
frame.pack()

combo = ttk.Combobox(
    frame,
    values=["BFS", "DFS", "UCS", "Greedy", "A*"],
    state="readonly"
)
combo.current(0)
combo.pack(side=tk.LEFT, padx=5)

btn = tk.Button(
    frame,
    text="Run",
    command=run_algorithm
)
btn.pack(side=tk.LEFT)

info = tk.Label(
    root,
    text="Choose algorithm and click Run",
    font=("Arial", 10)
)
info.pack(pady=10)

draw_maze()

root.mainloop()