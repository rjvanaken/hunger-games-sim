from Tribute import Tribute
from Player import HumanPlayer
from Resource import Resource
from Game import Game

WALL = 10  # inner wall boundary — effective arena is rows/cols 10–38

def setupTrainingArena():

    game = Game(48, True, True)
    A = Tribute(0, (20, 20))
    B = Tribute(1, (24, 24))
    game.arena.tributes.extend([A, B])
    p1 = HumanPlayer(A, game.arena)
    p2 = HumanPlayer(B, game.arena)
    game.players.extend([p1, p2])

    # --- INNER WALL (shrinks effective arena to rows/cols 10-38) ---
    inner_wall = (
        [(WALL, c) for c in range(WALL, 48 - WALL)] +      # top inner wall
        [(48 - WALL - 1, c) for c in range(WALL, 48 - WALL)] +  # bottom inner wall
        [(r, WALL) for r in range(WALL, 48 - WALL)] +      # left inner wall
        [(r, 48 - WALL - 1) for r in range(WALL, 48 - WALL)]    # right inner wall
    )

    # --- INTERIOR TREES (shifted into center zone) ---
    interior_trees = [
        (12, 14), (12, 24), (13, 32),
        (16, 12), (16, 30), (18, 20),
        (22, 13), (22, 35), (25, 18),
        (28, 14), (28, 28), (30, 22),
        (32, 16), (32, 32), (34, 12),
        (15, 22), (20, 35), (26, 12),
        (29, 35), (33, 25),
    ]

    for pos in inner_wall + interior_trees:
        game.arena.obstacles.append(pos)

    # --- WATER SOURCES (type 1) - 4x4 clusters, all in center zone ---
    water_positions = []

    # cluster 1: lower-left of center, upper left at (30, 13)
    for r in range(30, 34):
        for c in range(13, 17):
            water_positions.append((r, c))

    # cluster 2: upper-right of center, upper left at (13, 31)
    for r in range(13, 17):
        for c in range(31, 35):
            water_positions.append((r, c))

    # cluster 3: mid-center, upper left at (21, 22)
    for r in range(21, 25):
        for c in range(22, 26):
            water_positions.append((r, c))

    for pos in water_positions:
        game.arena.resources.append(Resource(game.arena.next_resource_id, pos, Resource.Type(1)))
        game.arena.next_resource_id += 1

    # --- FOOD SOURCES (type 3) ---
    single_food = [
        (13, 15), (14, 28), (17, 13), (19, 33),
        (23, 14), (26, 33), (31, 18), (33, 30),
    ]

    food_clusters = [
        (15, 20), (20, 30), (27, 15), (30, 28)  # upper-left of each 2x2
    ]
    cluster_food = [(r + dr, c + dc) for r, c in food_clusters for dr in range(2) for dc in range(2)]

    for pos in single_food + cluster_food:
        game.arena.resources.append(Resource(game.arena.next_resource_id, pos, Resource.Type(3)))
        game.arena.next_resource_id += 1

    # --- WEAPONS (type 5) ---
    weapons = [
        (14, 18, 10), (15, 14, 20),
        (31, 30, 10), (32, 28, 20),
        (22, 22, 15),  # center weapon
    ]
    for r, c, val in weapons:
        game.arena.resources.append(Resource(game.arena.next_resource_id, (r, c), Resource.Type(5), val))
        game.arena.next_resource_id += 1

    # --- BACKPACKS ---
    game.arena.resources.append(Resource(game.arena.next_resource_id, (19, 19), Resource.Type(7)))  # large, near A
    game.arena.next_resource_id += 1
    game.arena.resources.append(Resource(game.arena.next_resource_id, (25, 25), Resource.Type(6)))  # small, near B
    game.arena.next_resource_id += 1

    # --- UPDATE GRID ---
    for tribute in game.arena.tributes:
        game.arena.arena_grid[tribute.pos[0]][tribute.pos[1]] = tribute.letter

    for pos in game.arena.obstacles:
        game.arena.arena_grid[pos[0]][pos[1]] = 8

    for resource in game.arena.resources:
        game.arena.arena_grid[resource.pos[0]][resource.pos[1]] = resource.type.value

    return game