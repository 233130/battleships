# Abstrakcyjna klasa Pole. Po niej dziedziczą kolejne klasy pól
class Field:
    def __init__(self):
        self.symbol = "?"
        self.can_hit = False
        self.can_put_ship = False

    # Metoda odpowiedzialna za rysowanie symbolu
    def print_symbol(self):
        print(self.symbol, "", end='')

    # Metoda odpowiedzialna za rysowanie pustego symbolu gdy nie chcemy widzieć gdzie są umieszczone statki
    def print_empty_symbol(self):
        print(". ", end='')

    # Metoda wywoływania, gdy dane pole zostało uderzone. Będzie zwracać obiekt klasy w który dane pole się przekształci
    def field_hitted(self):
        pass


# Klasa odpowiedzialna za puste pole
class EmptyField(Field):
    def __init__(self):
        super().__init__()
        self.symbol = "."
        self.can_hit = True
        self.can_put_ship = True

    def field_hitted(self):
        return MishitField()


# Klasa odpowiedzialna za pole trafione
class HitField(Field):
    def __init__(self):
        super().__init__()
        self.symbol = "X"
        self.can_hit = False
        self.can_put_ship = False

    def print_empty_symbol(self):
        self.print_symbol()


# Klasa odpowiedzialna za strzelone pole, ale nie trafione
class MishitField(Field):
    def __init__(self):
        super().__init__()
        self.symbol = "O"
        self.can_hit = False
        self.can_put_ship = False

    def print_empty_symbol(self):
        self.print_symbol()


# Klasa odpowiedzialna za pole na którym jest fragment statku
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


# Klasa odpowiedzialna za statek. Posiada zapisane pola ShipField
class Ship:
    def __init__(self, id, size):
        self.fields = []
        self.size = size
        self.id = id

    # Metoda przyjmująca tablicę i umieszczająca statek na niej
    def set_ship_on_board(self, board):
        print("Dodajesz statek o rozmiarze: ", self.size)
        problem = True
        while problem:
            x = int(input("Podaj wartość początkową wartość X: "))
            y = int(input("Podaj wartość początkową wartość Y: "))
            orientation = int(input("poziomo czy pionowo 0/1: "))
            problem = False
            for i in range(self.size):
                if orientation:
                    if x > (board.width - 1) or (y + i) > (board.high - 1):
                        print("Wyszedłeś po za tablicę")
                        problem = True
                        continue
                    else:
                        field = board.get_obj(x, y + i)
                else:
                    if (x + i) > (board.width - 1) or y > (board.high - 1):
                        print("Wyszedłeś po za tablicę")
                        problem = True
                        continue
                    else:
                        field = board.get_obj(x + i, y)
                if not field.can_put_ship:
                    print("Pole zajęte")
                    problem = True
        for i in range(self.size):
            mast = ShipField(i, self.id, self.size)
            if orientation:
                board.change_field(x, y + i, mast)
            else:
                board.change_field(x + i, y, mast)
            self.fields.append(mast)

    # Metoda odpowiedzialna za trafienie pola statku. Zwraca wartość True gdy statek został w całości zatopiony
    def ship_hitted(self, new_field):
        self.fields.remove(new_field)
        if not self.fields:
            print("Trafiony, zatopiony")
            return True
        else:
            return False


# Klasa odpowiedzialna za tablicę
class Board:
    def __init__(self, width, high):
        self.width = width
        self.high = high
        self.board = [[EmptyField() for row in range(self.width)] for i in range(self.high)]
        self.ships = {}
        self.board[1][2] = MishitField()

    # Metoda odpowiedzialna za rysowanie tablicy
    def print_board(self):
        for row in self.board:
            for field in row:
                field.print_symbol()
            print("")
        print("")

    # Metoda odpowiedzialna za rysowanie tablicy bez statków
    def print_empty_board(self):
        for row in self.board:
            for field in row:
                field.print_empty_symbol()
            print("")

    # Metoda zwracająca obiekt leżący w danym miejscu x, y
    def get_obj(self, x, y):
        return self.board[y][x]

    # Metoda odpowiedzialna za obiektu pola na danym miejscu x, y
    def change_field(self, x, y, field):
        self.board[y][x] = field

    # Metoda odpowiedzialna za uderzenie pola w miejscu x, y. Gdy wszystie statki są zbite to zwraca wartość False oznaczającą koniec gry
    def board_hit(self, x, y):
        if x > (self.width - 1) or y > (self.high - 1):
            print("Wyszedłeś po za tablicę")
        else:
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
                            return False
            else:
                print("Nie możesz uderzyć w dane pole")
        return True


# Klasa odpowiedzialna za grę. Tworzy tablicę i dodaje na niej statki
class Game:
    def __init__(self):
        width = int(input("Podaj szerokość tablicy: "))
        high = int(input("Podaj wysokość tablicy: "))
        self.board = Board(width, high)
        ships_count = int(input("Ile chcesz statków: "))
        for i in range(ships_count):
            size = int(input("Podaj wielkość statku: "))
            ship = Ship(i, size)
            ship.set_ship_on_board(self.board)
            self.board.ships[i] = ship
            self.board.print_board()

    # Metoda odpowiedzialna za uderzenia tablicy. Pętla nieskończona działająca dopóki wszystkie statki pływają
    def game(self):
        the_end = True
        while the_end:
            x = int(input("Podaj wartość X: "))
            y = int(input("Podaj wartość Y: "))
            the_end = self.board.board_hit(x, y)
            self.board.print_board()


gra = Game()
gra.game()
