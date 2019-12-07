class Board:

    def __init__(self, width, high):
        self.width = width
        self.high = high
        self.board = []
        for row in range(high):
            self.board.append(["."] * self.width)

    def print_board(self):
        for row in self.board:
            print((" ").join(row))
        print("\n")

    def print_blank_board(self):
        for row in self.board:
            print((" ").join(row))
        print("\n")


class Ship:

    def __init__(self, size):
        self.size = size

    def put_ship_on_board(self, board):
        print("Dodajesz statek o rozmiarze: ", self.size)
        problem = True
        while problem:
            x = int(input("Podaj wartość początkową wartość X: "))
            y = int(input("Podaj wartość początkową wartość Y: "))
            orientation = int(input("poziomo czy pionowo 0/1: "))
            problem = False
            for i in range(self.size):
                try:
                    if orientation:
                        character = board[y + i][x]
                    else:
                        character = board[y][x + i]
                    if character != ".":
                        problem = True
                        print("Niestety nie mogę dodać tutaj statku")
                        break
                except IndexError:
                    problem = True
                    print("Wyszedłeś po za tablicę")
                    break

        for i in range(self.size):
            if orientation:
                board[y + i][x] = str(self.size)
            else:
                board[y][x + i] = str(self.size)


tablica = Board(8, 6)
tablica.print_board()
statek = Ship(2)
for i in range(5):
    statek.put_ship_on_board(tablica.board)
    tablica.print_board()
