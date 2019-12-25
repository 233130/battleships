class Field:
    def __init__(self):
        self.symbol = "?"
        self.can_hit = False
        self.can_

    def print_symbol(self):
        print(self.symbol, "", end='')


class EmptyField(Field):
    def __init__(self):
        super().__init__()
        self.symbol = "."
        self.can_hit = True


class HitField(Field):
    def __init__(self):
        super().__init__()
        self.symbol = "X"
        self.can_hit = False


class MishitField(Field):
    def __init__(self):
        super().__init__()
        self.symbol = "O"
        self.can_hit = False


class ShipField(Field):
    def __init__(self, size):
        super().__init__()
        self.symbol = size
        self.can_hit = True


class Ship:
    def __init__(self, id, size):
        self.fields = []
        self.size = size
        self.id = id

    def set_ship_on_board(self, board):
        print("Dodajesz ", self.id, "statek o rozmiarze ", self.size)
        problem = True
        while problem:
            x = int(input("Podaj wartość początkową wartość X: "))
            y = int(input("Podaj wartość początkową wartość Y: "))
            orientation = int(input("poziomo czy pionowo 0/1: "))
            problem = False
            for i in range(self.size):
                try:
                    if orientation:
                        field = board[y + i][x]
                    else:
                        field = board[y][x + i]
                    print(field.__class__.__name__)
                        # problem = True
                        # print("Niestety nie mogę dodać tutaj statku")
                        # break
                except IndexError:
                    problem = True
                    print("Wyszedłeś po za tablicę")
                    break

        for i in range(self.size):
            if orientation:
                board[y + i][x] = str(self.size)
            else:
                board[y][x + i] = str(self.size)


class Board:
    def __init__(self, width, high):
        self.width = width
        self.high = high
        self.board = []
        for row in range(self.high):
            self.board.append(EmptyField() for i in range(self.width))

    def print_board(self):
        for row in self.board:
            for field in row:
                field.print_symbol()
            print("")


tablica = Board(8, 6)
tablica.print_board()
statek = Ship(1,5)
statek.set_ship_on_board(tablica)