from draw_Functions import *
from chess_Engine import *
from chess_AI import *
import random


def main_menu(screen, timer):
    def start_match_clicked(coordinates):
        if start_rect.x <= coordinates[0] <= start_rect.x + start_rect.width and \
                start_rect.y <= coordinates[1] <= start_rect.y + start_rect.height:
            return True
        return False

    def past_games_clicked(coordinates):
        if past_rect.x <= coordinates[0] <= past_rect.x + past_rect.width and \
                past_rect.y <= coordinates[1] <= past_rect.y + past_rect.height:
            return True
        return False

    def how_to_pay_clicked(coordinates):
        if how_rect.x <= coordinates[0] <= how_rect.x + how_rect.width and \
                how_rect.y <= coordinates[1] <= how_rect.y + how_rect.height:
            return True
        return False

    start = MEDIUM_FONT.render(f'Start Game', True, 'white')
    start_rect = start.get_rect(center=(WIDTH / 2, 0.6 * HEIGHT))
    past = MEDIUM_FONT.render(f'Past Games', True, 'white')
    past_rect = past.get_rect(center=(WIDTH / 2, 0.7 * HEIGHT))
    how = MEDIUM_FONT.render(f'How To Play', True, 'white')
    how_rect = how.get_rect(center=(WIDTH / 2, 0.8 * HEIGHT))

    # Main Game Loop
    run = True
    while run:
        timer.tick(FPS)
        screen.fill(BEIGE)
        draw_menu_background(screen)
        draw_main_menu(screen)

        # Event Handling
        for event in pygame.event.get():
            # x, y = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_CLICK:
                # Grabs the pixel coordinates of cursor position
                x_coord = event.pos[0]
                y_coord = event.pos[1]
                click_coords = (x_coord, y_coord)

                # If button is pressed, open corresponding screen
                if start_match_clicked(click_coords):
                    match_settings(screen, timer)
                elif past_games_clicked(click_coords):
                    print("past games")
                elif how_to_pay_clicked(click_coords):
                    print("how to play")

        pygame.display.flip()
    pygame.quit()


def match_settings(screen, timer):
    def pvp_clicked(coordinates):
        if pvp_rect.x <= coordinates[0] <= pvp_rect.x + pvp_rect.width and \
                pvp_rect.y <= coordinates[1] <= pvp_rect.y + pvp_rect.height:
            return True
        return False

    def pvai_clicked(coordinates):
        if pvai_rect.x <= coordinates[0] <= pvai_rect.x + pvai_rect.width and \
                pvai_rect.y <= coordinates[1] <= pvai_rect.y + pvai_rect.height:
            return True
        return False

    def aivai_clicked(coordinates):
        if aivai_rect.x <= coordinates[0] <= aivai_rect.x + aivai_rect.width and \
                aivai_rect.y <= coordinates[1] <= aivai_rect.y + aivai_rect.height:
            return True
        return False

    def white_clicked(coordinates):
        if pwhite_rect.x <= coordinates[0] <= pwhite_rect.x + pwhite_rect.width and \
                pwhite_rect.y <= coordinates[1] <= pwhite_rect.y + pwhite_rect.height:
            return True
        return False

    def rand_clicked(coordinates):
        if prand_rect.x <= coordinates[0] <= prand_rect.x + prand_rect.width and \
                prand_rect.y <= coordinates[1] <= prand_rect.y + prand_rect.height:
            return True
        return False

    def black_clicked(coordinates):
        if pblack_rect.x <= coordinates[0] <= pblack_rect.x + pblack_rect.width and \
                pblack_rect.y <= coordinates[1] <= pblack_rect.y + pblack_rect.height:
            return True
        return False

    def start_match_clicked(coordinates):
        if start_rect.x <= coordinates[0] <= start_rect.x + start_rect.width and \
                start_rect.y <= coordinates[1] <= start_rect.y + start_rect.height:
            return True
        return False

    def white_top(setting_list):
        if setting_list[3]:  # White bottom
            return False
        if setting_list[4]:  # Random
            return random.choice([True, False])
        if setting_list[5]:  # White Top
            return True

    def player_or_ai(setting_list):
        if setting_list[0]:  # Player Vs Player
            return False, False
        if setting_list[1]:  # Player Vs AI
            return False, True
        if setting_list[2]:  # Ai Vs Ai
            return True, True

    pvp = MEDIUM_FONT.render(f'Player Vs. Player', True, 'white')
    pvp_rect = pvp.get_rect(center=(0.35 * WIDTH, 0.17 * HEIGHT))
    pvai = MEDIUM_FONT.render(f'Player Vs AI', True, 'white')
    pvai_rect = pvai.get_rect(center=(0.6 * WIDTH, 0.17 * HEIGHT))
    aivai = MEDIUM_FONT.render(f'AI Vs AI', True, 'white')
    aivai_rect = aivai.get_rect(center=(0.8 * WIDTH, 0.17 * HEIGHT))
    pwhite = MEDIUM_FONT.render(f'White', True, 'white')
    pwhite_rect = pwhite.get_rect(center=(0.35 * WIDTH, 0.41 * HEIGHT))
    prand = MEDIUM_FONT.render(f'Random', True, 'white')
    prand_rect = prand.get_rect(center=(0.6 * WIDTH, 0.41 * HEIGHT))
    pblack = MEDIUM_FONT.render(f'Black', True, 'white')
    pblack_rect = pblack.get_rect(center=(0.8 * WIDTH, 0.41 * HEIGHT))
    start = MEDIUM_FONT.render(f'Start Game', True, 'white')
    start_rect = start.get_rect(center=(WIDTH / 2, 0.8 * HEIGHT))

    # Holds info on which setting is chosen: PvP, PvAI, AIvAI, White, Random, Black
    match_setting_list = [True, False, False, False, True, False]

    # Main Game Loop
    run = True
    while run:
        timer.tick(FPS)
        screen.fill(BEIGE)
        draw_menu_background(screen)
        draw_settings_menu(screen, match_setting_list)

        # Event Handling
        for event in pygame.event.get():
            # x, y = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_CLICK:
                # Grabs the pixel coordinates of cursor position
                x_coord = event.pos[0]
                y_coord = event.pos[1]
                click_coords = (x_coord, y_coord)

                # If button is pressed, activate corresponding setting or open game screen
                if pvp_clicked(click_coords):
                    match_setting_list[0] = True
                    match_setting_list[1] = False
                    match_setting_list[2] = False
                if pvai_clicked(click_coords):
                    match_setting_list[0] = False
                    match_setting_list[1] = True
                    match_setting_list[2] = False
                if aivai_clicked(click_coords):
                    match_setting_list[0] = False
                    match_setting_list[1] = False
                    match_setting_list[2] = True
                if white_clicked(click_coords):
                    match_setting_list[3] = True
                    match_setting_list[4] = False
                    match_setting_list[5] = False
                if rand_clicked(click_coords):
                    match_setting_list[3] = False
                    match_setting_list[4] = True
                    match_setting_list[5] = False
                if black_clicked(click_coords):
                    match_setting_list[3] = False
                    match_setting_list[4] = False
                    match_setting_list[5] = True
                if start_match_clicked(click_coords):
                    game_screen(screen, timer, white_top(match_setting_list), player_or_ai(match_setting_list))
                    return

        pygame.display.flip()
    pygame.quit()


def game_screen(screen, timer, white_top, ai_status):
    # game variables
    last_moved = ["", (-1, -1), (-1, -1)]
    winner = ''
    game_over = False
    game_over_mode = ''
    selection = -1

    # Initial set up
    if white_top:
        white = Player('white', 'top', POSITIONS, WHITE_IMAGES, SMALL_WHITE_IMAGES, FORFEIT_COORDINATES, ai_status[1])
        top_avatar = white_avatar
        black = Player('black', 'bot', POSITIONS, BLACK_IMAGES, SMALL_BLACK_IMAGES, FORFEIT_COORDINATES, ai_status[0])
        bot_avatar = black_avatar

    else:
        white = Player('white', 'bot', POSITIONS, WHITE_IMAGES, SMALL_WHITE_IMAGES, FORFEIT_COORDINATES, ai_status[0])
        bot_avatar = white_avatar
        black = Player('black', 'top', POSITIONS, BLACK_IMAGES, SMALL_BLACK_IMAGES, FORFEIT_COORDINATES, ai_status[1])
        top_avatar = black_avatar
    avatar = [top_avatar, bot_avatar]
    player = [white, black]
    turn = 0
    count = 0

    # Main Game Loop
    run = True
    player[turn].check_options(last_moved, player[~turn & 1].positions, player[~turn & 1].pieces)
    while run:
        timer.tick(FPS)
        screen.fill(GREY)
        draw_board(screen, player, turn, selection, last_moved, avatar, player[turn].ai)
        draw_pieces(screen, white.pieces, white.positions, black.pieces, black.positions)
        draw_captured(screen, white.captured_pieces, black.captured_pieces)
        draw_check(screen, player[turn].under_check, player[turn].king_position)

        if selection != -1:
            valid_moves = player[turn].options[selection]
            draw_valid(screen, turn, valid_moves)

        if player[turn].promotion:
            if player[turn].ai:
                player[turn].pawn_promotion(player[turn].pawn_to_promo, 'queen')
                turn = ~turn & 1
                player[turn].check_options(last_moved, player[~turn & 1].positions, player[~turn & 1].pieces)
                player[turn].trim_invalid_moves(player[~turn & 1].pieces, player[~turn & 1].positions)
            else:
                promo_type = draw_pawn_promotion(screen, player[turn].colour, player[turn].top_or_bot,
                                                 player[turn].images)
                if promo_type != '':
                    player[turn].pawn_promotion(player[turn].pawn_to_promo, promo_type)
                    turn = ~turn & 1
                    player[turn].check_options(last_moved, player[~turn & 1].positions, player[~turn & 1].pieces)
                    player[turn].trim_invalid_moves(player[~turn & 1].pieces, player[~turn & 1].positions)
                    selection = -1

        if player[turn].ai and not game_over:
            count += 1
            if count >= 40:
                piece, move = find_random_move(player[turn].options)
                move_done, last_moved = player[turn].move_selected(piece, move, last_moved, player[~turn & 1].pieces,
                                                                   player[~turn & 1].positions)
                if move_done and not player[turn].promotion:
                    # Reset/Update values for next turn
                    turn = ~turn & 1
                    player[turn].check_options(last_moved, player[~turn & 1].positions, player[~turn & 1].pieces)
                    player[turn].trim_invalid_moves(player[~turn & 1].pieces, player[~turn & 1].positions)
                    selection = -1
                    move_done = False
                    count = 0

        # Event Handling
        for event in pygame.event.get():
            # x, y = pygame.mouse.get_pos()

            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_MOUSE_CLICK and not game_over and \
                    not player[turn].promotion and not player[turn].ai:
                # Convert pixel coordinates of cursor position into row/col of chess board
                # Note 0,0 is top left tile, while 7,7 is bottom right tile
                x_coord = (event.pos[0] - X_OFFSET) // TILE_SIZE
                y_coord = (event.pos[1] - Y_OFFSET) // TILE_SIZE
                click_coords = (x_coord, y_coord)

                # Determine if a white piece is selected
                if click_coords in player[turn].positions:
                    selection = player[turn].positions.index(click_coords)

                move_done, last_moved = player[turn].move_selected(selection, click_coords, last_moved,
                                                                   player[~turn & 1].pieces,
                                                                   player[~turn & 1].positions)

                if move_done and not player[turn].promotion:
                    # Reset/Update values for next turn
                    turn = ~turn & 1
                    player[turn].check_options(last_moved, player[~turn & 1].positions, player[~turn & 1].pieces)
                    player[turn].trim_invalid_moves(player[~turn & 1].pieces, player[~turn & 1].positions)
                    selection = -1
                    move_done = False

                # If forfeit button is pressed
                if player[turn].forfeit_button_boundary[0][0] <= event.pos[0] <= \
                        player[turn].forfeit_button_boundary[1][0] \
                        and player[turn].forfeit_button_boundary[0][1] <= event.pos[1] <= \
                        player[turn].forfeit_button_boundary[1][1]:
                    winner = player[~turn & 1].colour
                    game_over = True
                    game_over_mode = 'Forfeit'

            if event.type == pygame.KEYDOWN and game_over:
                # If enter key is pressed, reset the game, so they can play again with same settings
                if event.key == pygame.K_RETURN:
                    winner = ''
                    game_over = False
                    game_over_mode = ''
                    last_moved = ["", (-1, -1), (-1, -1)]
                    selection = -1
                    turn = 0
                    if white_top:
                        white = Player('white', 'top', POSITIONS, WHITE_IMAGES, SMALL_WHITE_IMAGES, FORFEIT_COORDINATES,
                                       ai_status[1])
                        top_avatar = white_avatar
                        black = Player('black', 'bot', POSITIONS, BLACK_IMAGES, SMALL_BLACK_IMAGES, FORFEIT_COORDINATES,
                                       ai_status[0])
                        bot_avatar = black_avatar

                    else:
                        white = Player('white', 'bot', POSITIONS, WHITE_IMAGES, SMALL_WHITE_IMAGES, FORFEIT_COORDINATES,
                                       ai_status[0])
                        bot_avatar = white_avatar
                        black = Player('black', 'top', POSITIONS, BLACK_IMAGES, SMALL_BLACK_IMAGES, FORFEIT_COORDINATES,
                                       ai_status[1])
                        top_avatar = black_avatar
                    avatar = [top_avatar, bot_avatar]
                    player = [white, black]
                    player[turn].check_options(last_moved, player[~turn & 1].positions, player[~turn & 1].pieces)
                elif event.key == pygame.K_ESCAPE:  # Return to main menu
                    return

        # Check for game over and if it is, draw the corresponding screen
        if game_over:
            draw_game_over(screen, game_over_mode, winner)
        else:
            game_over, game_over_mode, winner = player[turn].check_game_over(player[~turn & 1].colour)

        pygame.display.flip()
    pygame.quit()


def main():
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption('Pygame Chess!')
    timer = pygame.time.Clock()
    pygame.init()
    main_menu(screen, timer)


if __name__ == "__main__":
    main()
