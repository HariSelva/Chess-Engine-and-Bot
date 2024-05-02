import pygame

pygame.init()

# Mouse Event Constants
LEFT_MOUSE_CLICK = 1

# Use size of first monitor/display to set the screen size, while ensuring the dimensions are even
windowDimensions = pygame.display.get_desktop_sizes()
WIDTH = int(windowDimensions[0][0] * 0.8)
HEIGHT = int(windowDimensions[0][1] * 0.8)
if WIDTH % 2 == 1:
    WIDTH += 1
if HEIGHT % 2 == 1:
    HEIGHT += 1
print('Screen Dimensions:', WIDTH, ' x ', HEIGHT)
screen = pygame.display.set_mode([WIDTH, HEIGHT])


# Size variables for the board and images
TILE_SIZE = int(HEIGHT * 0.925/8)
BOARD_DIMENSION = TILE_SIZE * 8
X_OFFSET = int(WIDTH * 0.239)
Y_OFFSET = int(HEIGHT * 0.038)
AVATAR_TILE_SIZE = int(HEIGHT * 0.289)
AVATAR_SIZE = int(AVATAR_TILE_SIZE * 0.75)
PIECE_DIMENSIONS = (TILE_SIZE * 0.8, TILE_SIZE * 0.8)
PAWN_DIMENSIONS = (TILE_SIZE * 0.65, TILE_SIZE * 0.65)
SMALL_PIECE_DIMENSIONS = (TILE_SIZE * 0.45, TILE_SIZE * 0.45)

# Fonts
pygame.display.set_caption('Pygame Chess!')
font = pygame.font.SysFont('Times New Roman', 20)
medium_font = pygame.font.SysFont('Times New Roman', 40)
big_font = pygame.font.SysFont('Times New Roman', 60)


timer = pygame.time.Clock()
fps = 60

# Colour Variables
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BEIGE = (232, 220, 202)
GREEN = (110, 145, 0)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

# game variables
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_positions = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_positions = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
white_options = []
black_options = []
valid_moves = []
last_moved = ["", (-1, -1), (-1, -1)]
en_passant_coords = (-1, -1)
castling_moves = []

# load in game images
black_avatar = pygame.image.load('Assets/avatar player 2.png')
black_avatar = pygame.transform.scale(black_avatar, (AVATAR_SIZE, AVATAR_SIZE))
black_queen = pygame.image.load('Assets/black queen.png')
black_queen = pygame.transform.scale(black_queen, PIECE_DIMENSIONS)
black_queen_small = pygame.transform.scale(black_queen, SMALL_PIECE_DIMENSIONS)
black_king = pygame.image.load('Assets/black king.png')
black_king = pygame.transform.scale(black_king, PIECE_DIMENSIONS)
black_king_small = pygame.transform.scale(black_king, SMALL_PIECE_DIMENSIONS)
black_rook = pygame.image.load('Assets/black rook.png')
black_rook = pygame.transform.scale(black_rook, PIECE_DIMENSIONS)
black_rook_small = pygame.transform.scale(black_rook, SMALL_PIECE_DIMENSIONS)
black_bishop = pygame.image.load('Assets/black bishop.png')
black_bishop = pygame.transform.scale(black_bishop, PIECE_DIMENSIONS)
black_bishop_small = pygame.transform.scale(black_bishop, SMALL_PIECE_DIMENSIONS)
black_knight = pygame.image.load('Assets/black knight.png')
black_knight = pygame.transform.scale(black_knight, PIECE_DIMENSIONS)
black_knight_small = pygame.transform.scale(black_knight, SMALL_PIECE_DIMENSIONS)
black_pawn = pygame.image.load('Assets/black pawn.png')
black_pawn = pygame.transform.scale(black_pawn, PAWN_DIMENSIONS)
black_pawn_small = pygame.transform.scale(black_pawn, SMALL_PIECE_DIMENSIONS)

white_avatar = pygame.image.load('Assets/avatar player 1.png')
white_avatar = pygame.transform.scale(white_avatar, (AVATAR_SIZE, AVATAR_SIZE))
white_queen = pygame.image.load('Assets/white queen.png')
white_queen = pygame.transform.scale(white_queen, PIECE_DIMENSIONS)
white_queen_small = pygame.transform.scale(white_queen, SMALL_PIECE_DIMENSIONS)
white_king = pygame.image.load('Assets/white king.png')
white_king = pygame.transform.scale(white_king, PIECE_DIMENSIONS)
white_king_small = pygame.transform.scale(white_king, SMALL_PIECE_DIMENSIONS)
white_rook = pygame.image.load('Assets/white rook.png')
white_rook = pygame.transform.scale(white_rook, PIECE_DIMENSIONS)
white_rook_small = pygame.transform.scale(white_rook, SMALL_PIECE_DIMENSIONS)
white_bishop = pygame.image.load('Assets/white bishop.png')
white_bishop = pygame.transform.scale(white_bishop, PIECE_DIMENSIONS)
white_bishop_small = pygame.transform.scale(white_bishop, SMALL_PIECE_DIMENSIONS)
white_knight = pygame.image.load('Assets/white knight.png')
white_knight = pygame.transform.scale(white_knight, PIECE_DIMENSIONS)
white_knight_small = pygame.transform.scale(white_knight, SMALL_PIECE_DIMENSIONS)
white_pawn = pygame.image.load('Assets/white pawn.png')
white_pawn = pygame.transform.scale(white_pawn, PAWN_DIMENSIONS)
white_pawn_small = pygame.transform.scale(white_pawn, SMALL_PIECE_DIMENSIONS)
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
promotion_options = ['bishop', 'knight', 'rook', 'queen']

# check variables for determine various states of the game
winner = ''
game_over = False
# 0-whites turn no selection; 1-whites turn piece selected; 2-black turn no selection; 3-black turn piece selected
turn_step = 0
selection = -1
white_promotion = False
white_promotion_index = -1
black_promotion = False
black_promotion_index = -1
# 0-Both castling moves are available; 1-Only King side available; 2-Only Queen side available; 3-Neither is available
white_castling_state = 0
black_castling_state = 0

forfeit_coords = [(int(WIDTH * 0.045), int(HEIGHT * 0.023)), (int(WIDTH * 0.813), int(HEIGHT * 0.912))]


# draw main game board
def draw_board():
    # Drawing the board tiles
    pygame.draw.rect(screen, BEIGE, [X_OFFSET-10, Y_OFFSET-10, BOARD_DIMENSION + 20, BOARD_DIMENSION + 20])
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, GREEN,
                             [X_OFFSET + TILE_SIZE + (column * TILE_SIZE * 2),
                              Y_OFFSET + row * TILE_SIZE, TILE_SIZE, TILE_SIZE])
        else:
            pygame.draw.rect(screen, GREEN,
                             [X_OFFSET + (column * TILE_SIZE * 2), Y_OFFSET + row * TILE_SIZE, TILE_SIZE, TILE_SIZE])

    # Highlighting selected piece
    if turn_step == 1:
        pygame.draw.rect(screen, 'yellow', [X_OFFSET + white_positions[selection][0] * TILE_SIZE,
                                            Y_OFFSET + white_positions[selection][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE])
    elif turn_step == 3:
        pygame.draw.rect(screen, 'yellow', [X_OFFSET + black_positions[selection][0] * TILE_SIZE,
                                            Y_OFFSET + black_positions[selection][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE])

    # # Highlighting last moved piece and its previous location
    if last_moved[0] != "":
        for i in range(1, 3):
            # Changing the colour of the highlight depending on the original colour of the square
            if (last_moved[i][0] + last_moved[i][1]) % 2 == 0:
                colour = (204, 204, 0)
            else:
                colour = (150, 150, 0)
            pygame.draw.rect(screen, colour, [X_OFFSET + last_moved[i][0] * TILE_SIZE,
                                              Y_OFFSET + last_moved[i][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE])

    # Drawing grid lines
    for i in range(9):
        # Horizontal lines
        pygame.draw.line(screen, 'black', (X_OFFSET, Y_OFFSET + TILE_SIZE * i),
                         (X_OFFSET + BOARD_DIMENSION, Y_OFFSET + TILE_SIZE * i), 2)

        # Vertical lines
        pygame.draw.line(screen, 'black', (X_OFFSET + TILE_SIZE * i, Y_OFFSET),
                         (X_OFFSET + TILE_SIZE * i, Y_OFFSET + BOARD_DIMENSION), 2)

    # Drawing avatar area
    if turn_step < 2:  # White's Turn
        player1_avatar_colour = 'grey'
        player2_avatar_colour = GREY
    elif turn_step >= 2:  # Black's Turn
        player1_avatar_colour = GREY
        player2_avatar_colour = 'grey'
    pygame.draw.rect(screen, player1_avatar_colour, [WIDTH-AVATAR_TILE_SIZE, 0, AVATAR_TILE_SIZE, AVATAR_TILE_SIZE])
    pygame.draw.rect(screen, 'black', [WIDTH - AVATAR_TILE_SIZE, 0, AVATAR_TILE_SIZE, AVATAR_TILE_SIZE], 2)
    screen.blit(white_avatar, (WIDTH - AVATAR_TILE_SIZE + (AVATAR_TILE_SIZE - AVATAR_SIZE) / 2,
                               (AVATAR_TILE_SIZE - AVATAR_SIZE) / 2))
    pygame.draw.rect(screen, player2_avatar_colour, [0, HEIGHT - AVATAR_TILE_SIZE, AVATAR_TILE_SIZE, AVATAR_TILE_SIZE])
    pygame.draw.rect(screen, 'black', [0, HEIGHT - AVATAR_TILE_SIZE, AVATAR_TILE_SIZE, AVATAR_TILE_SIZE], 2)
    screen.blit(black_avatar, ((AVATAR_TILE_SIZE - AVATAR_SIZE) / 2,
                               HEIGHT - AVATAR_TILE_SIZE + (AVATAR_TILE_SIZE - AVATAR_SIZE) / 2))

    # Drawing forfeit button
    if turn_step < 2:  # White's Turn
        screen.blit(medium_font.render('FORFEIT', True, 'black'), forfeit_coords[0])
    elif turn_step >= 2:  # Black's Turn
        screen.blit(medium_font.render('FORFEIT', True, 'black'), forfeit_coords[1])


# Draws all the pieces onto the board according to their current position
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (TILE_SIZE * (white_positions[i][0] + 0.175) + X_OFFSET,
                                     TILE_SIZE * (white_positions[i][1] + 0.2) + + Y_OFFSET))
        else:
            screen.blit(white_images[index], (TILE_SIZE * (white_positions[i][0] + 0.1) + X_OFFSET,
                                              TILE_SIZE * (white_positions[i][1] + 0.12) + Y_OFFSET))

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (TILE_SIZE * (black_positions[i][0] + 0.175) + X_OFFSET,
                                     TILE_SIZE * (black_positions[i][1] + 0.2) + + Y_OFFSET))
        else:
            screen.blit(black_images[index], (TILE_SIZE * (black_positions[i][0] + 0.1) + X_OFFSET,
                                              TILE_SIZE * (black_positions[i][1] + 0.12) + Y_OFFSET))


# Check all the valid moves for each piece on the board.
def check_options(pieces, positions, turn, castle_state):
    moves_list = []
    global castling_moves
    all_moves_list = []

    for i in range(len(pieces)):
        piece = pieces[i]
        position = positions[i]
        if piece == 'pawn':
            moves_list = check_pawn(position, turn)
        elif piece == 'queen':
            moves_list = check_queen(position, turn)
        elif piece == 'king':
            moves_list = check_king(position, turn)
        elif piece == 'knight':
            moves_list = check_knight(position, turn)
        elif piece == 'rook':
            moves_list = check_rook(position, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(position, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


# Checks for all valid moves of the given pawn
def check_pawn(position, turn):
    moves_list = []
    x = position[0]
    y = position[1]
    global en_passant_coords
    if turn == 'white':
        # Move pawn forward 1 space
        if (x, y+1) not in white_positions and (x, y+1) not in black_positions and y < 7:
            moves_list.append((x, y+1))

            # Move pawn forward 2 space during its first move
            if (x, y+2) not in white_positions and (x, y+2) not in black_positions and y == 1:
                moves_list.append((x, y+2))

        # Move diagonally 1 space to capture an enemy piece
        if (x+1, y+1) in black_positions:
            moves_list.append((x+1, y+1))
        if (x-1, y+1) in black_positions:
            moves_list.append((x-1, y+1))

        # En Passant
        if y == 4 and last_moved[0] == 'pawn' and last_moved[1][1] == 6 and last_moved[2][1] == 4 and \
                abs(last_moved[1][0] - x) == 1:
            en_passant_coords = (last_moved[2][0], 5)
            moves_list.append(en_passant_coords)

    else:  # Black's turn
        # Move pawn forward 1 space
        if (x, y - 1) not in white_positions and (x, y - 1) not in black_positions and y > 0:
            moves_list.append((x, y - 1))

            # Move pawn forward 2 space during its first move
            if (x, y - 2) not in white_positions and (x, y - 2) not in black_positions and y == 6:
                moves_list.append((x, y - 2))

        # Move diagonally 1 space to capture an enemy piece
        if (x + 1, y - 1) in white_positions:
            moves_list.append((x + 1, y - 1))
        if (x - 1, y - 1) in white_positions:
            moves_list.append((x - 1, y - 1))

        # En Passant
        if y == 3 and last_moved[0] == 'pawn' and last_moved[1][1] == 1 and last_moved[2][1] == 3 and \
                abs(last_moved[1][0] - x) == 1:
            en_passant_coords = (last_moved[2][0], 2)
            moves_list.append(en_passant_coords)

    return moves_list


# Checks for all valid moves of the given queen
def check_queen(position, turn):
    # Use functions for check bishop and rook moves as the queen has the combined functionality of both pieces
    moves_list = check_bishop(position, turn)
    temp_moves_list = check_rook(position, turn)

    for moves in temp_moves_list:
        moves_list.append(moves)

    return moves_list


# Checks for all valid moves of the given king
def check_king(position, turn):
    moves_list = []
    x = position[0]
    y = position[1]
    if turn == 'white':
        ally_positions = white_positions
    else:  # Black's turn
        ally_positions = black_positions

    # Relative changes in position for each of the 8 position a king can reach by moving 1 tile in any direction
    delta = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        if 0 <= x + delta[i][0] <= 7 and 0 <= y + delta[i][1] <= 7 \
                and (x + delta[i][0], y + delta[i][1]) not in ally_positions:
            moves_list.append((x + delta[i][0], y + delta[i][1]))

    return moves_list


# Checks for all valid moves of the given knight
def check_knight(position, turn):
    moves_list = []
    x = position[0]
    y = position[1]
    if turn == 'white':
        ally_positions = white_positions
    else:  # Black's turn
        ally_positions = black_positions

    # Relative changes in position for each of the 8 position a knight can reach by going 2 tiles in the one direction
    # and 1 in the perpendicular direction
    delta = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        if 0 <= x + delta[i][0] <= 7 and 0 <= y + delta[i][1] <= 7 and \
                (x + delta[i][0], y + delta[i][1]) not in ally_positions:
            moves_list.append((x + delta[i][0], y + delta[i][1]))

    return moves_list


# Checks for all valid moves of the given rook
def check_rook(position, turn):
    moves_list = []
    x = position[0]
    y = position[1]
    if turn == 'white':
        enemy_positions = black_positions
        ally_positions = white_positions
    else:  # Black's turn
        enemy_positions = white_positions
        ally_positions = black_positions

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
        x_valid = x
        y_valid = y
        while path:
            x_valid = x_valid + delta_x
            y_valid = y_valid + delta_y
            if 0 <= x_valid <= 7 and 0 <= y_valid <= 7 and (x_valid, y_valid) not in ally_positions:
                moves_list.append((x_valid, y_valid))

                # If piece has encountered an enemy piece, it cannot go any further
                if (x_valid, y_valid) in enemy_positions:
                    path = False
            else:  # If piece has encountered the end of the board or an allied piece, it cannot go any further
                path = False

    return moves_list


# Checks for all valid moves of the given bishop
def check_bishop(position, turn):
    moves_list = []
    x = position[0]
    y = position[1]
    if turn == 'white':
        enemy_positions = black_positions
        ally_positions = white_positions
    else:  # Black's turn
        enemy_positions = white_positions
        ally_positions = black_positions

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
        x_valid = x
        y_valid = y
        while path:
            x_valid = x_valid + delta_x
            y_valid = y_valid + delta_y
            if 0 <= x_valid <= 7 and 0 <= y_valid <= 7 and (x_valid, y_valid) not in ally_positions:
                moves_list.append((x_valid, y_valid))

                # If piece has encountered an enemy piece, it cannot go any further
                if (x_valid, y_valid) in enemy_positions:
                    path = False
            else:  # If piece has encountered the end of the board or an allied piece, it cannot go any further
                path = False

    return moves_list


# Return the valid moves for the selected pieces
def check_valid_moves():
    castling_options = []
    if turn_step < 2:
        valid_options = white_options[selection]
        if white_pieces[selection] == 'king':
            castling_options = check_castling(white_positions[selection], 'white', white_castling_state)
    else:
        valid_options = black_options[selection]
        if black_pieces[selection] == 'king':
            castling_options = check_castling(black_positions[selection], 'black', black_castling_state)

    return valid_options, castling_options


# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, ((moves[i][0] + 0.5) * TILE_SIZE + X_OFFSET,
                                           (moves[i][1] + 0.5) * TILE_SIZE + Y_OFFSET), 5)


# draw captured pieces on either side of the chess board
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (X_OFFSET - SMALL_PIECE_DIMENSIONS[0] - 10,  Y_OFFSET + 1.2 * SMALL_PIECE_DIMENSIONS[0] * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index],
                    (X_OFFSET + BOARD_DIMENSION + 20,
                     BOARD_DIMENSION - 1.2 * SMALL_PIECE_DIMENSIONS[0] * i))


# draw the promotion selection menu and promote the pawn to the selected power piece
def pawn_promotion():
    global white_promotion
    global black_promotion
    window_corner = (-1, -1)

    # Draw the pawn promotion piece selection window
    if white_promotion:
        color = 'white'
        window_corner = (WIDTH - AVATAR_TILE_SIZE - TILE_SIZE * 0.1, 1.1 * AVATAR_TILE_SIZE)
        pygame.draw.rect(screen, 'dark gray',
                         [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2])
        for i in range(len(promotion_options)):
            piece = promotion_options[i]
            index = piece_list.index(piece)
            screen.blit(white_images[index], (WIDTH-AVATAR_TILE_SIZE, 1.12 * AVATAR_TILE_SIZE + TILE_SIZE * (i + 0.12)))
        pygame.draw.rect(screen, color, [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2], 8)
    elif black_promotion:
        color = 'black'
        window_corner = (AVATAR_TILE_SIZE - TILE_SIZE * 1.1, HEIGHT - 1.1 * AVATAR_TILE_SIZE - TILE_SIZE * 4.2)
        pygame.draw.rect(screen, 'dark gray', [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2])
        for i in range(len(promotion_options)):
            piece = promotion_options[i]
            index = piece_list.index(piece)
            screen.blit(black_images[index], (AVATAR_TILE_SIZE - TILE_SIZE,
                                              1.12 * AVATAR_TILE_SIZE + TILE_SIZE * (i + 0.12 - 1)))
        pygame.draw.rect(screen, color, [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2], 8)

    # Determine which piece was selected
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0]
    y_pos = int((mouse_pos[1] - window_corner[1]) // (TILE_SIZE * 1.05))
    if white_promotion and left_click and window_corner[0] <= x_pos <= window_corner[0] + TILE_SIZE and 0 <= y_pos < 4:
        white_pieces[white_promotion_index] = promotion_options[y_pos]
        white_promotion = False
    elif black_promotion and left_click and window_corner[0] <= x_pos <= window_corner[0] + TILE_SIZE and 0 <= y_pos < 4:
        black_pieces[black_promotion_index] = promotion_options[y_pos]
        black_promotion = False


# Updates the castling state and whether king/queen side (or neither) are available to castle
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


# Check if the king can complete a castling operation
def check_castling(king_position, turn, state):
    if state == 3:
        return []

    castling_options = []  # store each valid castle move as [[(king_coords)], [(castle_coords)]]
    if turn == 'white':
        enemy_positions = black_positions
        enemy_options = black_options
        ally_positions = white_positions
    else:  # Black's turn
        enemy_positions = white_positions
        enemy_options = white_options
        ally_positions = black_positions

    if state == 0 or state == 1:
        castling = True
        squares_to_check = [(king_position[0] - 1, king_position[1]), (king_position[0] - 2, king_position[1])]
        for square in squares_to_check:
            # Check if these squares have a piece on them and whether they are in check. If so castling not possible
            if square in ally_positions or square in enemy_positions or square in enemy_options:
                castling = False
        if castling:
            castling_options.append((king_position[0] - 2, king_position[1]))
    if state == 0 or state == 2:
        castling = True
        squares_to_check = [(king_position[0] + 1, king_position[1]), (king_position[0] + 2, king_position[1]),
                         (king_position[0] + 3, king_position[1])]
        for square in squares_to_check:
            # Check if these squares have a piece on them and whether they are in check. If so castling not possible
            if square in ally_positions or square in enemy_positions or square in enemy_options:
                castling = False
        if castling:
            castling_options.append((king_position[0] + 2, king_position[1]))
    return castling_options


# Drawing the option to castle for the king
def draw_castling(moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, ((moves[i][0] + 0.5) * TILE_SIZE + X_OFFSET,
                                           (moves[i][1] + 0.5) * TILE_SIZE + Y_OFFSET), 5)


# Main Game Loop
run = True
black_options = check_options(black_pieces, black_positions, 'black', black_castling_state)
white_options = check_options(white_pieces, white_positions, 'white', white_castling_state)
while run:
    timer.tick(fps)
    screen.fill(GREY)
    draw_board()
    draw_pieces()
    draw_captured()

    if white_promotion or black_promotion:
        pawn_promotion()

    if selection != -1:
        valid_moves, castling_moves = check_valid_moves()
        draw_valid(valid_moves)
        draw_castling(castling_moves)

    # Event Handling
    for event in pygame.event.get():
        x, y = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_CLICK and not game_over and \
                not white_promotion and not black_promotion:
            # Convert pixel coordinates of cursor position into row/col of chess board
            # Note 0,0 is top left tile, while 7,7 is bottom right tile
            x_coord = (event.pos[0] - X_OFFSET) // TILE_SIZE
            y_coord = (event.pos[1] - Y_OFFSET) // TILE_SIZE
            click_coords = (x_coord, y_coord)

            if turn_step <= 1:
                # Determine if a white piece is selected
                if click_coords in white_positions:
                    selection = white_positions.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1

                # Determine if a valid destination is selected
                if click_coords in valid_moves and selection != -1:
                    last_moved = [white_pieces[selection], white_positions[selection], click_coords]
                    white_positions[selection] = click_coords

                    # Check if an enemy piece was captured
                    if click_coords in black_positions:
                        black_piece_index = black_positions.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece_index])
                        black_pieces.pop(black_piece_index)
                        black_positions.pop(black_piece_index)

                    # check if en passant pawn was captured
                    if click_coords == en_passant_coords:
                        black_piece_index = black_positions.index((en_passant_coords[0], en_passant_coords[1] - 1))
                        captured_pieces_white.append(black_pieces[black_piece_index])
                        black_pieces.pop(black_piece_index)
                        black_positions.pop(black_piece_index)
                        en_passant_coords = (-1, -1)

                    # Check for pawn promotion
                    if white_pieces[selection] == 'pawn' and click_coords[1] == 7:
                        white_promotion = True
                        white_promotion_index = selection

                    # Update state of Castling
                    white_castling_state = update_castling_state(last_moved[0], last_moved[1], white_castling_state)

                    # Reset/Update values for next turn
                    black_options = check_options(black_pieces, black_positions, 'black', black_castling_state)
                    white_options = check_options(white_pieces, white_positions, 'white', white_castling_state)
                    turn_step = 2
                    selection = -1
                    valid_moves = []
                elif click_coords in castling_moves and selection != -1:
                    last_moved = [white_pieces[selection], white_positions[selection], click_coords]
                    white_positions[selection] = click_coords
                    if click_coords == (1, 0):
                        rook_coords = (0, 0)
                        rook_index = white_positions.index(rook_coords)
                        white_positions[rook_index] = (2, 0)
                    else:
                        rook_coords = (7, 0)
                        rook_index = white_positions.index(rook_coords)
                        white_positions[rook_index] = (4, 0)

                    # Update state of Castling
                    white_castling_state = update_castling_state(last_moved[0], last_moved[1], white_castling_state)

                    # Reset/Update values for next turn
                    black_options = check_options(black_pieces, black_positions, 'black', black_castling_state)
                    white_options = check_options(white_pieces, white_positions, 'white', white_castling_state)
                    turn_step = 2
                    selection = -1
                    valid_moves = []
            else:
                if click_coords in black_positions:
                    selection = black_positions.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3
                if click_coords in valid_moves and selection != -1:
                    last_moved = [black_pieces[selection], black_positions[selection], click_coords]
                    black_positions[selection] = click_coords
                    if click_coords in white_positions:
                        white_piece_index = white_positions.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece_index])
                        white_pieces.pop(white_piece_index)
                        white_positions.pop(white_piece_index)

                    # adding check if en passant pawn was captured
                    if click_coords == en_passant_coords:
                        white_piece_index = white_positions.index((en_passant_coords[0], en_passant_coords[1] + 1))
                        captured_pieces_black.append(white_pieces[white_piece_index])
                        white_pieces.pop(white_piece_index)
                        white_positions.pop(white_piece_index)
                        en_passant_coords = (-1, -1)

                    # Check for pawn promotion
                    if black_pieces[selection] == 'pawn' and click_coords[1] == 0:
                        black_promotion = True
                        black_promotion_index = selection

                    # Update Castling state
                    black_castling_state = update_castling_state(last_moved[0], last_moved[1], black_castling_state)

                    # Reset/Update values for next turn
                    black_options = check_options(black_pieces, black_positions, 'black', black_castling_state)
                    white_options = check_options(white_pieces, white_positions, 'white', white_castling_state)
                    turn_step = 0
                    selection = -1
                    valid_moves = []
                elif click_coords in castling_moves and selection != -1:
                    last_moved = [black_pieces[selection], black_positions[selection], click_coords]
                    black_positions[selection] = click_coords
                    if click_coords == (1, 7):
                        rook_coords = (0, 7)
                        rook_index = black_positions.index(rook_coords)
                        black_positions[rook_index] = (2, 7)
                    else:
                        rook_coords = (7, 7)
                        rook_index = black_positions.index(rook_coords)
                        black_positions[rook_index] = (4, 7)

                    # Update state of Castling
                    black_castling_state = update_castling_state(last_moved[0], last_moved[1], black_castling_state)

                    # Reset/Update values for next turn
                    black_options = check_options(black_pieces, black_positions, 'black', black_castling_state)
                    white_options = check_options(white_pieces, white_positions, 'white', white_castling_state)
                    turn_step = 0
                    selection = -1
                    valid_moves = []

    pygame.display.flip()
pygame.quit()
