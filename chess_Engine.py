from variables import *
from draw_Functions import *
from move_Generation import *

pygame.init()


# Returns the valid moves for the selected piece
def return_valid_moves():
    castling_options = []
    if turn_step < 2:
        valid_options = white_options[selection]
        if white_pieces[selection] == 'king':
            castling_options = check_castling('white', white_positions[selection], white_castling_state, under_check,
                                              white_positions, black_pieces, black_positions)
    else:
        valid_options = black_options[selection]
        if black_pieces[selection] == 'king':
            castling_options = check_castling('black', black_positions[selection], black_castling_state, under_check,
                                              black_positions, white_pieces, white_positions)

    return valid_options, castling_options


# Determines whether the game is over (checkmate or stalemate) and who the winner is
def check_game_over(ally_options, enemy_colour):
    # Check if current player has any valid moves. If so, game is not over.
    for i in range(len(ally_options)):
        if ally_options[i]:
            return False, '', ''

    # If current player cannot make any valid move, game is over.
    # If they are under check it is checkmate, otherwise it is stalemate
    if under_check:
        return True, 'Checkmate', enemy_colour
    else:
        return True, 'Stalemate', enemy_colour


# Main Game Loop
run = True
white_options, en_passant_coords = check_options('white', last_moved, white_pieces, white_positions, black_positions)
while run:
    timer.tick(FPS)
    screen.fill(GREY)
    draw_board(screen, turn_step, selection, last_moved, white_positions, black_positions)
    draw_pieces(screen, white_pieces, white_positions, black_pieces, black_positions)
    draw_captured(screen, captured_pieces_white, captured_pieces_black)

    # Check if king is in check, if so highlight it.
    if turn_step <= 1:  # White's Turn
        under_check, _, _ = check_pins_and_checks('white', white_king_position, white_positions,
                                                  black_pieces, black_positions)
        draw_check(screen, under_check, white_king_position)
    else:  # Black's Turn
        under_check, _, _ = check_pins_and_checks('black', black_king_position, black_positions,
                                                  white_pieces, white_positions)
        draw_check(screen, under_check, black_king_position)

    if white_promotion:
        white_promotion = pawn_promotion(screen, 'white', white_pieces, white_promotion_index)
        if not white_promotion:
            black_options, en_passant_coords = check_options('black', last_moved,
                                                             black_pieces, black_positions, white_positions)
            trim_invalid_moves('black', black_king_position, black_pieces, black_positions, black_options,
                               white_pieces, white_positions)

    elif black_promotion:
        black_promotion = pawn_promotion(screen, 'black', black_pieces, black_promotion_index)
        if not black_promotion:
            white_options, en_passant_coords = check_options('white', last_moved,
                                                             white_pieces, white_positions, black_positions)
            trim_invalid_moves('white', white_king_position, white_pieces, white_positions, white_options,
                               black_pieces, black_positions)

    if selection != -1:
        valid_moves, castling_moves = return_valid_moves()
        draw_valid(screen, turn_step, valid_moves)
        draw_castling(screen, turn_step, valid_moves)

    # Check for game over and if it is, draw the corresponding screen
    if game_over:
        draw_game_over(screen, game_over_mode, winner)
    else:
        if turn_step <= 1:  # White's Turn
            game_over, game_over_mode, winner = check_game_over(white_options, 'black')
        else:  # Black's Turn
            game_over, game_over_mode, winner = check_game_over(black_options, 'white')

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

            if turn_step <= 1:  # White's Turn
                # If forfeit button is pressed
                if FORFEIT_COORDS[0][0] <= event.pos[0] <= FORFEIT_COORDS[0][0] + TILE_SIZE * 2.05 and \
                        FORFEIT_COORDS[0][1] <= event.pos[1] <= FORFEIT_COORDS[0][1] + TILE_SIZE * 0.55:
                    winner = 'Black'
                    game_over = True
                    game_over_mode = 'Forfeit'

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

                    # Update king's position
                    if white_pieces[selection] == 'king':
                        white_king_position = click_coords

                    # Update state of Castling
                    white_castling_state = update_castling_state(last_moved[0], last_moved[1], white_castling_state)

                    # Reset/Update values for next turn
                    black_options, en_passant_coords = check_options('black', last_moved,
                                                                     black_pieces, black_positions, white_positions)
                    trim_invalid_moves('black', black_king_position, black_pieces, black_positions, black_options,
                                       white_pieces, white_positions)
                    turn_step = 2
                    selection = -1
                    valid_moves = []

                # Check if castling occurred
                elif click_coords in castling_moves and selection != -1:
                    last_moved = [white_pieces[selection], white_positions[selection], click_coords]
                    white_positions[selection] = click_coords
                    white_king_position = click_coords
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
                    black_options, en_passant_coords = check_options('black', last_moved,
                                                                     black_pieces, black_positions, white_positions)
                    trim_invalid_moves('black', black_king_position, black_pieces, black_positions, black_options,
                                       white_pieces, white_positions)
                    turn_step = 2
                    selection = -1
                    valid_moves = []

            else:  # Black's Turn
                # If forfeit button is pressed
                if FORFEIT_COORDS[1][0] <= event.pos[0] <= FORFEIT_COORDS[1][0] + TILE_SIZE * 2.05 and \
                        FORFEIT_COORDS[1][1] <= event.pos[1] <= FORFEIT_COORDS[1][1] + TILE_SIZE * 0.55:
                    winner = 'White'
                    game_over = True
                    game_over_mode = 'Forfeit'

                # Determine if a black piece is selected
                if click_coords in black_positions:
                    selection = black_positions.index(click_coords)
                    if turn_step == 2:
                        turn_step = 3

                # Determine if a valid destination is selected
                if click_coords in valid_moves and selection != -1:
                    last_moved = [black_pieces[selection], black_positions[selection], click_coords]
                    black_positions[selection] = click_coords

                    # Check if an enemy piece was captured
                    if click_coords in white_positions:
                        white_piece_index = white_positions.index(click_coords)
                        captured_pieces_black.append(white_pieces[white_piece_index])
                        white_pieces.pop(white_piece_index)
                        white_positions.pop(white_piece_index)

                    # Check if en passant pawn was captured
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

                    # Update king's position
                    if black_pieces[selection] == 'king':
                        black_king_position = click_coords

                    # Update Castling state
                    black_castling_state = update_castling_state(last_moved[0], last_moved[1], black_castling_state)

                    # Reset/Update values for next turn
                    white_options, en_passant_coords = check_options('white', last_moved,
                                                                     white_pieces, white_positions, black_positions)
                    trim_invalid_moves('white', white_king_position, white_pieces, white_positions, white_options,
                                       black_pieces, black_positions)
                    turn_step = 0
                    selection = -1
                    valid_moves = []

                # Check if castling occurred
                elif click_coords in castling_moves and selection != -1:
                    last_moved = [black_pieces[selection], black_positions[selection], click_coords]
                    black_positions[selection] = click_coords
                    black_king_position = click_coords
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
                    white_options, en_passant_coords = check_options('white', last_moved,
                                                                     white_pieces, white_positions, black_positions)
                    trim_invalid_moves('white', white_king_position, white_pieces, white_positions, white_options,
                                       black_pieces, black_positions)
                    turn_step = 0
                    selection = -1
                    valid_moves = []

        if event.type == pygame.KEYDOWN and game_over:
            # If enter key is pressed, reset the game, so they can play again
            if event.key == pygame.K_RETURN:
                winner = ''
                game_over = False
                game_over_mode = ''
                under_check = False
                white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                white_positions = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                white_castling_state = 0
                captured_pieces_white = []
                white_king_position = (3, 0)
                black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                black_positions = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                black_castling_state = 0
                captured_pieces_black = []
                black_king_position = (3, 7)
                last_moved = ["", (-1, -1), (-1, -1)]
                castling_moves = []
                turn_step = 0
                selection = -1
                valid_moves = []
                black_options = []
                white_options, en_passant_coords = check_options('white', last_moved,
                                                                 white_pieces, white_positions, black_positions)
                white_promotion = False
                white_promotion_index = -1
                black_promotion = False
                black_promotion_index = -1

    pygame.display.flip()
pygame.quit()
