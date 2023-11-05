from random import randint
from copy import deepcopy


class Game:
    def __init__(self):
        self.field = [[None] * 5 for i in range(5)]
        self.turn = 0
        self.bag = set([(i, j) for i in range(1, 5) for j in range(1, 14)])
        self.cur_num = None
    
    def get_next_num(self):
        assert not self.cur_num
        now = self.bag.pop()
        self.cur_num = now[1]
        return self.cur_num
    
    def make_turn(self, r, c):
        assert not self.field[r][c] and self.cur_num
        self.field[r][c] = self.cur_num
        self.cur_num = None

    @staticmethod
    def row_score(row: list):
        row = deepcopy(row)
        row.sort()
        if tuple(row[:4]) == (1, 1, 1, 1):
            return 200
        if tuple(row) == (1, 10, 11, 12, 13):
            return 150
        if tuple(row) == (1, 1, 1, 13, 13):
            return 100
        for i in (0, 4):
            if row.count(row[i]) == 4:
                return 160
        if tuple([x - row[0] for x in row]) == tuple([0, 1, 2, 3, 4]):
            return 50
        for k1, k2 in [(0, -1), (-1, 0)]:
            if row.count(row[k1]) == 2 and row.count(row[k2]) == 3:
                return 80
        for i in range(3):
            if row.count(row[i]) == 3:
                return 40
        cnt = sum([10 * int(row[i] == row[i+1]) for i in range(4)])
        return cnt

    def string_field(self):  
        def num2str(num, border=True):
            if num is None:
                out = "-"
            else:
                out = str(num)
            res = " " * (4 - len(out)) + out
            if border:
                return res + "|"
            else:
                return res + " "
        border_str = " " * 6 + "-" * (5 * 5 - 1)
        res = border_str + chr(10)
        for i in range(5):
            if self.field[i].count(None) == 0:
                begin = " " + num2str(self.row_score(self.field[i]))
            else:
                begin = " " + num2str(None)
            res += begin + "".join([num2str(self.field[i][j]) for j in range(5)]) 
            res += chr(10) + border_str + chr(10)
        diag1 = [self.field[i][4-i] for i in range(5)]
        diag2 = [self.field[i][i] for i in range(5)]
        if diag1.count(None) == 0:
            num = self.row_score(diag1)
            if num:
                num += 10
            res += " " + num2str(num, False)
        else:
            res += " " + num2str(None, False)
        for i in range(5):
            mas = [self.field[j][i] for j in range(5)]
            if mas.count(None) == 0:
                res += num2str(self.row_score(mas), False)
            else:
                res += num2str(None, False)
        if diag2.count(None) == 0:
            num = self.row_score(diag2)
            if num:
                num += 10
            res += num2str(num, False)
        else:
            begin += num2str(None, False)
        return res
    
    def print_field(self):
        fld = self.string_field()
        for s in fld.split(chr(10)):
            print(s)

    def score(self):
        for i in range(5):
            if None in self.field[i]:
                raise Exception("not a complete field")
        res = 0
        for i in range(5):
            res += self.row_score(self.field[i])
        for i in range(5):
            res += self.row_score([self.field[j][i] for j in range(5)])
        diag1 = [self.field[i][4-i] for i in range(5)]
        diag2 = [self.field[i][i] for i in range(5)]
        for diag in (diag1, diag2):
            num = self.row_score(diag)
            if num:
                num += 10
            res += num
        return res
    
        