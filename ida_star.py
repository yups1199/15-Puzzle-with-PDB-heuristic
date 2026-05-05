import copy
import manage_pdb
# from model import Puzzle
INF = float("inf")
OPPOSITE = {0:2, 1:3, 2:0, 3:1}

# 6-6-3 PDB
DEFAULT_PATTERN_SET = ((1, 2, 5, 6, 9, 13),(3, 4, 7, 8, 11, 12),(10, 14, 15))
# 5-5-5 : ((1,2,4,5,6), (3,7,8,10,11), (9,12,13,14,15))

def ida_star(_pz, pattern_set = DEFAULT_PATTERN_SET) -> tuple :
    pz = copy.deepcopy(_pz)

    # load pdb (build if necessary)
    pdb = manage_pdb.PDB(pattern_set)
    if not pdb.check_file() :
        if not pdb.build() :
            raise RuntimeError("PDB build fail")
    if not pdb.load() :
        raise RuntimeError("PDB load fail")

    # initialize global bound
    bound = pdb.heuristic(pz.board)

    res = None
    while not res :
        min_est = INF # estimated minimum
        for dir in pz.get_moveable_dir() :
            branch = ida_branch(pdb, pz.make_moved(dir), dir, bound, 1)
            if type(branch) == list : # path found
                branch.append(dir)
                res = branch
                break
            if branch < min_est : min_est = branch
        bound = min_est
    return tuple(reversed(res))

def ida_branch(pdb, pz, prev_dir, bound, depth) :
    if pz.is_goal() : return list()

    f = pdb.heuristic(pz.board) + depth
    if f > bound : return f

    min_est = INF
    for dir in pz.get_moveable_dir() :
        if dir == OPPOSITE[prev_dir] : continue
        branch = ida_branch(pdb, pz.make_moved(dir), dir, bound, depth+1)
        if type(branch) == list : # path found
            branch.append(dir)
            return branch
        if branch < min_est : min_est = branch
    
    return min_est