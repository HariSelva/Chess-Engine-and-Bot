# Check all the possible moves for each piece on the board not taking into account checks.
def check_options(turn, last_moved, en_passant_coords, ally_pieces, ally_positions, enemy_positions):
    moves_list = []
    all_moves_list = []

    for i in range(len(ally_pieces)):
        piece = ally_pieces[i]
        position = ally_positions[i]
        if piece == 'pawn':
            moves_list, en_passant_coords = check_pawn(position, turn, last_moved, en_passant_coords,
                                                       ally_positions, enemy_positions)
        elif piece == 'queen':
            moves_list = check_queen(position, ally_positions, enemy_positions)
        elif piece == 'king':
            moves_list = check_king(position, ally_positions)
        elif piece == 'knight':
            moves_list = check_knight(position, ally_positions)
        elif piece == 'rook':
            moves_list = check_rook(position, ally_positions, enemy_positions)
        elif piece == 'bishop':
            moves_list = check_bishop(position, ally_positions, enemy_positions)
        all_moves_list.append(moves_list)

    return all_moves_list, en_passant_coords


# Checks for all moves of the given pawn
def check_pawn(position, turn, last_moved, en_passant_coords, ally_positions, enemy_positions):
    moves_list = []
    pawn_x = position[0]
    pawn_y = position[1]
    if turn == 'white':
        # Move pawn forward 1 space
        if (pawn_x, pawn_y + 1) not in enemy_positions and (pawn_x, pawn_y + 1) not in ally_positions and pawn_y < 7:
            moves_list.append((pawn_x, pawn_y + 1))

            # Move pawn forward 2 space during its first move
            if (pawn_x, pawn_y + 2) not in enemy_positions and (pawn_x, pawn_y + 2) not in ally_positions \
                    and pawn_y == 1:
                moves_list.append((pawn_x, pawn_y + 2))

        # Move diagonally 1 space to capture an enemy piece
        if (pawn_x + 1, pawn_y + 1) in enemy_positions:
            moves_list.append((pawn_x + 1, pawn_y + 1))
        if (pawn_x - 1, pawn_y + 1) in enemy_positions:
            moves_list.append((pawn_x - 1, pawn_y + 1))

        # En Passant
        if pawn_y == 4 and last_moved[0] == 'pawn' and last_moved[1][1] == 6 and last_moved[2][1] == 4 and \
                abs(last_moved[1][0] - pawn_x) == 1:
            en_passant_coords = (last_moved[2][0], 5)
            moves_list.append(en_passant_coords)

    else:  # Black's turn
        # Move pawn forward 1 space
        if (pawn_x, pawn_y - 1) not in enemy_positions and (pawn_x, pawn_y - 1) not in ally_positions and pawn_y > 0:
            moves_list.append((pawn_x, pawn_y - 1))

            # Move pawn forward 2 space during its first move
            if (pawn_x, pawn_y - 2) not in enemy_positions and (pawn_x, pawn_y - 2) not in ally_positions \
                    and pawn_y == 6:
                moves_list.append((pawn_x, pawn_y - 2))

        # Move diagonally 1 space to capture an enemy piece
        if (pawn_x + 1, pawn_y - 1) in enemy_positions:
            moves_list.append((pawn_x + 1, pawn_y - 1))
        if (pawn_x - 1, pawn_y - 1) in enemy_positions:
            moves_list.append((pawn_x - 1, pawn_y - 1))

        # En Passant
        if pawn_y == 3 and last_moved[0] == 'pawn' and last_moved[1][1] == 1 and last_moved[2][1] == 3 and \
                abs(last_moved[1][0] - pawn_x) == 1:
            en_passant_coords = (last_moved[2][0], 2)
            moves_list.append(en_passant_coords)

    return moves_list, en_passant_coords


# Checks for all moves of the given queen
def check_queen(position, ally_positions, enemy_positions):
    # Use functions for check bishop and rook moves as the queen has the combined functionality of both pieces
    moves_list = check_bishop(position, ally_positions, enemy_positions)
    temp_moves_list = check_rook(position, ally_positions, enemy_positions)

    for moves in temp_moves_list:
        moves_list.append(moves)

    return moves_list


# Checks for all moves of the given king
def check_king(position, ally_positions):
    moves_list = []
    king_x = position[0]
    king_y = position[1]

    # Relative changes in position for each of the 8 position a king can reach by moving 1 tile in any direction
    delta = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        new_pos = (king_x + delta[i][0], king_y + delta[i][1])
        if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7 and new_pos not in ally_positions:
            moves_list.append(new_pos)

    return moves_list


# Checks for all moves of the given knight
def check_knight(position, ally_positions):
    moves_list = []
    knight_x = position[0]
    knight_y = position[1]

    # Relative changes in position for each of the 8 position a knight can reach by going 2 tiles in the one direction
    # and 1 in the perpendicular direction
    delta = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        new_pos = (knight_x + delta[i][0], knight_y + delta[i][1])
        if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7 and new_pos not in ally_positions:
            moves_list.append(new_pos)

    return moves_list


# Checks for all moves of the given rook
def check_rook(position, ally_positions, enemy_positions):
    moves_list = []
    rook_x = position[0]
    rook_y = position[1]

    for i in range(4):
        if i == 1:  # Move right
            delta_x = 1
            delta_y = 0
        elif i == 2:  # Move left
            delta_x = -1
            delta_y = 0
        elif i == 3:  # Move down
            delta_x = 0
            delta_y = 1
        else:  # i == 4  # Move up
            delta_x = 0
            delta_y = -1

        path = True

        # Coordinates for the various possible titles that the selected piece can move to, initially set to the current
        # position of the selected piece
        new_x = rook_x
        new_y = rook_y
        while path:
            new_x = new_x + delta_x
            new_y = new_y + delta_y
            if 0 <= new_x <= 7 and 0 <= new_y <= 7 and (new_x, new_y) not in ally_positions:
                moves_list.append((new_x, new_y))

                # If piece has encountered an enemy piece, it cannot go any further
                if (new_x, new_y) in enemy_positions:
                    path = False
            else:  # If piece has encountered the end of the board or an allied piece, it cannot go any further
                path = False

    return moves_list


# Checks for all moves of the given bishop
def check_bishop(position, ally_positions, enemy_positions):
    moves_list = []
    bishop_x = position[0]
    bishop_y = position[1]

    for i in range(4):
        if i == 1:  # Move right-down
            delta_x = 1
            delta_y = 1
        elif i == 2:  # Move left-down
            delta_x = -1
            delta_y = 1
        elif i == 3:  # Move right-up
            delta_x = 1
            delta_y = -1
        else:  # i == 4  # Move left-up
            delta_x = -1
            delta_y = -1

        path = True

        # Coordinates for the various possible titles that the selected piece can move to, initially set to the current
        # position of the selected piece
        new_x = bishop_x
        new_y = bishop_y
        while path:
            new_x = new_x + delta_x
            new_y = new_y + delta_y
            if 0 <= new_x <= 7 and 0 <= new_y <= 7 and (new_x, new_y) not in ally_positions:
                moves_list.append((new_x, new_y))

                # If piece has encountered an enemy piece, it cannot go any further
                if (new_x, new_y) in enemy_positions:
                    path = False
            else:  # If piece has encountered the end of the board or an allied piece, it cannot go any further
                path = False

    return moves_list


# Looks for pieces that are pinned due to an attacking enemy piece.
# It also looks for pieces that are attacking the king (aka check).
def check_pins_and_checks(turn, king_position, ally_positions, enemy_pieces, enemy_positions):
    pins = []
    checks = []
    in_check = False

    # Look outwards from king for pins and checks, while keeping track of pinned pieces
    # directions = left,    up,      right,  down, up-left, down-left, up-right, down-right
    directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
    for d, direction in enumerate(directions):
        possible_pin = ()
        for i in range(1, 8):
            new_pos = (king_position[0] + direction[0] * i, king_position[1] + direction[1] * i)
            if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                if new_pos in ally_positions:  # and not king
                    if possible_pin == ():  # first allied piece might be a pinned piece
                        possible_pin = (new_pos[0], new_pos[1], direction[0], direction[1])
                    else:  # Found a second allied piece, which means there is no check or pin in this direction
                        break
                elif new_pos in enemy_positions:
                    index = enemy_positions.index(new_pos)
                    enemy_type = enemy_pieces[index]

                    # 5 possibilities in this complex conditional
                    # 1. Horizontally or Vertically away from king and piece is a rook
                    # 2. Diagonally away from king and piece is a bishop
                    # 3. 1 square away diagonally from king and piece is a pawn.
                    #    Note the differing directions based on whose turn it is
                    # 4. Any direction and piece is a queen
                    # 5. Any direction 1 square away and piece is a king
                    if (0 <= d <= 3 and enemy_type == 'rook') \
                            or (4 <= d <= 7 and enemy_type == 'bishop') \
                            or (i == 1 and enemy_type == 'pawn' and
                                ((turn == 'white' and (d == 5 or d == 7)) or
                                 (turn == 'black' and (d == 4 or d == 6)))) \
                            or (enemy_type == 'queen') \
                            or (i == 1 and enemy_type == 'king'):
                        if possible_pin == ():  # No piece blocking, so check
                            in_check = True
                            checks.append((new_pos[0], new_pos[1], direction[0], direction[1]))
                            break
                        else:  # There is a piece blocking this check, so it is a pinned piece
                            pins.append(possible_pin)
                            break
                    else:  # enemy piece that isn't applying a check
                        break
            else:  # Coordinates out of board bounds
                break

    # Check for knight checks
    knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
    for move in knight_moves:
        new_pos = (king_position[0] + move[0], king_position[1] + move[1])
        if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
            if new_pos in enemy_positions:
                index = enemy_positions.index(new_pos)
                enemy_type = enemy_pieces[index]
                if enemy_type == 'knight':
                    in_check = True
                    checks.append((new_pos[0], new_pos[1], move[0], move[1]))

    return in_check, pins, checks


# Removes invalid moves from the options list. Invalid moves are moves that would put the king in check.
def trim_invalid_moves(turn, king_position, ally_pieces, ally_positions, ally_options,
                       enemy_pieces, enemy_positions):
    in_check, pins, checks = check_pins_and_checks(turn, king_position, ally_positions, enemy_pieces, enemy_positions)
    king_index = ally_positions.index(king_position)

    if in_check:
        # If the king is being checked by only 1 enemy, you can capture the piece, block the check, or move the king
        if len(checks) == 1:
            check_pos = (checks[0][0],  checks[0][1])
            check_dir = (checks[0][2],  checks[0][3])
            index = enemy_positions.index(check_pos)
            checking_piece = enemy_pieces[index]
            valid_squares = []  # squares that pieces can legally move to

            # If the checking piece is a knight, the option to block no longer exists.
            # You can only capture or move the king
            if checking_piece == 'knight':
                valid_squares = [check_pos]
            else:
                for i in range(1, 8):
                    valid_square = (king_position[0] + check_dir[0] * i, king_position[1] + check_dir[1] * i)
                    valid_squares.append(valid_square)
                    if valid_square == check_pos:  # The valid squares ends when you get to the checking piece
                        break

            # Get rid of any moves that don't block check
            for i in range(len(ally_options)):
                if i == king_index:
                    trim_invalid_king_moves(turn, king_index, ally_positions, ally_options,
                                            enemy_pieces, enemy_positions)
                else:
                    # Iterate through the list backwards, while removing corresponding elements
                    for j in range(len(ally_options[i]) - 1, -1, -1):
                        if ally_options[i][j] not in valid_squares:
                            ally_options[i].pop(j)

        # More than 1 piece causing check. This is when there is a double check (triple and more are impossible).
        # In this case, the king is forced to move. Thus, remove all moves from other pieces.
        else:
            for i in range(len(ally_options)):
                if i == king_index:
                    trim_invalid_king_moves(turn, king_index, ally_positions, ally_options,
                                            enemy_pieces, enemy_positions)
                else:
                    ally_options[i] = []
    else:  # If the king is not in check, we still need to trim the kings moves to ensure it doesn't move into check
        trim_invalid_king_moves(turn, king_index, ally_positions, ally_options, enemy_pieces, enemy_positions)

    # Check through pinned pieces and trim invalid moves.
    # These pieces can only move along the path of check, as they need to continue blocking the attacking piece.
    # If in check, these pieces may not have any moves to trim as they will have been trimmed in the earlier step.
    for pin in pins:
        pin_pos = (pin[0], pin[1])
        pin_dir = (pin[2], pin[3])
        negative_pin_dir = (-pin[2], -pin[3])

        pinned_piece_index = ally_positions.index(pin_pos)
        pinned_piece = ally_pieces[pinned_piece_index]

        # A knight moves in an 'L' shape, and thus, it cannot move and still be blocking they path of check.
        # As such all its moves an invalid, since they all lead to the king being in check
        if pinned_piece == 'knight':
            ally_options[pinned_piece_index] = []
        else:
            for j in range(len(ally_options[pinned_piece_index]) - 1, -1, -1):
                move = ally_options[pinned_piece_index][j]
                distance = (move[0] - pin_pos[0], move[1] - pin_pos[1])
                #  Ensure we aren't dividing by zero
                if distance[0] == 0:
                    dir_x = 0
                else:
                    dir_x = distance[0] / abs(distance[0])
                if distance[1] == 0:
                    dir_y = 0
                else:
                    dir_y = distance[1] / abs(distance[1])
                direction = (dir_x, dir_y)
                # If this move is not along the path of check, it is invalid and needs to be removed
                if direction != pin_dir and direction != negative_pin_dir:
                    ally_options[pinned_piece_index].pop(j)


# Removes the king's invalid moves from the options list. Invalid moves are those where the king moves into check.
def trim_invalid_king_moves(turn, king_index, ally_positions, ally_options, enemy_pieces, enemy_positions):
    moves_to_remove = []
    for i in range(len(ally_options[king_index])):
        move = ally_options[king_index][i]

        # Make a copy of required lists
        copy_ally_positions = list(ally_positions)
        copy_enemy_pieces = list(enemy_pieces)
        copy_enemy_positions = list(enemy_positions)

        # Pretend to move to this square
        copy_ally_positions[king_index] = move
        if move in enemy_positions:
            # Temporarily complete the capturing of enemy
            captured_index = enemy_positions.index(move)
            copy_enemy_pieces.pop(captured_index)
            copy_enemy_positions.pop(captured_index)

        # Recalculate whether king is in check or not, if so add to removal list
        in_check, _, _ = check_pins_and_checks(turn, move, copy_ally_positions, copy_enemy_pieces, copy_enemy_positions)
        if in_check:
            moves_to_remove.append(i)

    # Iterate through the list backwards and remove the corresponding moves
    for move in moves_to_remove[::-1]:
        ally_options[king_index].pop(move)


# Updates the castling state - whether king/queen side (or neither) are available to castle
def update_castling_state(piece_moved, original_position, state):
    if state == 3:  # Castling is no longer available, state cannot change
        return state
    if piece_moved == 'king':  # As the king has moved, castling is no longer available
        return 3
    if piece_moved == 'rook':
        if original_position[0] == 0:  # King side rook has moved
            if state == 0:
                return 2  # Only Queen side castling is available
            elif state == 1:
                return 3  # No more castling is available
        if original_position[0] == 7:  # Queen side rook has moved
            if state == 0:
                return 1  # Only King side castling is available
            elif state == 2:
                return 3  # No more castling is available
    return state


# Checks if the king can complete a castling operation - castling availability (aka state), under checks, and open path
def check_castling(turn, king_position, castling_state, under_check, ally_positions, enemy_pieces, enemy_positions):

    if castling_state == 3:
        return []
    if under_check:
        return []

    castling_options = []  # store each valid castle move as [(king_coords)]]

    if castling_state == 0 or castling_state == 1:
        castling = True
        squares_to_check = [(king_position[0] - 1, king_position[1]), (king_position[0] - 2, king_position[1])]
        # Check if these squares have a piece on them. If so castling not possible
        if (squares_to_check[0] in ally_positions or squares_to_check[0] in enemy_positions) or \
                (squares_to_check[1] in ally_positions or squares_to_check[1] in enemy_positions):
            castling = False
        else:  # Squares are empty. Thus, check if king will move through or end in check.
            king_index = ally_positions.index(king_position)
            for square in squares_to_check:

                # Make a copy of required list
                copy_ally_positions = list(ally_positions)

                # Pretend to move to this square
                copy_ally_positions[king_index] = square

                # Recalculate whether king is in check or not, if so add to removal list
                in_check, _, _ = check_pins_and_checks(turn, square, copy_ally_positions, enemy_pieces,
                                                       enemy_positions)
                if in_check:
                    castling = False

        if castling:
            castling_options.append((king_position[0] - 2, king_position[1]))
    if castling_state == 0 or castling_state == 2:
        castling = True
        squares_to_check = [(king_position[0] + 1, king_position[1]), (king_position[0] + 2, king_position[1])]
        # Check if these squares have a piece on them. If so castling not possible
        if (squares_to_check[0] in ally_positions or squares_to_check[0] in enemy_positions) or \
                (squares_to_check[1] in ally_positions or squares_to_check[1] in enemy_positions):
            castling = False
        else:  # Squares are empty. Thus, check if king will move through or end in check.
            king_index = ally_positions.index(king_position)
            for square in squares_to_check:

                # Make a copy of required list
                copy_ally_positions = list(ally_positions)

                # Pretend to move to this square
                copy_ally_positions[king_index] = square

                # Recalculate whether king is in check or not, if so add to removal list
                in_check, _, _ = check_pins_and_checks(turn, square, copy_ally_positions, enemy_pieces,
                                                       enemy_positions)
                if in_check:
                    castling = False

        if castling:
            castling_options.append((king_position[0] + 2, king_position[1]))
    return castling_options
