class chess:
    white = []
    black = []
    Moves = []

    def __init__(self, init_pos: list, cost: int, color: int,
                 piece: int, number: int):
        self.init_pos = init_pos  # Stores the initial Position of the chess piece
        self.pos = init_pos  # Stores the current Position of the chess piece
        # stores the temporary position of chess, made to be used in Drag and Drop and legal move
        self.temp_pos = init_pos
        self.check_pos = init_pos
        self.cost = cost  # Stores the cost of Chess piece
        # stores color of chess piece: (-1) - White, 1 - Black
        self.color = color
        self.piece = piece  # 0 - King, 1 - Queen, 2 - Rook, 3 - Bishop, 4 - Knight, 5 - Pawn
        self.captured = False  # variable tells if the piece is captured
        self.capture = False  # variable that does the same as above but to be used for legal moves
        # stores the serial number of the chess piece ( different for every piece )
        self.number = number
        self.delx = 0  # distance of the cursor position in x direction from self.pos
        self.dely = 0  # distance of the cursor position in y direction from self.pos
        self.moves = 0  # number of moves played by the piece
        self.captures = 0  # number of times the piece have captured a piece
        # if the move would be en passant it would store the position
        self.en_passant = [False, False]
        self.castling = []

        if self.color == -1:
            chess.white.append(self)
        else:
            chess.black.append(self)

    # returns the set of all positions of given color, else give all other position of the color given except the exception(the exception's number is given) given
    def occupied_pos(color: int, _except=None, __except=None):
        if color == -1:
            return [tuple(i.pos) for i in chess.white if ((i.number != _except) and (i.captured == False))]
            # returns the list of all the white positions except the exception
        elif color == +1:
            return [tuple(i.pos) for i in chess.black if ((i.number != _except) and (i.captured == False))]
            # returns the list of all the black positions except the exception
        elif color == 0:
            return ([tuple(i.pos) for i in chess.white if ((i.number != _except) and (i.number != __except) and (i.captured == False))]+[tuple(i.pos) for i in chess.black if ((i.number != _except) and (i.number != __except) and (i.captured == False))])

    def total_legal_moves(colour):
        moves = set()
        if colour == 1:
            for i in chess.black:
                for position in i.legal_moves(False, tuple(i.pos)):
                    moves.add(position)
        if colour == -1:
            for i in chess.white:
                for position in i.legal_moves(False, tuple(i.pos)):
                    moves.add(position)
        return moves

    def total_cost(colour):
        cost = 0
        if colour == 1:
            for i in chess.black:
                if i.captured == False:
                    cost += i.cost
        if colour == -1:
            for i in chess.white:
                if i.captured == False:
                    cost += i.cost
        return cost

    def available_pieces(colour, piece_value):
        if colour == -1:
            return [i for i in chess.white if (i.captured == False) and (i.piece == piece_value)]
        if colour == 1:
            return [i for i in chess.black if (i.captured == False) and (i.piece == piece_value)]

    # if any object is at that place then set it to be captured
    def captured_pos(self, position, type=False):
        if self.color == -1:
            for i in chess.black:
                if i.captured == False:
                    if i.pos == position:
                        if type == True:
                            i.capture = False
                        else:
                            i.capture = True

        if self.color == 1:
            for i in chess.white:
                if i.captured == False:
                    if i.pos == position:
                        if type == True:
                            i.capture = False
                        else:
                            i.capture = True

    def check(colour):
        if colour == -1:
            for i in chess.white:
                if i.piece == 0 and i.captured == False:  # ie the piece is *King*
                    for elem in chess.black:
                        if i.captured == False and elem.capture == False and elem.captured == False:
                            if i.pos in elem.legal_moves(False, (), True):
                                return True
                    return False
        if colour == 1:
            for i in chess.black:
                if i.piece == 0 and i.captured == False:  # ie the piece is *King*
                    for elem in chess.white:
                        if elem.captured == False and elem.capture == False and elem.captured == False:
                            if i.pos in elem.legal_moves(False, (), True):
                                return True
                    return False

    def attacked_pos(colour):
        positions = set()
        if colour == -1:
            for i in chess.white:
                if i.captured == False and i.capture == False:
                    for pos in i.legal_moves(False, (), True):
                        positions.add(pos)
        else:
            for i in chess.black:
                if i.captured == False and i.capture == False:
                    for pos in i.legal_moves(False, (), True):
                        positions.add(pos)
        return positions

    # returns the object with the serial number given

    def obj_from_num(num):
        for i in chess.white:
            if i.number == num:
                return i
        for i in chess.black:
            if i.number == num:
                return i

    def obj_from_pos(position):
        for i in chess.white:
            if i.pos == position:
                return i
        for i in chess.black:
            if i.pos == position:
                return i

    # if type is True, it means that it is needed to check if the given position is true, else it means to return a set of legal moves
    def legal_moves(self, type: bool, position=tuple(), trial=False):
        legal_moves = set()
        terminate = False
        if self.captured == False:
            if self.piece == 0:  # legal move of *King*
                for x in range(8):
                    for y in range(8):
                        if (abs(self.pos[0]-x) == 1) or (abs(self.pos[1]-y) == 1):
                            if (abs(self.pos[0]-x) == abs(self.pos[1] - y)):
                                if trial == False:
                                    if (x, y) not in chess.attacked_pos(-self.color):
                                        if (x, y) not in chess.occupied_pos(self.color, self.number):
                                            self.check_pos = self.pos
                                            self.pos = (x, y)
                                            if chess.check(self.color) == False:
                                                self.pos = self.check_pos
                                                legal_moves.add((x, y))
                                            self.pos = self.check_pos
                                else:
                                    legal_moves.add((x, y))
                            if (self.pos[0] == x and self.pos[1] != y) or (self.pos[1] == y and self.pos[0] != x):
                                if trial == False:
                                    if (x, y) not in chess.attacked_pos(-self.color):
                                        if (x, y) not in chess.occupied_pos(self.color, self.number):
                                            self.check_pos = self.pos
                                            self.pos = (x, y)
                                            if chess.check(self.color) == False:
                                                self.pos = self.check_pos
                                                legal_moves.add((x, y))
                                            self.pos = self.check_pos
                                else:
                                    legal_moves.add((x, y))
                                    
                if trial == False:
                    if self.moves == 0:
                        for rook in chess.available_pieces(self.color, 2):
                            if rook.moves == 0:
                                if (self.pos[0]-rook.pos[0]) > 0:
                                    for x in range(self.pos[0], rook.pos[0]-1, -1):
                                        if (x, self.pos[1]) in chess.attacked_pos(-self.color):
                                            break
                                        if (x, self.pos[1]) in chess.occupied_pos(0, self.number, rook.number):
                                            break
                                    else:
                                        legal_moves.add(
                                            (self.pos[0]-2, self.pos[1]))
                                        self.castling.append(
                                            [(self.pos[0]-2, self.pos[1]), rook.number, (self.pos[0]-1, self.pos[1])])
                                    continue
                                else:
                                    for x in range(self.pos[0], rook.pos[0]+1):
                                        if (x, self.pos[1]) in chess.attacked_pos(-self.color):
                                            break
                                        if (x, self.pos[1]) in chess.occupied_pos(0, self.number, rook.number):
                                            break
                                    else:
                                        legal_moves.add(
                                            (self.pos[0]+2, self.pos[1]))
                                        self.castling.append(
                                            [(self.pos[0]+2, self.pos[1]), rook.number, (self.pos[0]+1, self.pos[1])])
                                    continue

            elif self.piece == 1:  # legal move of Queen

                for x in range(self.pos[0] - 1, -1, -1):
                    # Searching for legal moves in horizontally backward direction until a black or white piece comes in the way
                    if trial == True:
                        if (x, self.pos[1]) in chess.occupied_pos(self.color, self.number):
                            legal_moves.add((x, self.pos[1]))
                            break
                        elif (x, self.pos[1]) in chess.occupied_pos(-self.color):
                            legal_moves.add((x, self.pos[1]))
                            break
                        else:
                            legal_moves.add((x, self.pos[1]))
                    else:
                        if (x, self.pos[1]) in chess.occupied_pos(self.color, self.number):
                            break
                        elif (x, self.pos[1]) in chess.occupied_pos(-self.color):
                            self.check_pos = self.pos
                            self.pos = (x, self.pos[1])
                            self.captured_pos((x, self.pos[1]))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((x, self.pos[1]), True)
                                legal_moves.add((x, self.pos[1]))
                            self.pos = self.check_pos
                            self.captured_pos((x, self.pos[1]), True)
                            break
                        else:
                            self.check_pos = self.pos
                            self.pos = (x, self.pos[1])
                            self.captured_pos((x, self.pos[1]))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((x, self.pos[1]), True)
                                legal_moves.add((x, self.pos[1]))
                            self.pos = self.check_pos
                            self.captured_pos((x, self.pos[1]), True)

                for x in range(self.pos[0] + 1, 8):
                    # Searching for legal moves in horizontally forward direction until a black or white piece comes in the way
                    if trial == True:
                        if (x, self.pos[1]) in chess.occupied_pos(self.color, self.number):
                            legal_moves.add((x, self.pos[1]))
                            break
                        elif (x, self.pos[1]) in chess.occupied_pos(-self.color):
                            legal_moves.add((x, self.pos[1]))
                            break
                        else:
                            legal_moves.add((x, self.pos[1]))
                    else:
                        if (x, self.pos[1]) in chess.occupied_pos(self.color, self.number):
                            break
                        elif (x, self.pos[1]) in chess.occupied_pos(-self.color):
                            self.check_pos = self.pos
                            self.pos = (x, self.pos[1])
                            self.captured_pos((x, self.pos[1]))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((x, self.pos[1]), True)
                                legal_moves.add((x, self.pos[1]))
                            self.pos = self.check_pos
                            self.captured_pos((x, self.pos[1]), True)
                            break
                        else:
                            self.check_pos = self.pos
                            self.pos = (x, self.pos[1])
                            self.captured_pos((x, self.pos[1]))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((x, self.pos[1]), True)
                                legal_moves.add((x, self.pos[1]))
                            self.pos = self.check_pos
                            self.captured_pos((x, self.pos[1]), True)

                for y in range(self.pos[1] - 1, -1, -1):
                    # Searching for legal moves in vertically backward direction until a black or white piece comes in the way
                    if trial == True:
                        if (self.pos[0], y) in chess.occupied_pos(self.color, self.number):
                            legal_moves.add((self.pos[0], y))
                            break
                        elif (self.pos[0], y) in chess.occupied_pos(-self.color):
                            legal_moves.add((self.pos[0], y))
                            break
                        else:
                            legal_moves.add((self.pos[0], y))
                    else:
                        if (self.pos[0], y) in chess.occupied_pos(self.color, self.number):
                            break
                        elif (self.pos[0], y) in chess.occupied_pos(-self.color):
                            self.check_pos = self.pos
                            self.pos = (self.pos[0], y)
                            self.captured_pos((self.pos[0], y))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((self.pos[0], y), True)
                                legal_moves.add((self.pos[0], y))
                            self.pos = self.check_pos
                            self.captured_pos((self.pos[0], y), True)
                            break
                        else:
                            self.check_pos = self.pos
                            self.pos = (self.pos[0], y)
                            self.captured_pos((self.pos[0], y))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((self.pos[0], y), True)
                                legal_moves.add((self.pos[0], y))
                            self.pos = self.check_pos
                            self.captured_pos((self.pos[0], y), True)

                for y in range(self.pos[1] + 1, 8):
                    # Searching for legal moves in vertically forward direction until a black or white piece comes in the way
                    if trial == True:
                        if (self.pos[0], y) in chess.occupied_pos(self.color, self.number):
                            legal_moves.add((self.pos[0], y))
                            break
                        elif (self.pos[0], y) in chess.occupied_pos(-self.color):
                            legal_moves.add((self.pos[0], y))
                            break
                        else:
                            legal_moves.add((self.pos[0], y))
                    else:
                        if (self.pos[0], y) in chess.occupied_pos(self.color, self.number):
                            break
                        elif (self.pos[0], y) in chess.occupied_pos(-self.color):
                            self.check_pos = self.pos
                            self.pos = (self.pos[0], y)
                            self.captured_pos((self.pos[0], y))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((self.pos[0], y), True)
                                legal_moves.add((self.pos[0], y))
                            self.pos = self.check_pos
                            self.captured_pos((self.pos[0], y), True)
                            break
                        else:
                            self.check_pos = self.pos
                            self.pos = (self.pos[0], y)
                            self.captured_pos((self.pos[0], y))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((self.pos[0], y), True)
                                legal_moves.add((self.pos[0], y))
                            self.pos = self.check_pos
                            self.captured_pos((self.pos[0], y), True)

                for x in range(self.pos[0] - 1, -1, -1):
                    for y in range(self.pos[1] - 1, -1, -1):
                        # Searching for legal moves in top left direction diagonally until a piece comes in the way
                        if abs(self.pos[0] - x) == abs(self.pos[1] - y):
                            if trial == True:
                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                else:
                                    legal_moves.add((x, y))
                            else:

                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                                    terminate = True
                                    break
                                else:
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                    if terminate == True:
                        terminate = False
                        break
                for x in range(self.pos[0] - 1, -1, -1):
                    for y in range(self.pos[1] + 1, 8):
                        # Searching for legal moves in top right direction diagonally until a piece comes in the way
                        if abs(self.pos[0] - x) == abs(self.pos[1] - y):
                            if trial == True:
                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                else:
                                    legal_moves.add((x, y))
                            else:

                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                                    terminate = True
                                    break
                                else:
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                    if terminate == True:
                        terminate = False
                        break

                for x in range(self.pos[0] + 1, 8):
                    for y in range(self.pos[1] + 1, 8):
                        # Searching for legal moves in bottom right direction diagonally until a piece comes in the way
                        if abs(self.pos[0] - x) == abs(self.pos[1] - y):
                            if trial == True:
                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                else:
                                    legal_moves.add((x, y))
                            else:

                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                                    terminate = True
                                    break
                                else:
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                    if terminate == True:
                        terminate = False
                        break

                for x in range(self.pos[0] + 1, 8):
                    for y in range(self.pos[1] - 1, -1, -1):
                        # Searching for legal moves in bottom left direction diagonally until a piece comes in the way
                        if abs(self.pos[0] - x) == abs(self.pos[1] - y):
                            if trial == True:
                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                else:
                                    legal_moves.add((x, y))
                            else:

                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                                    terminate = True
                                    break
                                else:
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                    if terminate == True:
                        terminate = False
                        break

            elif self.piece == 2:  # legal move of Rook
                for x in range(self.pos[0] - 1, -1, -1):
                    # Searching for legal moves in horizontally backward direction until a black or white piece comes in the way
                    if trial == True:
                        if (x, self.pos[1]) in chess.occupied_pos(self.color, self.number):
                            legal_moves.add((x, self.pos[1]))
                            break
                        elif (x, self.pos[1]) in chess.occupied_pos(-self.color):
                            legal_moves.add((x, self.pos[1]))
                            break
                        else:
                            legal_moves.add((x, self.pos[1]))
                    else:
                        if (x, self.pos[1]) in chess.occupied_pos(self.color, self.number):
                            break
                        elif (x, self.pos[1]) in chess.occupied_pos(-self.color):
                            self.check_pos = self.pos
                            self.pos = (x, self.pos[1])
                            self.captured_pos((x, self.pos[1]))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((x, self.pos[1]), True)
                                legal_moves.add((x, self.pos[1]))
                            self.pos = self.check_pos
                            self.captured_pos((x, self.pos[1]), True)
                            break
                        else:
                            self.check_pos = self.pos
                            self.pos = (x, self.pos[1])
                            self.captured_pos((x, self.pos[1]))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((x, self.pos[1]), True)
                                legal_moves.add((x, self.pos[1]))
                            self.pos = self.check_pos
                            self.captured_pos((x, self.pos[1]), True)

                for x in range(self.pos[0] + 1, 8):
                    # Searching for legal moves in horizontally forward direction until a black or white piece comes in the way
                    if trial == True:
                        if (x, self.pos[1]) in chess.occupied_pos(self.color, self.number):
                            legal_moves.add((x, self.pos[1]))
                            break
                        elif (x, self.pos[1]) in chess.occupied_pos(-self.color):
                            legal_moves.add((x, self.pos[1]))
                            break
                        else:
                            legal_moves.add((x, self.pos[1]))
                    else:
                        if (x, self.pos[1]) in chess.occupied_pos(self.color, self.number):
                            break
                        elif (x, self.pos[1]) in chess.occupied_pos(-self.color):
                            self.check_pos = self.pos
                            self.pos = (x, self.pos[1])
                            self.captured_pos((x, self.pos[1]))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((x, self.pos[1]), True)
                                legal_moves.add((x, self.pos[1]))
                            self.pos = self.check_pos
                            self.captured_pos((x, self.pos[1]), True)
                            break
                        else:
                            self.check_pos = self.pos
                            self.pos = (x, self.pos[1])
                            self.captured_pos((x, self.pos[1]))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((x, self.pos[1]), True)
                                legal_moves.add((x, self.pos[1]))
                            self.pos = self.check_pos
                            self.captured_pos((x, self.pos[1]), True)

                for y in range(self.pos[1] - 1, -1, -1):
                    # Searching for legal moves in vertically backward direction until a black or white piece comes in the way
                    if trial == True:
                        if (self.pos[0], y) in chess.occupied_pos(self.color, self.number):
                            legal_moves.add((self.pos[0], y))
                            break
                        elif (self.pos[0], y) in chess.occupied_pos(-self.color):
                            legal_moves.add((self.pos[0], y))
                            break
                        else:
                            legal_moves.add((self.pos[0], y))
                    else:
                        if (self.pos[0], y) in chess.occupied_pos(self.color, self.number):
                            break
                        elif (self.pos[0], y) in chess.occupied_pos(-self.color):
                            self.check_pos = self.pos
                            self.pos = (self.pos[0], y)
                            self.captured_pos((self.pos[0], y))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((self.pos[0], y), True)
                                legal_moves.add((self.pos[0], y))
                            self.pos = self.check_pos
                            self.captured_pos((self.pos[0], y), True)
                            break
                        else:
                            self.check_pos = self.pos
                            self.pos = (self.pos[0], y)
                            self.captured_pos((self.pos[0], y))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((self.pos[0], y), True)
                                legal_moves.add((self.pos[0], y))
                            self.pos = self.check_pos
                            self.captured_pos((self.pos[0], y), True)

                for y in range(self.pos[1] + 1, 8):
                    # Searching for legal moves in vertically forward direction until a black or white piece comes in the way
                    if trial == True:
                        if (self.pos[0], y) in chess.occupied_pos(self.color, self.number):
                            legal_moves.add((self.pos[0], y))
                            break
                        elif (self.pos[0], y) in chess.occupied_pos(-self.color):
                            legal_moves.add((self.pos[0], y))
                            break
                        else:
                            legal_moves.add((self.pos[0], y))
                    else:
                        if (self.pos[0], y) in chess.occupied_pos(self.color, self.number):
                            break
                        elif (self.pos[0], y) in chess.occupied_pos(-self.color):
                            self.check_pos = self.pos
                            self.pos = (self.pos[0], y)
                            self.captured_pos((self.pos[0], y))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((self.pos[0], y), True)
                                legal_moves.add((self.pos[0], y))
                            self.pos = self.check_pos
                            self.captured_pos((self.pos[0], y), True)
                            break
                        else:
                            self.check_pos = self.pos
                            self.pos = (self.pos[0], y)
                            self.captured_pos((self.pos[0], y))
                            if chess.check(self.color) == False:
                                self.pos = self.check_pos
                                self.captured_pos((self.pos[0], y), True)
                                legal_moves.add((self.pos[0], y))
                            self.pos = self.check_pos
                            self.captured_pos((self.pos[0], y), True)

            elif self.piece == 3:  # legal move of Bishop
                for x in range(self.pos[0] - 1, -1, -1):
                    for y in range(self.pos[1] - 1, -1, -1):
                        # Searching for legal moves in top left direction diagonally until a piece comes in the way
                        if abs(self.pos[0] - x) == abs(self.pos[1] - y):
                            if trial == True:
                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                else:
                                    legal_moves.add((x, y))
                            else:

                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                                    terminate = True
                                    break
                                else:
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                    if terminate == True:
                        terminate = False
                        break
                for x in range(self.pos[0] - 1, -1, -1):
                    for y in range(self.pos[1] + 1, 8):
                        # Searching for legal moves in top right direction diagonally until a piece comes in the way
                        if abs(self.pos[0] - x) == abs(self.pos[1] - y):
                            if trial == True:
                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                else:
                                    legal_moves.add((x, y))
                            else:

                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                                    terminate = True
                                    break
                                else:
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                    if terminate == True:
                        terminate = False
                        break

                for x in range(self.pos[0] + 1, 8):
                    for y in range(self.pos[1] + 1, 8):
                        # Searching for legal moves in bottom right direction diagonally until a piece comes in the way
                        if abs(self.pos[0] - x) == abs(self.pos[1] - y):
                            if trial == True:
                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                else:
                                    legal_moves.add((x, y))
                            else:

                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                                    terminate = True
                                    break
                                else:
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                    if terminate == True:
                        terminate = False
                        break

                for x in range(self.pos[0] + 1, 8):
                    for y in range(self.pos[1] - 1, -1, -1):
                        # Searching for legal moves in bottom left direction diagonally until a piece comes in the way
                        if abs(self.pos[0] - x) == abs(self.pos[1] - y):
                            if trial == True:
                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    legal_moves.add((x, y))
                                    terminate = True
                                    break
                                else:
                                    legal_moves.add((x, y))
                            else:

                                if (x, y) in chess.occupied_pos(self.color, self.number):
                                    terminate = True
                                    break
                                elif (x, y) in chess.occupied_pos(-self.color):
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                                    terminate = True
                                    break
                                else:
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos
                    if terminate == True:
                        terminate = False
                        break

            elif self.piece == 4:  # legal move of Knight
                for x in range(8):
                    for y in range(8):
                        if abs(self.pos[0] - x) in [1, 2] and abs(self.pos[1] - y) in [1, 2]:
                            # logic for finding legal move for Knight
                            if abs(self.pos[0] - x) != abs(self.pos[1] - y):
                                # exception of logic
                                if trial == True:
                                    legal_moves.add((x, y))
                                else:
                                    self.check_pos = self.pos
                                    self.pos = (x, y)
                                    self.captured_pos((x, y))
                                    if chess.check(self.color) == False:
                                        self.pos = self.check_pos
                                        self.captured_pos((x, y), True)
                                        if (x, y) not in chess.occupied_pos(self.color, self.number):
                                            legal_moves.add((x, y))
                                    self.captured_pos((x, y), True)
                                    self.pos = self.check_pos

            elif self.piece == 5:  # legal move of Pawn
                if trial == True:
                    legal_moves.add(
                        (self.pos[0]+1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1])))))
                    legal_moves.add(
                        (self.pos[0]-1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1])))))
                else:
                    self.check_pos = self.pos
                    self.pos = (
                        self.pos[0]-1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1]))))
                    self.captured_pos(tuple(self.pos))
                    if chess.check(self.color) == False:
                        if self.pos in chess.occupied_pos(-self.color):
                            self.captured_pos(tuple(self.pos), True)
                            self.pos = self.check_pos
                            legal_moves.add(
                                (self.pos[0]-1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1])))))
                    self.pos = self.check_pos
                    self.captured_pos(tuple(self.pos), True)

                    self.check_pos = self.pos
                    self.pos = (
                        self.pos[0]+1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1]))))
                    self.captured_pos(tuple(self.pos))
                    if chess.check(self.color) == False:
                        if self.pos in chess.occupied_pos(-self.color):
                            self.captured_pos(tuple(self.pos), True)
                            self.pos = self.check_pos
                            legal_moves.add(
                                (self.pos[0]+1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1])))))
                    self.pos = self.check_pos
                    self.captured_pos(tuple(self.pos), True)

                    self.check_pos = self.pos
                    self.pos = (
                        self.pos[0], self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1]))))
                    if chess.check(self.color) == False:
                        if self.pos not in chess.occupied_pos(0, self.number):
                            legal_moves.add(self.pos)
                            self.pos = self.check_pos
                        self.pos = self.check_pos
                    self.pos = self.check_pos

                    self.check_pos = self.pos
                    self.pos = (
                        self.pos[0], self.pos[1]+int((4-self.init_pos[1])*2/(abs(4-self.init_pos[1]))))
                    if chess.check(self.color) == False:
                        if (self.pos not in chess.occupied_pos(-self.color)) and (self.pos not in chess.occupied_pos(self.color, self.number)) and self.moves == 0:
                            if ((self.check_pos[0], self.check_pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1])))) not in chess.occupied_pos(-self.color)) and ((self.check_pos[0], self.check_pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1])))) not in chess.occupied_pos(self.color, self.number)):
                                legal_moves.add(self.pos)
                                self.pos = self.check_pos
                            self.pos = self.check_pos
                        self.pos = self.check_pos
                    self.pos = self.check_pos

                    if len(chess.Moves) > 0:
                        if (self.pos[0]+1, self.pos[1]) in chess.occupied_pos(-self.color, self.number):
                            otherPiece = chess.obj_from_pos(
                                (self.pos[0]+1, self.pos[1]))
                            if otherPiece.piece == 5 and otherPiece.color == -self.color:
                                if (self.pos[0]+1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1])))) not in chess.occupied_pos(0, self.number):
                                    if otherPiece.captures == 0 and self.captures == 0 and otherPiece.moves == 1 and self.moves == 2:
                                        if chess.Moves[-1] == [otherPiece.number, otherPiece.init_pos, otherPiece.pos]:
                                            self.check_pos = self.pos
                                            self.pos = (
                                                self.pos[0]+1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1]))))
                                            otherPiece.capture = True
                                            if chess.check(self.color) == False:
                                                self.pos = self.check_pos
                                                legal_moves.add(
                                                    (self.pos[0]+1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1])))))
                                                self.en_passant = [otherPiece.number, (self.pos[0]+1, self.pos[1]+int(
                                                    (4-self.init_pos[1])/(abs(4-self.init_pos[1]))))]
                                            otherPiece.capture = False
                        if (self.pos[0]-1, self.pos[1]) in chess.occupied_pos(-self.color, self.number):
                            otherPiece = chess.obj_from_pos(
                                (self.pos[0]-1, self.pos[1]))
                            if otherPiece.piece == 5 and otherPiece.color == -self.color:
                                if (self.pos[0]-1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1])))) not in chess.occupied_pos(0, self.number):
                                    if otherPiece.captures == 0 and self.captures == 0 and otherPiece.moves == 1 and self.moves == 2:
                                        if chess.Moves[-1] == [otherPiece.number, otherPiece.init_pos, otherPiece.pos]:
                                            self.check_pos = self.pos
                                            self.pos = (
                                                self.pos[0]-1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1]))))
                                            otherPiece.capture = True
                                            if chess.check(self.color) == False:
                                                self.pos = self.check_pos
                                                legal_moves.add(
                                                    (self.pos[0]-1, self.pos[1]+int((4-self.init_pos[1])/(abs(4-self.init_pos[1])))))
                                                self.en_passant = [otherPiece.number, (self.pos[0]-1, self.pos[1]+int(
                                                    (4-self.init_pos[1])/(abs(4-self.init_pos[1]))))]
                                            otherPiece.capture = False

            else:
                return False

        if type == True:  # checks if the value of type is True
            # return true if the given position is a legal move else return false
            return (position in legal_moves)
        else:
            # return the set of legal moves
            return legal_moves
