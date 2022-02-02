from enum import Enum

class Figure(Enum):
    WHITE_PIECE = 'w'
    BLACK_PIECE = 'b'
    WHITE_KING = 'W'
    BLACK_KING = 'B'
    

class CheckersPiece:
    def __init__(self, id: str, row: int, col: int):
        self.id = id
        self.row = row
        self.col = col
        self.king = False    
        self.turn = True if self.id == Figure.WHITE_PIECE else False

    # def make_king(self):
    #     self.king == True
    #     self.id = Figure.WHITE_KING if self.id == Figure.WHITE_PIECE else Figure.BLACK_KING
    #     return None

    def __hash__(self):
        return hash(self.__str__())

    def __str__(self) -> str:
        return "Piece: {}, {}, {}".format(self.id, self.row, self.col)