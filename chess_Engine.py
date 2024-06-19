class Player:
    def __init__(self, colour, top_or_bot, positions, images, small_images, forfeit_bounds, ai_or_not):
        self.colour = colour

        self.pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                       'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
        self.images = images
        self.small_images = small_images

        self.top_or_bot = top_or_bot
        if top_or_bot == 'top':
            i = 0
            pawn_direction = 1  # Down the board
            self.forfeit_button_boundary = forfeit_bounds[0]
        else:  # bottom
            i = 1
            pawn_direction = -1  # Up the board
            self.forfeit_button_boundary = forfeit_bounds[1]
        if colour == 'black':
            i += 2
        self.positions = list(positions[i])  # Make a copy of the given position array

        self.king_position = self.positions[3]

        self.captured_pieces = []
        self.options = []

        # 0-Both castling moves are available; 1-Only King side available;
        # 2-Only Queen side available; 3-Neither is available
        self.castling_state = 0
        self.castling_options = []  # store each valid castle move as [(king_coords)]]

        # Whether a pawn needs to be promoted and the index pointing to that pawn
        self.promotion = False
        self.pawn_to_promo = -1

        self.pawn_direction = pawn_direction
        self.pawn_promo_row = 7 - self.king_position[1]
        self.pawn_start_row = self.positions[-1][1]
        self.en_passant_coords = (-1, -1)

        self.under_check = False
        self.ai = ai_or_not

    # Check all the possible moves for each piece on the board not taking into account checks.
    def check_options(self, last_moved, enemy_positions, enemy_pieces):
        moves_list = []
        self.options = []
        self.en_passant_coords = (-1, -1)

        for i in range(len(self.pieces)):
            piece = self.pieces[i]
            position = self.positions[i]
            if piece == 'pawn':
                moves_list = self.check_pawn(position, last_moved, enemy_positions)
            elif piece == 'queen':
                moves_list = self.check_queen(position, enemy_positions)
            elif piece == 'king':
                moves_list = self.check_king(position, enemy_positions, enemy_pieces)
            elif piece == 'knight':
                moves_list = self.check_knight(position)
            elif piece == 'rook':
                moves_list = self.check_rook(position, enemy_positions)
            elif piece == 'bishop':
                moves_list = self.check_bishop(position, enemy_positions)

            self.options.append(moves_list)

    # Checks for all moves of the given pawn
    def check_pawn(self, position, last_moved, enemy_positions):
        moves_list = []
        pawn_x = position[0]
        pawn_y = position[1]

        # Move pawn forward 1 space
        if (pawn_x, pawn_y + self.pawn_direction) not in enemy_positions and \
                (pawn_x, pawn_y + self.pawn_direction) not in self.positions and 0 <= pawn_y <= 7:
            moves_list.append((pawn_x, pawn_y + self.pawn_direction))

            # Move pawn forward 2 space during its first move
            if (pawn_x, pawn_y + 2 * self.pawn_direction) not in enemy_positions and \
                    (pawn_x, pawn_y + 2 * self.pawn_direction) not in self.positions and pawn_y == self.pawn_start_row:
                moves_list.append((pawn_x, pawn_y + 2 * self.pawn_direction))

        # Move diagonally 1 space to capture an enemy piece
        if (pawn_x + 1, pawn_y + self.pawn_direction) in enemy_positions:
            moves_list.append((pawn_x + 1, pawn_y + self.pawn_direction))
        if (pawn_x - 1, pawn_y + self.pawn_direction) in enemy_positions:
            moves_list.append((pawn_x - 1, pawn_y + self.pawn_direction))

        # En Passant
        # Your pawn needs to be 2 rows in front of the opponents starting pawn row
        # Opponent should've moved a pawn in the last turn
        # Opponent moved their pawn two spaces, and it is to 1 space left/right of your pawn
        if pawn_y == self.pawn_promo_row - (3 * self.pawn_direction) and last_moved[0] == 'pawn' \
                and abs(last_moved[2][1] - last_moved[1][1]) == 2 and abs(last_moved[1][0] - pawn_x) == 1:
            self.en_passant_coords = (last_moved[2][0], pawn_y + self.pawn_direction)
            moves_list.append(self.en_passant_coords)

        return moves_list

    # Checks for all moves of the given queen
    def check_queen(self, position, enemy_positions):
        # Use functions for check bishop and rook moves as the queen has the combined functionality of both pieces
        moves_list = self.check_bishop(position, enemy_positions)
        temp_moves_list = self.check_rook(position, enemy_positions)

        for moves in temp_moves_list:
            moves_list.append(moves)

        return moves_list

    # Checks for all moves of the given king
    def check_king(self, position, enemy_positions, enemy_pieces):
        moves_list = []
        king_x = position[0]
        king_y = position[1]

        # Relative changes in position for each of the 8 position a king can reach by moving 1 tile in any direction
        delta = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
        for i in range(8):
            new_pos = (king_x + delta[i][0], king_y + delta[i][1])
            if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7 and new_pos not in self.positions:
                moves_list.append(new_pos)

        for coord in self.check_castling(enemy_pieces, enemy_positions):
            moves_list.append(coord)

        return moves_list

    # Checks for all moves of the given knight
    def check_knight(self, position):
        moves_list = []
        knight_x = position[0]
        knight_y = position[1]

        # Relative changes in position for each of the 8 position a knight can reach by going 2 tiles in the one
        # direction and 1 tile in the perpendicular direction
        delta = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
        for i in range(8):
            new_pos = (knight_x + delta[i][0], knight_y + delta[i][1])
            if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7 and new_pos not in self.positions:
                moves_list.append(new_pos)

        return moves_list

    # Checks for all moves of the given rook
    def check_rook(self, position, enemy_positions):
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

            # Coordinates for the various possible titles that the selected piece can move to, initially set to the
            # current position of the selected piece
            new_x = rook_x
            new_y = rook_y
            while path:
                new_x = new_x + delta_x
                new_y = new_y + delta_y
                if 0 <= new_x <= 7 and 0 <= new_y <= 7 and (new_x, new_y) not in self.positions:
                    moves_list.append((new_x, new_y))

                    # If piece has encountered an enemy piece, it cannot go any further
                    if (new_x, new_y) in enemy_positions:
                        path = False
                else:  # If piece has encountered the end of the board or an allied piece, it cannot go any further
                    path = False

        return moves_list

    # Checks for all moves of the given bishop
    def check_bishop(self, position, enemy_positions):
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

            # Coordinates for the various possible titles that the selected piece can move to, initially set to the
            # current position of the selected piece
            new_x = bishop_x
            new_y = bishop_y
            while path:
                new_x = new_x + delta_x
                new_y = new_y + delta_y
                if 0 <= new_x <= 7 and 0 <= new_y <= 7 and (new_x, new_y) not in self.positions:
                    moves_list.append((new_x, new_y))

                    # If piece has encountered an enemy piece, it cannot go any further
                    if (new_x, new_y) in enemy_positions:
                        path = False
                else:  # If piece has encountered the end of the board or an allied piece, it cannot go any further
                    path = False

        return moves_list

    # Updates the castling state - whether king/queen side (or neither) are available to castle
    def update_castling_state(self, piece_moved, original_position):
        if self.castling_state != 3:  # Castling is still available in some manner
            if piece_moved == 'king':  # As the king has moved, castling is no longer available
                self.castling_state = 3
            elif piece_moved == 'rook':
                if original_position[0] == 0:  # King side rook has moved
                    if self.castling_state == 0:
                        self.castling_state = 2  # Only Queen side castling is available
                    elif self.castling_state == 1:
                        self.castling_state = 3  # No more castling is available
                elif original_position[0] == 7:  # Queen side rook has moved
                    if self.castling_state == 0:
                        self.castling_state = 1  # Only King side castling is available
                    elif self.castling_state == 2:
                        self.castling_state = 3  # No more castling is available

    # Checks if the king can complete a castling operation based on castling availability (aka castling state),
    # under checks, and open path
    def check_castling(self, enemy_pieces, enemy_positions):
        self.castling_options = []
        if self.castling_state == 3:
            return []
        if self.under_check:
            return []

        if self.castling_state == 0 or self.castling_state == 1:
            castling = True
            squares_to_check = [(self.king_position[0] - 1, self.king_position[1]),
                                (self.king_position[0] - 2, self.king_position[1])]
            # Check if these squares have a piece on them. If so castling not possible
            if (squares_to_check[0] in self.positions or squares_to_check[0] in enemy_positions) or \
                    (squares_to_check[1] in self.positions or squares_to_check[1] in enemy_positions):
                castling = False
            else:  # Squares are empty. Thus, check if king will move through or end in check.
                king_index = self.positions.index(self.king_position)
                for square in squares_to_check:

                    # Make a copy of required list
                    copy_ally_positions = list(self.positions)

                    # Pretend to move to this square
                    copy_ally_positions[king_index] = square

                    # Recalculate whether king is in check or not, if so can't castle
                    will_be_in_check = self.check_checks(square, copy_ally_positions, enemy_pieces, enemy_positions)
                    if will_be_in_check:
                        castling = False

            if castling:
                self.castling_options.append((self.king_position[0] - 2, self.king_position[1]))
        if self.castling_state == 0 or self.castling_state == 2:
            castling = True
            squares_to_check = [(self.king_position[0] + 1, self.king_position[1]),
                                (self.king_position[0] + 2, self.king_position[1])]
            # Check if these squares have a piece on them. If so castling not possible
            if (squares_to_check[0] in self.positions or squares_to_check[0] in enemy_positions) or \
                    (squares_to_check[1] in self.positions or squares_to_check[1] in enemy_positions):
                castling = False
            else:  # Squares are empty. Thus, check if king will move through or end in check.
                king_index = self.positions.index(self.king_position)
                for square in squares_to_check:

                    # Make a copy of required list
                    copy_ally_positions = list(self.positions)

                    # Pretend to move to this square
                    copy_ally_positions[king_index] = square

                    # Recalculate whether king is in check or not, if so add to removal list
                    will_be_in_check = self.check_checks(square, copy_ally_positions, enemy_pieces, enemy_positions)
                    if will_be_in_check:
                        castling = False

            if castling:
                self.castling_options.append((self.king_position[0] + 2, self.king_position[1]))

        return self.castling_options

    # Check whether king is in check
    def check_checks(self, king_position, ally_positions, enemy_pieces, enemy_positions):
        in_check = False

        # Look outwards from king for pins and checks, while keeping track of pinned pieces
        # directions = left,    up,      right,  down, up-left, down-left, up-right, down-right
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for d, direction in enumerate(directions):
            for i in range(1, 8):
                new_pos = (king_position[0] + direction[0] * i, king_position[1] + direction[1] * i)
                if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                    # Note we will never check the king's current position so additional condition isn't required
                    if new_pos in ally_positions:
                        # Found an allied piece, which means there is no check in this direction
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
                                    (direction[1] == self.pawn_direction and abs(direction[0]) == 1)) \
                                or (enemy_type == 'queen') \
                                or (i == 1 and enemy_type == 'king'):
                            in_check = True
                        break  # Stopping checking in this direction, as the enemy piece is either applying check or not
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

        return in_check

    # Looks for pieces that are pinned due to an attacking enemy piece.
    # It also looks for pieces that are attacking the king (aka check).
    def check_pins_and_checks(self, enemy_pieces, enemy_positions):
        pins = []
        checks = []
        self.under_check = False

        # Look outwards from king for pins and checks, while keeping track of pinned pieces
        # directions = left,    up,      right,  down, up-left, down-left, up-right, down-right
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for d, direction in enumerate(directions):
            possible_pin = ()
            for i in range(1, 8):
                new_pos = (self.king_position[0] + direction[0] * i, self.king_position[1] + direction[1] * i)
                if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                    # Note we will never check the king's current position so additional condition isn't required
                    if new_pos in self.positions:
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
                                    (direction[1] == self.pawn_direction and abs(direction[0]) == 1)) \
                                or (enemy_type == 'queen') \
                                or (i == 1 and enemy_type == 'king'):
                            if possible_pin == ():  # No piece blocking, so check
                                self.under_check = True
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
            new_pos = (self.king_position[0] + move[0], self.king_position[1] + move[1])
            if 0 <= new_pos[0] <= 7 and 0 <= new_pos[1] <= 7:
                if new_pos in enemy_positions:
                    index = enemy_positions.index(new_pos)
                    enemy_type = enemy_pieces[index]
                    if enemy_type == 'knight':
                        self.under_check = True
                        checks.append((new_pos[0], new_pos[1], move[0], move[1]))

        return pins, checks

    # Removes invalid moves from the options list. Invalid moves are moves that would put the king in check.
    def trim_invalid_moves(self, enemy_pieces, enemy_positions):
        pins, checks = self.check_pins_and_checks(enemy_pieces, enemy_positions)
        king_index = self.positions.index(self.king_position)

        if self.under_check:
            # If the king is being checked by only 1 enemy, you can capture the piece, block the check, or move the king
            if len(checks) == 1:
                check_pos = (checks[0][0], checks[0][1])
                check_dir = (checks[0][2], checks[0][3])
                index = enemy_positions.index(check_pos)
                checking_piece = enemy_pieces[index]
                valid_squares = []  # squares that pieces can legally move to

                # If the checking piece is a knight, the option to block no longer exists.
                # You can only capture or move the king
                if checking_piece == 'knight':
                    valid_squares = [check_pos]
                else:
                    for i in range(1, 8):
                        valid_square = (self.king_position[0] + check_dir[0] * i,
                                        self.king_position[1] + check_dir[1] * i)
                        valid_squares.append(valid_square)
                        if valid_square == check_pos:  # The valid squares ends when you get to the checking piece
                            break

                # Get rid of any moves that don't block check
                for i in range(len(self.options)):
                    if i == king_index:
                        self.trim_invalid_king_moves(king_index, enemy_pieces, enemy_positions)
                    else:
                        # Iterate through the list backwards, while removing corresponding elements
                        for j in range(len(self.options[i]) - 1, -1, -1):
                            if self.options[i][j] not in valid_squares:
                                self.options[i].pop(j)

            # More than 1 piece causing check. This is when there is a double check (triple and more are impossible).
            # In this case, the king is forced to move. Thus, remove all moves from other pieces.
            else:
                for i in range(len(self.options)):
                    if i == king_index:
                        self.trim_invalid_king_moves(king_index, enemy_pieces, enemy_positions)
                    else:
                        self.options[i] = []
        else:  # If the king is not in check, we still need to trim the kings moves to ensure it doesn't move into check
            self.trim_invalid_king_moves(king_index, enemy_pieces, enemy_positions)

        # Check through pinned pieces and trim invalid moves.
        # These pieces can only move along the path of check, as they need to continue blocking the attacking piece.
        # If in check, these pieces may not have any moves to trim as they will have been trimmed in the earlier step.
        for pin in pins:
            pin_pos = (pin[0], pin[1])
            pin_dir = (pin[2], pin[3])
            negative_pin_dir = (-pin[2], -pin[3])

            pinned_piece_index = self.positions.index(pin_pos)
            pinned_piece = self.pieces[pinned_piece_index]

            # A knight moves in an 'L' shape, and thus, it cannot move and still be blocking they path of check.
            # As such all its moves an invalid, since they all lead to the king being in check
            if pinned_piece == 'knight':
                self.options[pinned_piece_index] = []
            else:
                for j in range(len(self.options[pinned_piece_index]) - 1, -1, -1):
                    move = self.options[pinned_piece_index][j]
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
                        self.options[pinned_piece_index].pop(j)

    # Removes the king's invalid moves from the options list. Invalid moves are those where the king moves into check.
    def trim_invalid_king_moves(self, king_index, enemy_pieces, enemy_positions):
        moves_to_remove = []
        for i in range(len(self.options[king_index])):
            move = self.options[king_index][i]

            # Make a copy of required lists
            copy_ally_positions = list(self.positions)
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
            in_check = self.check_checks(move, copy_ally_positions, copy_enemy_pieces, copy_enemy_positions)
            if in_check:
                moves_to_remove.append(i)

        # Iterate through the list backwards and remove the corresponding moves
        for move in moves_to_remove[::-1]:
            self.options[king_index].pop(move)

    # Moves the selected piece to the destination (if a valid one is chosen) and take the appropriate actions
    # (capture, en passant, castling)
    def move_selected(self, selection, destination, last_moved, enemy_pieces, enemy_positions):
        piece_moved = False

        # Determine if a valid destination is selected
        if selection != -1 and destination in self.options[selection]:
            last_moved = [self.pieces[selection], self.positions[selection], destination]
            print(last_moved)
            self.positions[selection] = destination
            piece_moved = True

            # Check if an enemy piece was captured
            if destination in enemy_positions:
                enemy_piece_index = enemy_positions.index(destination)
                self.captured_pieces.append(enemy_pieces[enemy_piece_index])
                enemy_pieces.pop(enemy_piece_index)
                enemy_positions.pop(enemy_piece_index)

            # check if en passant pawn was captured
            if destination == self.en_passant_coords:
                coords = (self.en_passant_coords[0], self.en_passant_coords[1] - self.pawn_direction)
                enemy_piece_index = enemy_positions.index(coords)
                self.captured_pieces.append(enemy_pieces[enemy_piece_index])
                enemy_pieces.pop(enemy_piece_index)
                enemy_positions.pop(enemy_piece_index)
                self.en_passant_coords = (-1, -1)

            # Check for pawn promotion
            if self.pieces[selection] == 'pawn' and destination[1] == self.pawn_promo_row:
                self.promotion = True
                self.pawn_to_promo = selection

            # Update king's position
            if self.pieces[selection] == 'king':
                self.king_position = destination

                # Check if castling occurred, which is when king moves 2 squares in either direction
                if last_moved[1][0] - destination[0] == -2:  # Move to the right side
                    rook_coords = (7, destination[1])
                    rook_index = self.positions.index(rook_coords)
                    self.positions[rook_index] = (destination[0] - 1, destination[1])
                elif last_moved[1][0] - destination[0] == 2:  # Move to the left side
                    rook_coords = (0, destination[1])
                    rook_index = self.positions.index(rook_coords)
                    self.positions[rook_index] = (destination[0] + 1, destination[1])

            # Update state of Castling
            self.update_castling_state(self.pieces[selection], last_moved[1])

        return piece_moved, last_moved  # , castling_state

    # Promote the pawn to the selected power piece
    def pawn_promotion(self, pawn_to_promo, promo_type):
        self.pieces[pawn_to_promo] = promo_type
        self.promotion = False
        self.pawn_to_promo = -1

    # Determines whether the game is over (checkmate or stalemate) and who the winner is
    def check_game_over(self, enemy_colour):
        # Check if current player has any valid moves. If so, game is not over.
        for i in range(len(self.options)):
            if self.options[i]:
                return False, '', ''

        # If current player cannot make any valid move, game is over.
        # If they are under check it is checkmate, otherwise it is stalemate
        if self.under_check:
            return True, 'Checkmate', enemy_colour
        else:
            return True, 'Stalemate', enemy_colour
