class Field:
    def __init__(self):
        self.symbol = "?"
        self.can_hit = False
        self.can_put_ship = False

    def print_symbol(self):
        print(self.symbol, "", end='')

    def print_empty_symbol(self):
        print(". ", end='')

    def field_hitted(self):
        pass


class EmptyField(Field):
    def __init__(self):
        super().__init__()
        self.symbol = "."
        self.can_hit = True
        self.can_put_ship = True

    def field_hitted(self):
        return MishitField()


class HitField(Field):
    def __init__(self):
        super().__init__()
        self.symbol = "X"
        self.can_hit = False
        self.can_put_ship = False

    def print_empty_symbol(self):
        self.print_symbol()


class MishitField(Field):
    def __init__(self):
        super().__init__()
        self.symbol = "O"
        self.can_hit = False
        self.can_put_ship = False

    def print_empty_symbol(self):
        self.print_symbol()


class ShipField(Field):
    def __init__(self, id, ship_id, size):
        super().__init__()
        self.symbol = size
        self.can_hit = True
        self.can_put_ship = False
        self.id = id
        self.ship_id = ship_id

    def field_hitted(self):
        return HitField()


class Ship:
    def __init__(self, id, size):
        self.fields = []
        self.size = size
        self.id = id

    def set_ship_on_board(self, board):
        print("Dodajesz statek o rozmiarze: ", self.size)
        problem = True
        while problem:
            x = int(input("Podaj wartość początkową wartość X: "))
            y = int(input("Podaj wartość początkową wartość Y: "))
            orientation = int(input("poziomo czy pionowo 0/1: "))
            problem = False
            if x > (board.width - 1) or y > (board.high - 1):
                print("Wyszedłeś po za tablicę")
                problem = True
                continue
            for i in range(self.size):
                if orientation:
                    field = board.get_obj(x, y + i)
                else:
                    field = board.get_obj(x + i, y)

                if not field.can_put_ship:
                    print("Pole zajęte")
                    problem = True
                    break
        for i in range(self.size):
            mast = ShipField(i, self.id, self.size)
            if orientation:
                board.change_field(x, y + i, mast)
            else:
                board.change_field(x + i, y, mast)
            self.fields.append(mast)

    def ship_hitted(self, new_field):
        self.fields.remove(new_field)
        if not self.fields:
            print("Trafiony, zatopiony")
            return True
        else:
            return False


class Board:
    def __init__(self, width, high):
        self.width = width
        self.high = high
        self.board = [[EmptyField() for row in range(self.width)] for i in range(self.high)]
        self.ships = {}
        self.board[1][2] = MishitField()

    def print_board(self):
        for row in self.board:
            for field in row:
                field.print_symbol()
            print("")
        print("")

    def print_empty_board(self):
        for row in self.board:
            for field in row:
                field.print_empty_symbol()
            print("")

    def get_obj(self, x, y):
        return self.board[y][x]

    def change_field(self, x, y, field):
        self.board[y][x] = field

    def board_hit(self, x, y):
        field = self.get_obj(x, y)
        if field.can_hit:
            new_field = field.field_hitted()
            self.change_field(x, y, new_field)
            if not field.can_put_ship:
                hitted_ship = self.ships[field.ship_id]
                if hitted_ship.ship_hitted(field):
                    del self.ships[field.ship_id]
                    if not self.ships:
                        print("Koniec gry. Zatopiono wszystkie statki")

        else:
            print("Nie możesz uderzyć w dane pole")


tablica = Board(8, 6)
tablica.print_board()
for i in range(2):
    rozmiar = int(input("Podaj wielkość statku: "))
    statek = Ship(i, rozmiar)
    statek.set_ship_on_board(tablica)
    tablica.ships[i] = statek
    tablica.print_board()
for i in range(5):
    x = int(input("Podaj wartość X: "))
    y = int(input("Podaj wartość Y: "))
    tablica.board_hit(x, y)
    tablica.print_board()
