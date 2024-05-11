from constants import *


# Draws the main game board
def draw_board(screen, turn_step, selection, last_moved, white_positions, black_positions):
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
        pygame.draw.rect(screen, 'grey',
                         [FORFEIT_COORDS[0][0], FORFEIT_COORDS[0][1], TILE_SIZE * 2.05, TILE_SIZE * 0.55])
        screen.blit(MEDIUM_FONT.render('FORFEIT', True, 'black'), FORFEIT_COORDS[0])
    elif turn_step >= 2:  # Black's Turn
        pygame.draw.rect(screen, 'grey',
                         [FORFEIT_COORDS[1][0], FORFEIT_COORDS[1][1], TILE_SIZE * 2.05, TILE_SIZE * 0.55])
        screen.blit(MEDIUM_FONT.render('FORFEIT', True, 'black'), FORFEIT_COORDS[1])


# Draws all the pieces onto the board according to their current position
def draw_pieces(screen, white_pieces, white_positions, black_pieces, black_positions):
    for i in range(len(white_pieces)):
        index = PIECE_LIST.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (TILE_SIZE * (white_positions[i][0] + 0.175) + X_OFFSET,
                                     TILE_SIZE * (white_positions[i][1] + 0.2) + + Y_OFFSET))
        else:
            screen.blit(WHITE_IMAGES[index], (TILE_SIZE * (white_positions[i][0] + 0.1) + X_OFFSET,
                                              TILE_SIZE * (white_positions[i][1] + 0.12) + Y_OFFSET))

    for i in range(len(black_pieces)):
        index = PIECE_LIST.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (TILE_SIZE * (black_positions[i][0] + 0.175) + X_OFFSET,
                                     TILE_SIZE * (black_positions[i][1] + 0.2) + + Y_OFFSET))
        else:
            screen.blit(BLACK_IMAGES[index], (TILE_SIZE * (black_positions[i][0] + 0.1) + X_OFFSET,
                                              TILE_SIZE * (black_positions[i][1] + 0.12) + Y_OFFSET))


# Draws valid moves on screen
def draw_valid(screen, turn_step, moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, ((moves[i][0] + 0.5) * TILE_SIZE + X_OFFSET,
                                           (moves[i][1] + 0.5) * TILE_SIZE + Y_OFFSET), 5)


# Draws the option to castle for the king
def draw_castling(screen, turn_step, moves):
    if turn_step < 2:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, ((moves[i][0] + 0.5) * TILE_SIZE + X_OFFSET,
                                           (moves[i][1] + 0.5) * TILE_SIZE + Y_OFFSET), 5)


# Draw the promotion selection menu and promote the pawn to the selected power piece
def pawn_promotion(screen, turn, ally_pieces, promotion_index):
    window_corner = (-1, -1)

    # Draw the pawn promotion piece selection window
    if turn == 'white':
        window_corner = (WIDTH - AVATAR_TILE_SIZE - TILE_SIZE * 0.1, 1.1 * AVATAR_TILE_SIZE)
        pygame.draw.rect(screen, 'dark gray',
                         [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2])
        for i in range(len(PROMOTION_OPTIONS)):
            piece = PROMOTION_OPTIONS[i]
            index = PIECE_LIST.index(piece)
            screen.blit(WHITE_IMAGES[index],
                        (WIDTH - AVATAR_TILE_SIZE, 1.12 * AVATAR_TILE_SIZE + TILE_SIZE * (i + 0.12)))
        pygame.draw.rect(screen, turn, [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2], 8)
    else:
        window_corner = (AVATAR_TILE_SIZE - TILE_SIZE * 1.1, HEIGHT - 1.1 * AVATAR_TILE_SIZE - TILE_SIZE * 4.2)
        pygame.draw.rect(screen, 'dark gray', [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2])
        for i in range(len(PROMOTION_OPTIONS)):
            piece = PROMOTION_OPTIONS[i]
            index = PIECE_LIST.index(piece)
            screen.blit(BLACK_IMAGES[index], (AVATAR_TILE_SIZE - TILE_SIZE,
                                              1.12 * AVATAR_TILE_SIZE + TILE_SIZE * (i + 0.12 - 1)))
        pygame.draw.rect(screen, turn, [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2], 8)

    # Determine which piece was selected, promote the pawn and then recalculate the moves
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0]
    y_pos = int((mouse_pos[1] - window_corner[1]) // (TILE_SIZE * 1.05))
    if turn == 'white' and left_click and window_corner[0] <= x_pos <= window_corner[0] + TILE_SIZE and 0 <= y_pos < 4:
        ally_pieces[promotion_index] = PROMOTION_OPTIONS[y_pos]
        return False
    elif turn == 'black' and left_click and window_corner[0] <= x_pos <= window_corner[0] + TILE_SIZE \
            and 0 <= y_pos < 4:
        ally_pieces[promotion_index] = PROMOTION_OPTIONS[y_pos]
        return False

    return True


# Draws captured pieces on either side of the chess board
def draw_captured(screen, captured_pieces_white, captured_pieces_black):
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = PIECE_LIST.index(captured_piece)
        screen.blit(SMALL_BLACK_IMAGES[index],
                    (X_OFFSET - SMALL_PIECE_DIMENSIONS[0] - 10,  Y_OFFSET + 1.2 * SMALL_PIECE_DIMENSIONS[0] * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = PIECE_LIST.index(captured_piece)
        screen.blit(SMALL_WHITE_IMAGES[index],
                    (X_OFFSET + BOARD_DIMENSION + 20,
                     BOARD_DIMENSION - 1.2 * SMALL_PIECE_DIMENSIONS[0] * i))


# Draws a red border around the king if it is in check
def draw_check(screen, check, king_position):
    if check:
        pygame.draw.rect(screen, 'dark red', [X_OFFSET + king_position[0] * TILE_SIZE,
                                              Y_OFFSET + king_position[1] * TILE_SIZE, TILE_SIZE, TILE_SIZE], 5)


# Draws the game over screen. Message changes depending on the mode of game over - Forfeit, Stalemate, or Checkmate
def draw_game_over(screen, mode, winner):
    # Creating a transparent overlay for the game over screen
    s = pygame.Surface((WIDTH, HEIGHT))
    s.set_alpha(128)  # alpha level for transparency
    s.fill(GREY)
    screen.blit(s, (0, 0))

    if mode == 'Forfeit':
        text1 = BIG_FONT.render(f'{winner} won the game due to opponent forfeiting!', True, WHITE)
    elif mode == 'Checkmate':
        text1 = BIG_FONT.render(f'Checkmate! {winner} won the game!', True, WHITE)
    elif mode == 'Stalemate':
        text1 = BIG_FONT.render(f'Stalemate!', True, WHITE)

    text1_rect = text1.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text1, text1_rect)
    text2 = FONT.render(f'Press ENTER to Restart!', True, WHITE)
    text2_rect = text2.get_rect(center=(WIDTH / 2, (HEIGHT + TILE_SIZE) / 2))
    screen.blit(text2, text2_rect)
