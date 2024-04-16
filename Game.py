import pygame

pygame.init()

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


# Board variables
TILE_SIZE = 80
BOARD_DIMENSION = TILE_SIZE * 8
X_OFFSET = 294
Y_OFFSET = 26

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
player1_avatar_colour = GREY
player2_avatar_colour = GREY

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
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = -1
valid_moves = []
last_moved = []

# load in game piece images (queen, king, rook, bishop, knight, pawn) for black and white
PIECE_DIMENSIONS = (TILE_SIZE * 0.8, TILE_SIZE * 0.8)
PAWN_DIMENSIONS = (TILE_SIZE * 0.65, TILE_SIZE * 0.65)
SMALL_PIECE_DIMENSIONS = (TILE_SIZE * 0.45, TILE_SIZE * 0.45)
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

# check variables/ flashing counter
counter = 0
winner = ''
game_over = False


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
    # pygame.draw.rect(screen, 'yellow', [X_OFFSET + white_positions[last_moved[1]][0] * TILE_SIZE,
    #                                     Y_OFFSET + white_positions[last_moved[1]][1] * TILE_SIZE, TILE_SIZE, TILE_SIZE])
    # pygame.draw.rect(screen, 'yellow', [X_OFFSET + black_positions[last_moved[0]][0] * TILE_SIZE,
    #                                     Y_OFFSET + black_positions[last_moved[0]][1] * TILE_SIZE, TILE_SIZE,TILE_SIZE])

    # Drawing grid lines
    for i in range(9):
        pygame.draw.line(screen, 'black', (X_OFFSET, Y_OFFSET + TILE_SIZE * i),
                         (X_OFFSET + BOARD_DIMENSION, Y_OFFSET + TILE_SIZE * i), 2)
        pygame.draw.line(screen, 'black', (X_OFFSET + TILE_SIZE * i, Y_OFFSET),
                         (X_OFFSET + TILE_SIZE * i, Y_OFFSET + BOARD_DIMENSION), 2)

    # Drawing avatar area
    if turn_step < 2:
        player1_avatar_colour = 'grey'
        player2_avatar_colour = GREY
    elif turn_step >= 2:
        player1_avatar_colour = GREY
        player2_avatar_colour = 'grey'
    pygame.draw.rect(screen, player1_avatar_colour, [0, HEIGHT-200, 200, 200])
    pygame.draw.rect(screen, 'black', [0, HEIGHT - 200, 200, 200], 2)
    pygame.draw.rect(screen, player2_avatar_colour, [WIDTH-200, 0, 200, 200])
    pygame.draw.rect(screen, 'black', [WIDTH-200, 0, 200, 200], 2)

    # Drawing forfeit button
    # screen.blit(medium_font.render('FORFEIT', True, 'black'), (998, 631))

# Draws all the pieces onto the board according to their current position
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            screen.blit(white_pawn, (TILE_SIZE * (white_positions[i][0] + 0.175) + X_OFFSET,
                                     TILE_SIZE * (white_positions[i][1] + 0.2) + + Y_OFFSET ))
        else:
            screen.blit(white_images[index], (TILE_SIZE * (white_positions[i][0] + 0.1) + X_OFFSET,
                                              TILE_SIZE * (white_positions[i][1] + 0.12) + Y_OFFSET))

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (TILE_SIZE * (black_positions[i][0] + 0.175) + X_OFFSET,
                                     TILE_SIZE * (black_positions[i][1] + 0.2) + + Y_OFFSET ))
        else:
            screen.blit(black_images[index], (TILE_SIZE * (black_positions[i][0] + 0.1) + X_OFFSET,
                                              TILE_SIZE * (black_positions[i][1] + 0.12) + Y_OFFSET))


# Main Game Loop
run = True
while run:
    timer.tick(fps)
    screen.fill(GREY)
    draw_board()
    draw_pieces()

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.flip()
pygame.quit()
