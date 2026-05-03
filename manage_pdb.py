import math
from collections import deque
from pathlib import Path
PDB_FILENAME = "pattern_database.bin"

class RankSetup:
    def __init__(self, tile_sets, pzsize=16) : # tile_sets = tuple(set, set)
        self.tile_sets = [set(tset) | {0} for tset in tile_sets]
        tile_sets_len = len(tile_sets)
        self.pzsize = pzsize

        # make base ranks
        self.tset_rank = [0] # base rank
        self.tset_nb_rank = [0] # base rank (of no blanks)
        for i, tset in enumerate(self.tile_sets) :
            if i < tile_sets_len - 1 : 
                self.tset_rank.append(self.max_ranks_in(tset) + self.tset_rank[i])
                self.tset_nb_rank.append(self.max_ranks_in(tset, True) + self.tset_nb_rank[i])
            elif i == tile_sets_len - 1 :
                self.data_size = self.tset_rank[i] + self.max_ranks_in(tset)
                self.idx_size = self.tset_nb_rank[i] + self.max_ranks_in(tset, True)

        # make dictionaries of index for tiles in tile_sets
        self.tile_set_order = list() # list of dicts
        for tset in self.tile_sets : 
            tiles = sorted(t for t in tset if t != 0)
            self.tile_set_order.append({tile:i for i, tile in enumerate(tiles)})

    def max_ranks_in(self, tile_set, no_blanks = False) -> int:
        tsize = len(tile_set)
        if no_blanks : tsize -= 1
        return math.comb(self.pzsize, tsize) * math.factorial(tsize)
    
    def comb_rank(self, p_pos, pos_len) -> int:
        pos_list = [-1] + sorted(p_pos)
        c_rank = 0
        for idx, pos in enumerate(pos_list[1:], start = 1) : # idx start at 1
            for at in range(pos_list[idx-1]+1, pos) :
                c_rank += math.comb(self.pzsize - at - 1, pos_len - idx)
        # print("comb rank : ", c_rank)
        return c_rank

    def perm_rank(self, p_pos, l) -> int:
        p_sort = sorted((p, i) for i, p in enumerate(p_pos))
        p_perm = [i[1] for i in p_sort]

        elements = sorted(p_perm)
        p_rank = 0
        for i, v in enumerate(p_perm) :
            idx = elements.index(v)
            p_rank += idx * math.factorial(l - i - 1)
            elements.pop(idx)
        # print("perm rank : ", p_rank)
        return p_rank

    def rank_pattern(self, p_pos, set_num, no_blank = False) -> int: # p_pos = tuple(blank_pos, t1pos, t2pos t3pos...)
        l = len(p_pos)
        if no_blank : rank = self.tset_nb_rank[set_num] # set base rank (for no blank)
        else : rank = self.tset_rank[set_num] # set base rank

        rank += self.comb_rank(p_pos, l) * math.factorial(l)
        rank += self.perm_rank(p_pos, l)
        return rank
    
    def full_rank_pattern(self, set_num, pboard, zero) -> int:
        tile_order = self.tile_set_order[set_num]
        p_pos = [0] * len(self.tile_sets[set_num])
        p_pos[0] = zero
        for i, v in enumerate(pboard) :
            if v in tile_order : p_pos[tile_order[v] + 1] = i
        return self.rank_pattern(p_pos, set_num)
    
    def idx_rank_pattern(self, set_num, pboard) -> int:
        tile_order = self.tile_set_order[set_num]
        p_pos = [0] * (len(self.tile_sets[set_num]) - 1)
        for i, v in enumerate(pboard) :
            if v in tile_order : p_pos[tile_order[v]] = i
        return self.rank_pattern(p_pos, set_num, no_blank=True)
    
    def check_visit(self, set_num, pboard, zero) -> int:
        return self.full_rank_pattern(set_num, pboard, zero) - self.tset_rank[set_num]
    
    def get_visited_size(self, set_num) -> int:
        if set_num == len(self.tile_sets) - 1 : res = self.data_size
        else : res = self.tset_rank[set_num + 1]
        res -= self.tset_rank[set_num]
        return res

    def get_idx(self, board) -> tuple :
        res = list()
        for set_num, set in enumerate(self.tile_sets) :
            res.append(self.idx_rank_pattern(set_num, board))
        return tuple(res)

class PDB :
    NOT_VIST = 255

    def __init__(self, pattern_sets, pzsize=16) : 
        self.pzsize = pzsize

        # make tile_sets
        ts = list()
        for tset in pattern_sets : ts.append(set(tset))
        self.tile_sets = tuple(ts)

        # make tile_tuples
        self.tile_tuples = tuple(sorted(tset) for tset in pattern_sets)

        # make ranker
        self.ranker = RankSetup(self.tile_sets, self.pzsize)
        self.data_size = self.ranker.data_size
        self.idx_size = self.ranker.idx_size
        
    def build(self) : # for 4*4 board
        data_path = Path(PDB_FILENAME)
        if data_path.exists() :
            print("data file existent")
            return False
        print("building data file....")

        data = bytearray([self.NOT_VIST]) * self.idx_size
        dy, dx = (0, 1, 0, -1), (1, 0, -1, 0)
        
        for set_num, tiles in enumerate(self.tile_tuples) : # Build database for each pattern
            
            #make init_board
            init_board = [0] * 16
            for tile in tiles : init_board[tile-1] = tile

            # initialize q
            q = deque() # (board, zero_pos)
            q.append((init_board, 15))

            # make depth[]
            depth = bytearray([self.NOT_VIST]) * self.ranker.get_visited_size(set_num)

            # initialize depth, data
            depth[self.ranker.check_visit(set_num, init_board, 15)] = 0
            data[self.ranker.idx_rank_pattern(set_num, init_board)] = 0
            

            while(q) :
                board, zero = q.popleft()
                zy, zx = zero // 4, zero % 4

                cur_depth_idx = self.ranker.check_visit(set_num, board, zero)
                cur_depth = depth[cur_depth_idx]

                for dir in range(4) :
                    ny, nx = zy + dy[dir], zx + dx[dir]
                    if ny < 0 or ny >= 4 or nx < 0 or nx >= 4 : continue

                    new_zero = 4 * ny + nx
                    new_board = board.copy()

                    cost = 0
                    if board[new_zero] != 0 : 
                        cost = 1
                        new_board[zero], new_board[new_zero] = new_board[new_zero], new_board[zero]

                    new_depth = cur_depth + cost
                    next_depth_idx = self.ranker.check_visit(set_num, new_board, new_zero)
            
                    if new_depth < depth[next_depth_idx] :
                        depth[next_depth_idx] = new_depth
                        data_idx = self.ranker.idx_rank_pattern(set_num, new_board)
                        if new_depth < data[data_idx] : data[data_idx] = new_depth
                        if cost == 0 : q.appendleft((new_board, new_zero))
                        else : q.append((new_board, new_zero))
        
        with open(data_path, "wb") as f:
            f.write(data)
        self.data = data
        print("data file build and load complete")
        return True
    # end pdb build

    def load(self) :
        data_path = Path(PDB_FILENAME)

        if not data_path.exists() :
            print("pdb build required")
            return False
        
        print("pdb loading...")
        with open(data_path, "rb") as f:
            self.data = bytearray(f.read())
        print("pdb load complete")

        return True
    
    def check_file(self) -> bool:
        data_path = Path(PDB_FILENAME)
        return data_path.exists()

    # final heuristic
    def heuristic(self, board) : 
        pdb_idx = self.ranker.get_idx(board)
        res = 0
        for i in pdb_idx :
            res += self.data[i]
        return res