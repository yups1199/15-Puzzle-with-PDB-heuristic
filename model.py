from random import shuffle, sample

class Puzzle :

    def __init__(self, board = tuple(list(range(1,16)) + [0]), zero = -1, size = 4) :
        self.size = size
        self.board = tuple(board)
        if zero == -1 : self.zero = self.board.index(0)
        else : self.zero = zero
        self.movable_tiles = self.find_movables()

    def find_movables(self) :
        dy, dx = (0, 1, 0, -1), (1, 0, -1, 0)
        zpos = self.index_to_pos(self.zero)
        res = dict()
        for i in range(4) :
            ny, nx = zpos
            ny += dy[i]
            nx += dx[i]
            if ny < 0 or ny >= self.size or nx < 0 or nx >= self.size : continue
            res[self.pos_to_index(ny, nx)] = i
        return res

    def movable_dir(self, pos) :
        if pos in self.movable_tiles.keys() :
            return self.movable_tiles[pos]
        else : return None

    def get_moveable_dir(self) :
        return self.movable_tiles.values()

    def is_goal(self) -> bool :
        if self.size == 4 :
            GOAL = (1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0)
            return self.board == GOAL
    
    def index_to_pos(self, index) :
        return (index // self.size, index % self.size)

    def pos_to_index(self, y, x) -> int :
        return self.size * y + x
    
    def get_v_at(self, pos) -> int :
        return self.board[pos]

    def make_moved(self, dir) : # -> Puzzle 
        dy, dx = (0, 1, 0, -1), (1, 0, -1, 0) # dir 0,1,2,3
        ny, nx = self.zero // self.size + dy[dir], self.zero % self.size + dx[dir]
        if ny < 0 or ny >= self.size or nx < 0 or nx >= self.size :
            return None
        new_zero = self.pos_to_index(ny, nx)
        new_board = list(self.board)
        new_board[self.zero], new_board[new_zero] = new_board[new_zero], new_board[self.zero]
        return Puzzle(new_board, new_zero)
    
    def is_solvable(self) -> bool :
        # count inversions
        inv = 0
        for i in range(self.size**2) :
            if self.board[i] == 0 : continue
            for j in range(i+1, self.size**2) :
                if self.board[j] == 0 : continue
                if self.board[i] > self.board[j] : inv += 1
        # apply zero's row(counted from top)
        inv += (self.zero // self.size) # only works on 4*4
        return inv % 2 == 1
    
    def shuffle_board(self) :
        board = list(self.board)
        shuffle(board)
        self.board = tuple(board)
        self.zero = self.board.index(0)

        if not self.is_solvable() :
            non_zero_indexs = [i for i, v in enumerate(self.board) if v != 0]
            i, j = sample(non_zero_indexs, 2)

            board = list(self.board)
            board[i], board[j] = board[j], board[i]
            self.board = tuple(board)
            self.zero = self.board.index(0)

        self.movable_tiles = self.find_movables()
        return

    def __eq__(self, other) :
        return isinstance(other, Puzzle) and self.board == other.board