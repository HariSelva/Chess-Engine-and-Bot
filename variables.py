from constants import *

screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Pygame Chess!')
timer = pygame.time.Clock()

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
white_king_position = (3, 0)
black_king_position = (3, 7)

valid_moves = []
last_moved = ["", (-1, -1), (-1, -1)]
en_passant_coords = (-1, -1)
castling_moves = []

# check variables for determine various states of the game
winner = ''
game_over = False
game_over_mode = ''
under_check = False
selection = -1
white_promotion = False
white_promotion_index = -1
black_promotion = False
black_promotion_index = -1

# 0-Both castling moves are available; 1-Only King side available; 2-Only Queen side available; 3-Neither is available
white_castling_state = 0
black_castling_state = 0

# 0-whites turn no selection; 1-whites turn piece selected; 2-black turn no selection; 3-black turn piece selected
turn_step = 0
