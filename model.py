class Board:
    def __init__(self):
        self.squares = [[None] * 8 for _ in range(8)]

    def is_occupied(self, x, y):
        if self.squares[x][y] != None:
            return True
        return False

    def attack(self, cl):
        attack_matrix = [[False] * 8 for _ in range(8)]
        for r in range(len(self.squares)):
            for c in range(len(self.squares[r])):
                piece = self.squares[r][c]
                if piece is not None:
                    if piece.cl == cl and type(piece) != Pawn and type(piece) != King:
                        moves = piece.can_move()
                        for m in moves:
                            attack_matrix[m[0]][m[1]] = True
                    elif piece.cl == cl and type(piece) == Pawn:
                        if cl == 'white':
                            x1 = piece.pos[0] - 1
                            y1 = piece.pos[1] + 1
                            x2 = piece.pos[0] - 1
                            y2 = piece.pos[1] - 1
                            if 0 <= x1 <= 7 and 0 <= y1 <= 7:
                                attack_matrix[x1][y1] = True
                            if 0 <= x2 <= 7 and 0 <= y2 <= 7:
                                attack_matrix[x2][y2] = True
                        elif cl == 'black':
                            x1 = piece.pos[0] + 1
                            y1 = piece.pos[1] + 1
                            x2 = piece.pos[0] + 1
                            y2 = piece.pos[1] - 1
                            if 0 <= x1 <= 7 and 0 <= y1 <= 7:
                                attack_matrix[x1][y1] = True
                            if 0 <= x2 <= 7 and 0 <= y2 <= 7:
                                attack_matrix[x2][y2] = True
                    elif type(piece) == King and piece.cl == cl:
                        dirs = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
                        for d in dirs:
                            if 0 <= piece.pos[0] + d[0] <= 7 and 0 <= piece.pos[1] + d[1] <= 7:
                                attack_matrix[piece.pos[0] + d[0]][piece.pos[1] + d[1]] = True
        return attack_matrix

b = Board()

class Pawn(Board):
    def __init__(self, x, y, cl):
        self.cl = cl
        Board.__init__(self)
        self.pos = (x, y)
        b.squares[x][y] = self

    def can_move(self):
        moves = []
        dirs = []
        if self.cl == 'white':
            if 0 <= self.pos[0]-1 <= 7 and 0 <= self.pos[1]+1 <= 7:
                if b.is_occupied(self.pos[0]-1, self.pos[1]+1) and b.squares[self.pos[0]-1][self.pos[1]+1].cl == 'black':
                    dirs.append((-1, 1))
            if 0 <= self.pos[0]-1 <= 7 and 0 <= self.pos[1]-1 <= 7:
                if b.is_occupied(self.pos[0]-1, self.pos[1]-1) and b.squares[self.pos[0]-1][self.pos[1]-1].cl == 'black':
                    dirs.append((-1, -1))
            if 0 <= self.pos[0]-1 <= 7 and 0 <= self.pos[1] <= 7:
                if not b.is_occupied(self.pos[0]-1, self.pos[1]):
                    dirs.append((-1, 0))
            if self.pos[0] == 6 and not b.is_occupied(self.pos[0] - 2, self.pos[1]) and not b.is_occupied(self.pos[0] - 1, self.pos[1]):
                moves.append([self.pos[0]-2, self.pos[1]])

        elif self.cl == 'black':
            if 0 <= self.pos[0]+1 <= 7 and 0 <= self.pos[1]+1 <= 7:
                if b.is_occupied(self.pos[0]+1, self.pos[1]+1) and b.squares[self.pos[0]+1][self.pos[1]+1].cl == 'white':
                    dirs.append((1, 1))
            if 0 <= self.pos[0]+1 <= 7 and 0 <= self.pos[1]-1 <= 7:
                if b.is_occupied(self.pos[0]+1, self.pos[1]-1) and b.squares[self.pos[0]+1][self.pos[1]-1].cl == 'white':
                    dirs.append((1, -1))
            if 0 <= self.pos[0]+1 <= 7 and 0 <= self.pos[1] <= 7:
                if not b.is_occupied(self.pos[0]+1, self.pos[1]):
                    dirs.append((1, 0))
            if self.pos[0] == 1 and not b.is_occupied(self.pos[0] + 2, self.pos[1]) and not b.is_occupied(self.pos[0] + 1, self.pos[1]):
                moves.append([self.pos[0]+2, self.pos[1]])

        for d in dirs:
            moves.append([self.pos[0] + d[0], self.pos[1] + d[1]])            

        return moves

class Rook:
    def __init__(self, x, y, cl):
        self.cl = cl
        self.pos = (x, y)
        b.squares[x][y] = self
        self.has_moved = False
    def can_move(self):
        moves = []
        dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]

        for d in dirs:
            m = [*self.pos]
            while 0 <= m[0] + d[0] <= 7 and 0 <= m[1] + d[1] <= 7:
                m[0] += d[0]
                m[1] += d[1]
                if b.is_occupied(m[0], m[1]) and b.squares[m[0]][m[1]].cl == self.cl:
                    break
                elif not b.is_occupied(m[0], m[1]):
                    moves.append([*m])
                elif b.is_occupied(m[0], m[1]) and b.squares[m[0]][m[1]].cl != self.cl:
                    moves.append([*m])
                    break
        return moves

class Bishop:
    def __init__(self, x, y, cl):
        self.cl = cl
        self.pos = (x, y)
        b.squares[x][y] = self

    def can_move(self):
        moves = []
        dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        for d in dirs:
            m = [*self.pos]
            while 0 <= m[0] + d[0] <= 7 and 0 <= m[1] + d[1] <= 7:
                m[0] += d[0]
                m[1] += d[1]
                if b.is_occupied(m[0], m[1]) and b.squares[m[0]][m[1]].cl == self.cl:
                    break
                elif not b.is_occupied(m[0], m[1]):
                    moves.append([*m])
                elif b.is_occupied(m[0], m[1]) and b.squares[m[0]][m[1]].cl != self.cl:
                    moves.append([*m])
                    break
        return moves

class Knight:
    def __init__(self, x, y, cl):
        self.pos = (x, y)
        self.cl = cl
        b.squares[x][y] = self

    def can_move(self):
        moves = []
        dirs = [(2, 1), (2, -1), (1, 2), (1, -2), (-1, -2), (-1, 2), (-2, 1), (-2, -1)]
        for d in dirs:
            if 0 <= self.pos[0] + d[0] <= 7 and 0 <= self.pos[1] + d[1] <= 7:
                if not b.is_occupied(self.pos[0] + d[0], self.pos[1] + d[1]):
                    moves.append([self.pos[0] + d[0], self.pos[1] + d[1]])
                elif b.is_occupied(self.pos[0] + d[0], self.pos[1] + d[1]) and b.squares[self.pos[0] + d[0]][self.pos[1] + d[1]].cl != self.cl:
                    moves.append([self.pos[0] + d[0], self.pos[1] + d[1]])
                else:
                    continue
        return moves

class Queen:
    def __init__(self, x, y, cl):
        self.pos = (x, y)
        self.cl = cl
        b.squares[x][y] = self

    def can_move(self):
        moves = []
        dirs = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (-1, 0), (0, -1)]

        for d in dirs:
            m = [*self.pos]
            while 0 <= m[0] + d[0] <= 7 and 0 <= m[1] + d[1] <= 7:
                m[0] += d[0]
                m[1] += d[1]
                if b.is_occupied(m[0], m[1]) and b.squares[m[0]][m[1]].cl == self.cl:
                    break
                elif not b.is_occupied(m[0], m[1]):
                    moves.append([*m])
                elif b.is_occupied(m[0], m[1]) and b.squares[m[0]][m[1]].cl != self.cl:
                    moves.append([*m])
                    break
        return moves

class King:
    def __init__(self, x, y, cl):
        self.pos = (x, y)
        self.cl = cl
        self.has_moved = False
        self.attacked = False
        b.squares[x][y] = self

    def can_move(self):
        moves = []
        danger_moves = []
        dirs = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        for d in dirs:
            if 0 <= self.pos[0] + d[0] <= 7 and 0 <= self.pos[1] + d[1] <= 7:
                if not b.is_occupied(self.pos[0] + d[0], self.pos[1] + d[1]) or b.squares[self.pos[0] + d[0]][self.pos[1] + d[1]].cl != self.cl:
                    moves.append([self.pos[0] + d[0], self.pos[1] + d[1]])
        for i in range(len(b.squares)):
            for j in range(len(b.squares[i])):
                p = b.squares[i][j]
                if p is not None and p.cl != self.cl and type(p) != King:
                    if type(p) == Pawn:
                        if self.cl == 'white':
                            x1 = p.pos[0] + 1
                            y1 = p.pos[1] + 1
                            x2 = p.pos[0] + 1
                            y2 = p.pos[1] - 1
                            if 0 <= x1 <= 7 and 0 <= y1 <= 7:
                                danger_moves.append([x1, y1])
                            if 0 <= x2 <= 7 and 0 <= y2 <= 7:
                                danger_moves.append([x2, y2])
                        elif self.cl == 'black':
                            x1 = p.pos[0] - 1
                            y1 = p.pos[1] + 1
                            x2 = p.pos[0] - 1
                            y2 = p.pos[1] - 1
                            if 0 <= x1 <= 7 and 0 <= y1 <= 7:
                                danger_moves.append([x1, y1])
                            if 0 <= x2 <= 7 and 0 <= y2 <= 7:
                                danger_moves.append([x2, y2])
                    else:
                        danger_moves = p.can_move()
                for m in danger_moves:
                    if m in moves:
                        moves.remove(m)
                
                for m in moves:
                    if self.cl == 'black':
                        attack_matrix = b.attack('white')
                        if attack_matrix[m[0]][m[1]]:
                            moves.remove(m)
                    elif self.cl == 'white':
                        attack_matrix = b.attack('black')
                        if attack_matrix[m[0]][m[1]]:
                            moves.remove(m)
        return moves

    def in_check(self):
        if self.cl == 'white':
            attack_matrix = b.attack('black')
        else:
            attack_matrix = b.attack('white')

        if attack_matrix[self.pos[0]][self.pos[1]]:
            return True
        return False

    def check_mate(self):
        dirs = [(0, 1), (1, 0), (-1, 0), (0, -1), (1, 1), (-1, 1), (-1, -1), (1, -1)]
        if self.cl == 'white':
            attack_matrix = b.attack('black')
        elif self.cl == 'black':
            attack_matrix = b.attack('white')

        
        if self.in_check():
            for d in dirs:
                if 0 <= self.pos[0] + d[0] <= 7 and 0 <= self.pos[1] + d[1] <= 7:
                    if not attack_matrix[self.pos[0] + d[0]][self.pos[1] + d[1]]:
                        if not b.is_occupied(self.pos[0] + d[0], self.pos[1] + d[1]):
                            return False

            for row in b.squares:
                for col in row:
                    if col is not None and col.cl == self.cl:
                        moves = col.can_move()
                        old_pos = [*col.pos]
                        for m in moves:
                            temp = None
                            col.pos = [m[0], m[1]]
                            if b.is_occupied(m[0], m[1]) and b.squares[m[0]][m[1]].cl != self.cl:
                                temp = b.squares[m[0]][m[1]]
                            b.squares[m[0]][m[1]] = col
                            b.squares[old_pos[0]][old_pos[1]] = None
                            if not self.in_check():
                                col.pos = [old_pos[0], old_pos[1]]
                                b.squares[old_pos[0]][old_pos[1]] = col
                                if temp:
                                    b.squares[m[0]][m[1]] = temp
                                else: 
                                    b.squares[m[0]][m[1]] = None
                                return False
                            else:
                                col.pos = [old_pos[0], old_pos[1]]
                                b.squares[old_pos[0]][old_pos[1]] = col
                                if temp:
                                    b.squares[m[0]][m[1]] = temp
                                else: 
                                    b.squares[m[0]][m[1]] = None
            return True

def check_move(king, piece, new_pos):
    old_pos = piece.pos
    piece.pos = new_pos
    temp_piece = None
    if b.squares[new_pos[0]][new_pos[1]]:
        temp_piece = b.squares[new_pos[0]][new_pos[1]]
    b.squares[piece.pos[0]][piece.pos[1]] = None
    b.squares[new_pos[0]][new_pos[1]] = piece

    if king.in_check():
        piece.pos = old_pos
        if temp_piece:
            b.squares[new_pos[0]][new_pos[1]] = temp_piece
        else:
            b.squares[new_pos[0]][new_pos[1]] = None
        b.squares[old_pos[0]][old_pos[1]] = piece
        return False
    return True