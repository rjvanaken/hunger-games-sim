from Tribute import Tribute
from Player import HumanPlayer
from Tribute import Tribute
from Resource import Resource
from Game import Game


def setupTrainingArena():

    game = Game(48, True, True)
    A = Tribute(0, (4, 4))
    B = Tribute(1, (40, 42))
    game.arena.tributes.extend([A, B])
    p1 = HumanPlayer(A, game.arena)
    p2 = HumanPlayer(B, game.arena)
    game.players.extend([p1, p2])



    # --- TREES / OBSTACLES (20 total) ---
    trees = [
        (2,  8),  (3,  20), (5,  35), (6,  14),
        (9,  2),  (11, 28), (13, 42), (15, 10),
        (18, 22), (20, 38), (22, 5),  (24, 17),
        (27, 32), (29, 8),  (31, 44), (33, 20),
        (36, 12), (38, 36), (42, 26), (45, 6),
    ]
    for pos in trees:
        game.arena.obstacles.append(pos)

    # --- WATER SOURCES (type 1) - 4x4 clusters, 3 total ---
    water_positions = []

    # cluster 1: lower-left area, upper left at (32, 6)
    for r in range(32, 36):
        for c in range(6, 10):
            water_positions.append((r, c))

    # cluster 2: upper-right area, upper left at (4, 36)
    for r in range(4, 8):
        for c in range(36, 40):
            water_positions.append((r, c))

    # cluster 3: center area, upper left at (20, 22)
    for r in range(20, 24):
        for c in range(22, 26):
            water_positions.append((r, c))

    for pos in water_positions:
        game.arena.resources.append(Resource(game.arena.next_resource_id, pos, Resource.Type(1)))
        game.arena.next_resource_id += 1

    # --- FOOD SOURCES (type 3) ---
    single_food = [
        (3,  12), (7,  28), (10, 6),  (14, 38),
        (17, 15), (25, 40), (30, 10), (35, 30),
        (40, 8),  (44, 34),
    ]

    food_clusters = [
        (8,  10), (16, 30), (28, 18), (37, 40)  # upper-left of each 2x2
    ]
    cluster_food = [(r + dr, c + dc) for r, c in food_clusters for dr in range(2) for dc in range(2)]

    for pos in single_food + cluster_food:
        game.arena.resources.append(Resource(game.arena.next_resource_id, pos, Resource.Type(3)))
        game.arena.next_resource_id += 1

    # --- WEAPONS (type 5) ---
    weapons = [
        (5,  6,  10), (6,  2,  20),
        (30, 44, 10), (31, 42, 20),
        (22, 12, 15),
    ]
    for r, c, val in weapons:
        game.arena.resources.append(Resource(game.arena.next_resource_id, (r, c), Resource.Type(5), val))
        game.arena.next_resource_id += 1

    # --- BACKPACKS ---
    game.arena.resources.append(Resource(game.arena.next_resource_id, (4, 2),   Resource.Type(7)))  # large, near A
    game.arena.next_resource_id += 1
    game.arena.resources.append(Resource(game.arena.next_resource_id, (42, 44), Resource.Type(6)))  # small, near B
    game.arena.next_resource_id += 1

    # --- UPDATE GRID ---
    for tribute in game.arena.tributes:
        game.arena.arena_grid[tribute.pos[0]][tribute.pos[1]] = tribute.letter

    for pos in game.arena.obstacles:
        game.arena.arena_grid[pos[0]][pos[1]] = 8

    for resource in game.arena.resources:
        game.arena.arena_grid[resource.pos[0]][resource.pos[1]] = resource.type.value
        
    game.arena.displayArena()

    return game