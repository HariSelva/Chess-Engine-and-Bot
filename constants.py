import pygame
pygame.init()

# Mouse Event Constant(s)
LEFT_MOUSE_CLICK = 1

# Use size of first monitor/display to set the screen size, while ensuring the dimensions are even
WINDOW_DIMENSIONS = pygame.display.get_desktop_sizes()
WIDTH = int(WINDOW_DIMENSIONS[0][0] * 0.8)
HEIGHT = int(WINDOW_DIMENSIONS[0][1] * 0.8)
if WIDTH % 2 == 1:
    WIDTH += 1
if HEIGHT % 2 == 1:
    HEIGHT += 1
print('Screen Dimensions:', WIDTH, ' x ', HEIGHT)

# Fonts
FONT = pygame.font.SysFont('Times New Roman', 20)
MEDIUM_FONT = pygame.font.SysFont('Times New Roman', 40)
BIG_FONT = pygame.font.SysFont('Times New Roman', 60)

# Size and position constants for the board and images
TILE_SIZE = int(HEIGHT * 0.925/8)
BOARD_DIMENSION = TILE_SIZE * 8
X_OFFSET = int(WIDTH * 0.239)
Y_OFFSET = int(HEIGHT * 0.038)
AVATAR_TILE_SIZE = int(HEIGHT * 0.289)
AVATAR_SIZE = int(AVATAR_TILE_SIZE * 0.75)
PIECE_DIMENSIONS = (TILE_SIZE * 0.8, TILE_SIZE * 0.8)
PAWN_DIMENSIONS = (TILE_SIZE * 0.65, TILE_SIZE * 0.65)
SMALL_PIECE_DIMENSIONS = (TILE_SIZE * 0.45, TILE_SIZE * 0.45)
FORFEIT_COORDS = [(int(WIDTH * 0.045), int(HEIGHT * 0.023)), (int(WIDTH * 0.813), int(HEIGHT * 0.912))]

# Colour Variables
WHITE = (255, 255, 255)
GREY = (128, 128, 128)
BEIGE = (232, 220, 202)
GREEN = (110, 145, 0)
# YELLOW = (204, 204, 0)
# BLUE = (50, 255, 255)
# BLACK = (0, 0, 0)

# load in game images for Black
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

# load in game images for White
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

# List of pieces and their corresponding images
PIECE_LIST = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
WHITE_IMAGES = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
SMALL_WHITE_IMAGES = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
BLACK_IMAGES = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
SMALL_BLACK_IMAGES = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]

# Miscellaneous
PROMOTION_OPTIONS = ['bishop', 'knight', 'rook', 'queen']
FPS = 60

