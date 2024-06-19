from constants import *


# Draws the main menu background
def draw_menu_background(screen):
    num_columns = WIDTH // TILE_SIZE + 1
    num_rows = HEIGHT // TILE_SIZE + 1
    row = 0
    column = 0
    while row < num_rows:
        if row % 2 == 0:
            pygame.draw.rect(screen, GREEN,
                             [TILE_SIZE + (column * TILE_SIZE * 2), row * TILE_SIZE, TILE_SIZE, TILE_SIZE])
        else:
            pygame.draw.rect(screen, GREEN, [(column * TILE_SIZE * 2), row * TILE_SIZE, TILE_SIZE, TILE_SIZE])
        column += 1
        if column > num_columns:
            column = 0
            row += 1


# Draws the main menu buttons and text
def draw_main_menu(screen):
    title = BIG_FONT.render(f'Pygame Chess', True, 'black')
    title_rect = title.get_rect(center=(WIDTH / 2, 0.175 * HEIGHT))
    screen.blit(title, title_rect)

    start = MEDIUM_FONT.render(f'Start Game', True, 'white')
    start_rect = start.get_rect(center=(WIDTH / 2, 0.6 * HEIGHT))
    pygame.draw.rect(screen, 'black', start_rect)
    screen.blit(start, start_rect)

    past = MEDIUM_FONT.render(f'Past Games', True, 'white')
    past_rect = past.get_rect(center=(WIDTH / 2, 0.7 * HEIGHT))
    pygame.draw.rect(screen, 'black', past_rect)
    screen.blit(past, past_rect)

    how = MEDIUM_FONT.render(f'How To Play', True, 'white')
    how_rect = how.get_rect(center=(WIDTH / 2, 0.8 * HEIGHT))
    pygame.draw.rect(screen, 'black', how_rect)
    screen.blit(how, how_rect)


def draw_settings_menu(screen, match_setting_list):
    # Game Type
    game_type = MEDIUM_FONT.render(f'Game Type:', True, 'Black')
    game_type_rect = game_type.get_rect(center=(0.1 * WIDTH, 0.17 * HEIGHT))
    screen.blit(game_type, game_type_rect)

    colour = 'grey' if match_setting_list[0] else 'black'
    pvp = MEDIUM_FONT.render(f'Player Vs. Player', True, 'white')
    pvp_rect = pvp.get_rect(center=(0.35 * WIDTH, 0.17 * HEIGHT))
    pygame.draw.rect(screen, colour, pvp_rect)
    screen.blit(pvp, pvp_rect)

    colour = 'grey' if match_setting_list[1] else 'black'
    pvai = MEDIUM_FONT.render(f'Player Vs AI', True, 'white')
    pvai_rect = pvai.get_rect(center=(0.6 * WIDTH, 0.17 * HEIGHT))
    pygame.draw.rect(screen, colour, pvai_rect)
    screen.blit(pvai, pvai_rect)

    colour = 'grey' if match_setting_list[2] else 'black'
    aivai = MEDIUM_FONT.render(f'AI Vs AI', True, 'white')
    aivai_rect = aivai.get_rect(center=(0.8 * WIDTH, 0.17 * HEIGHT))
    pygame.draw.rect(screen, colour, aivai_rect)
    screen.blit(aivai, aivai_rect)

    # Player 1 Colour
    player_colour = MEDIUM_FONT.render(f'Player 1 Colour:', True, 'Black')
    player_colour_rect = player_colour.get_rect(center=(0.12 * WIDTH, 0.41 * HEIGHT))
    screen.blit(player_colour, player_colour_rect)

    colour = 'grey' if match_setting_list[3] else 'black'
    pwhite = MEDIUM_FONT.render(f'White', True, 'white')
    pwhite_rect = pwhite.get_rect(center=(0.35 * WIDTH, 0.41 * HEIGHT))
    pygame.draw.rect(screen, colour, pwhite_rect)
    screen.blit(pwhite, pwhite_rect)

    colour = 'grey' if match_setting_list[4] else 'black'
    prand = MEDIUM_FONT.render(f'Random', True, 'white')
    prand_rect = prand.get_rect(center=(0.6 * WIDTH, 0.41 * HEIGHT))
    pygame.draw.rect(screen, colour, prand_rect)
    screen.blit(prand, prand_rect)

    colour = 'grey' if match_setting_list[5] else 'black'
    pblack = MEDIUM_FONT.render(f'Black', True, 'white')
    pblack_rect = pblack.get_rect(center=(0.8 * WIDTH, 0.41 * HEIGHT))
    pygame.draw.rect(screen, colour, pblack_rect)
    screen.blit(pblack, pblack_rect)

    start = MEDIUM_FONT.render(f'Start Game', True, 'white')
    start_rect = start.get_rect(center=(WIDTH / 2, 0.8 * HEIGHT))
    pygame.draw.rect(screen, 'black', start_rect)
    screen.blit(start, start_rect)


# Draws the main game board
def draw_board(screen, player, turn, selection, last_moved, avatar, ai):
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
    if selection != -1:
        pygame.draw.rect(screen, 'yellow', [X_OFFSET + player[turn].positions[selection][0] * TILE_SIZE,
                                            Y_OFFSET + player[turn].positions[selection][1] * TILE_SIZE,
                                            TILE_SIZE, TILE_SIZE])

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
    if player[turn].top_or_bot == 'top':  # Top Player's turn
        top_avatar_colour = 'grey'
        bot_avatar_colour = GREY
    else:  # Bottom Player's turn
        top_avatar_colour = GREY
        bot_avatar_colour = 'grey'
    pygame.draw.rect(screen, top_avatar_colour, [WIDTH-AVATAR_TILE_SIZE, 0, AVATAR_TILE_SIZE, AVATAR_TILE_SIZE])
    pygame.draw.rect(screen, 'black', [WIDTH - AVATAR_TILE_SIZE, 0, AVATAR_TILE_SIZE, AVATAR_TILE_SIZE], 2)
    screen.blit(avatar[0], (WIDTH - AVATAR_TILE_SIZE + (AVATAR_TILE_SIZE - AVATAR_SIZE) / 2,
                            (AVATAR_TILE_SIZE - AVATAR_SIZE) / 2))
    pygame.draw.rect(screen, bot_avatar_colour, [0, HEIGHT - AVATAR_TILE_SIZE, AVATAR_TILE_SIZE, AVATAR_TILE_SIZE])
    pygame.draw.rect(screen, 'black', [0, HEIGHT - AVATAR_TILE_SIZE, AVATAR_TILE_SIZE, AVATAR_TILE_SIZE], 2)
    screen.blit(avatar[1], ((AVATAR_TILE_SIZE - AVATAR_SIZE) / 2,
                            HEIGHT - AVATAR_TILE_SIZE + (AVATAR_TILE_SIZE - AVATAR_SIZE) / 2))

    # Drawing forfeit button, only for human players
    if not ai:
        pygame.draw.rect(screen, 'grey',
                         [player[turn].forfeit_button_boundary[0][0], player[turn].forfeit_button_boundary[0][1],
                          TILE_SIZE * 2.05, TILE_SIZE * 0.55])
        screen.blit(MEDIUM_FONT.render('FORFEIT', True, 'black'), player[turn].forfeit_button_boundary[0])


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
def draw_valid(screen, turn, moves):
    if turn == 0:
        color = 'red'
    else:
        color = 'blue'
    for i in range(len(moves)):
        pygame.draw.circle(screen, color, ((moves[i][0] + 0.5) * TILE_SIZE + X_OFFSET,
                                           (moves[i][1] + 0.5) * TILE_SIZE + Y_OFFSET), 5)


# Draw the promotion selection menu and determines which power piece was selected
def draw_pawn_promotion(screen, turn, top_or_bot, images):
    # Draw the pawn promotion piece selection window
    if top_or_bot == 'top':
        window_corner = (WIDTH - AVATAR_TILE_SIZE - TILE_SIZE * 0.1, 1.1 * AVATAR_TILE_SIZE)
        pygame.draw.rect(screen, 'dark gray', [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2])
        for i in range(len(PROMOTION_OPTIONS)):
            piece = PROMOTION_OPTIONS[i]
            index = PIECE_LIST.index(piece)
            screen.blit(images[index],
                        (WIDTH - AVATAR_TILE_SIZE, 1.12 * AVATAR_TILE_SIZE + TILE_SIZE * (i + 0.12)))
        pygame.draw.rect(screen, turn, [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2], 8)
    else:  # top
        window_corner = (AVATAR_TILE_SIZE - TILE_SIZE * 1.1, HEIGHT - 1.1 * AVATAR_TILE_SIZE - TILE_SIZE * 4.2)
        pygame.draw.rect(screen, 'dark gray', [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2])
        for i in range(len(PROMOTION_OPTIONS)):
            piece = PROMOTION_OPTIONS[i]
            index = PIECE_LIST.index(piece)
            screen.blit(images[index], (AVATAR_TILE_SIZE - TILE_SIZE,
                                        1.12 * AVATAR_TILE_SIZE + TILE_SIZE * (i + 0.12 - 1)))
        pygame.draw.rect(screen, turn, [window_corner[0], window_corner[1], TILE_SIZE, TILE_SIZE * 4.2], 8)

    # Determine which piece was selected, promote the pawn and then recalculate the moves
    mouse_pos = pygame.mouse.get_pos()
    left_click = pygame.mouse.get_pressed()[0]
    x_pos = mouse_pos[0]
    y_pos = int((mouse_pos[1] - window_corner[1]) // (TILE_SIZE * 1.05))
    if left_click and window_corner[0] <= x_pos <= window_corner[0] + TILE_SIZE and 0 <= y_pos < 4:
        return PROMOTION_OPTIONS[y_pos]

    # If no option has been chosen yet
    return ''


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
    text1 = ''
    if mode == 'Forfeit':
        text1 = BIG_FONT.render(f'{winner} won the game due to opponent forfeiting!', True, WHITE)
    elif mode == 'Checkmate':
        text1 = BIG_FONT.render(f'Checkmate! {winner} won the game!', True, WHITE)
    elif mode == 'Stalemate':
        text1 = BIG_FONT.render(f'Stalemate!', True, WHITE)

    text1_rect = text1.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    screen.blit(text1, text1_rect)
    text2 = FONT.render(f'Press ENTER to Restart Game!', True, WHITE)
    text2_rect = text2.get_rect(center=(WIDTH / 2, 0.6 * HEIGHT))
    screen.blit(text2, text2_rect)
    text3 = FONT.render(f'Press ESC to Return to Main Menu!', True, WHITE)
    text3_rect = text3.get_rect(center=(WIDTH / 2, 0.65 * HEIGHT))
    screen.blit(text3, text3_rect)
