import sys, pygame, math
from model import *
    
pygame.init()
size = width, height = 800, 800
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Chess')
running = True

white_pawn_img = pygame.image.load('pics/wP.png')
black_pawn_img = pygame.image.load('pics/bP.png')
white_king_img = pygame.image.load('pics/wK.png')
black_king_img = pygame.image.load('pics/bK.png')
white_knight_img = pygame.image.load('pics/wN.png')
black_knight_img = pygame.image.load('pics/bN.png')
black_bishop_img = pygame.image.load('pics/bB.png')
white_bishop_img = pygame.image.load('pics/wB.png')
black_queen_img = pygame.image.load('pics/bQ.png')
white_queen_img = pygame.image.load('pics/wQ.png')
black_rook_img = pygame.image.load('pics/bR.png')
white_rook_img = pygame.image.load('pics/wR.png')

def map_coords(c, r):
    return (math.floor(r/100), math.floor(c/100))

def map_index(c, r):
    return (r*100+5, c*100+5)

def start_game():
    for i in range(8):
        Pawn(1, i, 'black')

    for i in range(8):
        Pawn(6, i, 'white')

    Rook(0, 0, 'black')
    Rook(0, 7, 'black')
    Rook(7, 0, 'white')
    Rook(7, 7, 'white')

    Knight(0, 1, 'black')
    Knight(0, 6, 'black')
    Knight(7, 1, 'white')
    Knight(7, 6, 'white') 

    Bishop(0, 2, 'black')
    Bishop(0, 5, 'black')
    Bishop(7, 2, 'white')
    Bishop(7, 5, 'white')

    Queen(0, 3, 'black')
    Queen(7, 3, 'white')

    King(0, 4, 'black')
    King(7, 4, 'white')

    return b.squares

def draw_pieces():
    for i in range(8):
        for j in range(8):
            piece = b.squares[i][j]
            square = type(piece)
            
            
            if square == Pawn and piece.cl == 'white':
                screen.blit(white_pawn_img, map_index(piece.pos[0], piece.pos[1]))
            elif square == Pawn and piece.cl == 'black':
                screen.blit(black_pawn_img, map_index(piece.pos[0], piece.pos[1]))

            if square == Rook and piece.cl == 'white':
                screen.blit(white_rook_img, map_index(piece.pos[0], piece.pos[1]))
            elif square == Rook and piece.cl == 'black':
                screen.blit(black_rook_img, map_index(piece.pos[0], piece.pos[1]))

            if square == Knight and piece.cl == 'white':
                screen.blit(white_knight_img, map_index(piece.pos[0], piece.pos[1]))
            elif square == Knight and piece.cl == 'black':
                screen.blit(black_knight_img, map_index(piece.pos[0], piece.pos[1]))

            if square == Bishop and piece.cl == 'white':
                screen.blit(white_bishop_img, map_index(piece.pos[0], piece.pos[1]))
            elif square == Bishop and piece.cl == 'black':
                screen.blit(black_bishop_img, map_index(piece.pos[0], piece.pos[1]))

            if square == Queen and piece.cl == 'white':
                screen.blit(white_queen_img, map_index(piece.pos[0], piece.pos[1]))
            elif square == Queen and piece.cl == 'black':
                screen.blit(black_queen_img, map_index(piece.pos[0], piece.pos[1]))
                
            if square == King and piece.cl == 'white':
                screen.blit(white_king_img, map_index(piece.pos[0], piece.pos[1]))
            elif square == King and piece.cl == 'black':
                screen.blit(black_king_img, map_index(piece.pos[0], piece.pos[1]))

start_game()

turn = 1

def highlight_squares(p):
    moves = p.can_move()
    [pygame.draw.circle(screen, (200, 166, 13), map(lambda x: x + 15, map_index(p.pos[0], p.pos[1])), 15) for _ in range(len(moves))]


def black_is_in_check():
    for row in b.squares:
        for col in row:
            if type(col) == King and col.cl == 'black':
                if col.in_check():
                    return col.cl
    return False

def white_is_in_check():
    for row in b.squares:
        for col in row:
            if type(col) == King and col.cl == 'white':
                if col.in_check():
                    return col.cl
    return False

def is_check_mate():
    for row in b.squares:
        for col in row:
            if type(col) == King and col.check_mate():
                return True

def castle(king, sq):
    if not king.has_moved:
        if king.cl == 'white' and sq == [7, 2]:
            if not b.squares[7][0].has_moved and b.squares[7][1] is None and b.squares[7][2] is None and b.squares[7][3] is None:
                attack_matrix = b.attack('black')
                for i in range(0, king.pos[1]+1):
                    if attack_matrix[7][i]:
                        return False
                king.pos = (7, 2)
                b.squares[king.pos[0]][king.pos[1]] = king
                b.squares[7][4] = None
                b.squares[7][3] = b.squares[7][0]
                b.squares[7][0].pos = (7, 3)
                b.squares[7][0] = None
        elif king.cl == 'white' and sq == [7, 6]:
            if not b.squares[7][7].has_moved and b.squares[7][5] is None and b.squares[7][6] is None:
                attack_matrix = b.attack('black')
                for i in range(king.pos[1], 7):
                    if attack_matrix[7][i]:
                        return False
                king.pos = (7, 6)
                b.squares[king.pos[0]][king.pos[1]] = king
                b.squares[7][4] = None
                b.squares[7][5] = b.squares[7][7]
                b.squares[7][7].pos = (7, 5)
                b.squares[7][7] = None
        elif king.cl == 'black' and sq == [0, 2]:
            if not b.squares[0][0].has_moved and b.squares[0][1] is None and b.squares[0][2] is None and b.squares[0][3] is None:
                attack_matrix = b.attack('white')
                for i in range(0, king.pos[1]+1):
                    if attack_matrix[0][i] != False:
                        return False
                king.pos = (0, 2)
                b.squares[king.pos[0]][king.pos[1]] = king
                b.squares[0][4] = None
                b.squares[0][3] = b.squares[0][0]
                b.squares[0][0].pos = (0, 3)
                b.squares[0][0] = None
        elif king.cl == 'black' and sq == [0, 6]:
            if not b.squares[0][7].has_moved and b.squares[0][5] is None and b.squares[0][6] is None:
                attack_matrix = b.attack('white')
                for i in range(king.pos[1], 7):
                    if attack_matrix[0][i] != False:
                        return False
                king.pos = (0, 6)
                b.squares[king.pos[0]][king.pos[1]] = king
                b.squares[0][4] = None
                b.squares[0][5] = b.squares[0][7]
                b.squares[0][7].pos = (0, 5)
                b.squares[0][7] = None

    return False

def promote(pawn):
    b.squares[pawn.pos[0]][pawn.pos[1]] = Queen(pawn.pos[0], pawn.pos[1], pawn.cl)



while running:
    # highlight = []
    if is_check_mate():
        print('checkmate!')
        exit()

    if black_is_in_check() or white_is_in_check():
        print('king is attacked!')


    screen.fill((83, 85, 83))
    for i in range(8):
        for j in range(8):
            if j % 2  == 0 and i % 2 == 0 or j % 2 != 0 and i % 2 != 0:
                cl = (240, 217, 181)
            else:
                cl = (181, 136, 99)
            pygame.draw.rect(screen, cl, (j*100, i*100, j*100+100, i*100+100))

    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            start_pos = pygame.mouse.get_pos()
            r, c = map_coords(*start_pos)

            piece = b.squares[r][c]
                
            if piece is not None:
                if turn == 1 and piece.cl == 'white' or turn == 2 and piece.cl == 'black':

                    moves = piece.can_move()
                    print(f'{type(piece)} can move to: {moves}')
                    draw_pieces()
                else:
                    moves = []
            else:
                moves = None
                print('False')

        if event.type == pygame.MOUSEBUTTONUP and piece is not None:
            
            end_pos = pygame.mouse.get_pos()
            r1, c1 = map_coords(*end_pos)

            print(r1, c1)

            if type(piece) == King and [r1, c1] == [7, 2] and [r, c] == [7, 4]:
                if castle(piece, [7, 2]):
                    turn = 3 - turn
                    continue
            elif type(piece) == King and [r1, c1] == [7, 6] and [r, c] == [7, 4]:
                if castle(piece, [7, 6]):
                    turn = 3 - turn
                    continue
            elif type(piece) == King and [r1, c1] == [0, 2] and [r, c] == [0, 4]:
                if castle(piece, [0, 2]):
                    turn = 3 - turn
                    continue
            elif type(piece) == King and [r1, c1] == [0, 6] and [r, c] == [0, 4]:       
                if castle(piece, [0, 6]):
                    turn = 3 - turn
                    continue
     
            

            if [r1, c1] in moves:
                temp = None
                piece.pos = [r1, c1]
                if b.is_occupied(r1, c1):
                    temp = b.squares[r1][c1]
                b.squares[r1][c1] = piece
                b.squares[r][c] = None
                if black_is_in_check() and turn == 2:
                    piece.pos = [r, c]
                    b.squares[r][c] = piece
                    if temp:
                        b.squares[r1][c1] = temp
                    else: 
                        b.squares[r1][c1] = None
                    continue
                if white_is_in_check() and turn == 1:
                    piece.pos = [r, c]
                    b.squares[r][c] = piece
                    if temp:
                        b.squares[r1][c1] = temp
                    else:
                        b.squares[r1][c1] = None
                    continue
                if type(piece) == Rook or type(piece) == King:
                    piece.has_moved = True
                turn = 3 - turn

            if type(piece) == Pawn and piece.cl == 'white' and r1 == 0:
                promote(piece)
            elif type(piece) == Pawn and piece.cl == 'black' and r1 == 7:
                promote(piece)
    
    draw_pieces()
    pygame.display.update()