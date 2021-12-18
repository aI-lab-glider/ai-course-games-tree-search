class CheckersPiece:
    def __init__(self, id: str, row: int, col: int):
        self.id = id
        self.row = row
        self.col = col
        self.king = False
        
        self.turn = True if self.id == 'w' else False

        if self.king == True:
            self.id = self.id.capitalize()

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self) -> str:
        return "Piece: {}, {}, {}".format(self.id, self.row, self.col)