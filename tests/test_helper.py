import sys
import os

parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)


from Tribute import Tribute
from Player import HumanPlayer
from Tribute import Tribute
from Resource import Resource
from Game import Game


def setupTestArena():

    game = Game(24, False, False, True)
    A = Tribute(0, (3, 3))
    B = Tribute(1, (16, 20))
    game.arena.tributes.extend ([A, B])
    p1 = HumanPlayer(A, game.arena)
    p2 = HumanPlayer(B, game.arena)
    game.players.extend ([p1, p2])

    # --- TREES ---
    trees = [(2, 5), (7, 2), (12, 2), (0, 11), (23, 4)]
    for pos in trees:
        game.arena.obstacles.append(pos)

    # --- WATER SOURCES (type 1) - 4x4 clusters ---
    # left cluster, upper left at (16, 4)
    water_positions = []
    for r in range(16, 20):
        for c in range(4, 8):
            water_positions.append((r, c))

    # right cluster, upper left at (2, 17)
    for r in range(2, 6):
        for c in range(17, 21):
            water_positions.append((r, c))

    for pos in water_positions:
        game.arena.resources.append(Resource(game.arena.next_resource_id, pos, Resource.Type(1)))
        game.arena.next_resource_id += 1

    # --- FOOD SOURCES (type 3) ---
    single_food = [(2, 10), (5, 6), (15, 6), (10, 18), (20, 17)]

    food_clusters = [(3, 10), (8, 8), (11, 17)]  # upper left cell of each 2x2
    cluster_food = [(r + dr, c + dc) for r, c in food_clusters for dr in range(2) for dc in range(2)]

    for pos in single_food + cluster_food:
        game.arena.resources.append(Resource(game.arena.next_resource_id, pos, Resource.Type(3)))
        game.arena.next_resource_id += 1

    # --- WEAPONS (type 5) ---
    weapons = [(3, 5, 10), (4, 1, 20), (18, 19, 10), (19, 20, 20)]  # (row, col, value)
    for r, c, val in weapons:
        game.arena.resources.append(Resource(game.arena.next_resource_id, (r, c), Resource.Type(5), val))
        game.arena.next_resource_id += 1

    # --- BACKPACKS ---
    game.arena.resources.append(Resource(game.arena.next_resource_id, (3, 1), Resource.Type(7)))   # large, near A
    game.arena.next_resource_id += 1
    game.arena.resources.append(Resource(game.arena.next_resource_id, (18, 21), Resource.Type(6))) # small, near B
    game.arena.next_resource_id += 1

    # --- UPDATE GRID ---
    for tribute in game.arena.tributes:
        game.arena.arena_grid[tribute.pos[0]][tribute.pos[1]] = tribute.letter

    for pos in game.arena.obstacles:
        game.arena.arena_grid[pos[0]][pos[1]] = 8

    for resource in game.arena.resources:
        game.arena.arena_grid[resource.pos[0]][resource.pos[1]] = resource.type.value

    return game


# def setupMidGameArena():
