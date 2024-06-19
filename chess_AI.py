import random


# Plays a random move from the valid move set. Note that this AI doesn't know how to castle.
def find_random_move(valid_moves):
    flattened_valid_moves = [move
                             for moves in valid_moves
                             for move in moves]

    index = random.randint(0, len(flattened_valid_moves) - 1)
    count = 0
    selection = -1
    for moves in valid_moves:
        selection += 1
        for move in moves:
            if count == index:
                return selection, move
            count += 1

    return -1, (-1, -1)
