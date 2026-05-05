import pygame
import gui
from model import Puzzle
import ida_star as ida

# PDB PATTERN SET
# 패턴셋을 바꾸려면 기존 PDB 파일 삭제 후 다시 build할 것
PATTERN_SET = ((1, 2, 5, 6, 9, 13),(3, 4, 7, 8, 11, 12),(10, 14, 15))

# base setting
Version = "1.0"
BOARD_SIZE = 4

# GUI setting
DISPLAY_SIZE = DISPLAY_WIDTH, DISPLAY_HEIGHT = 900, 500
screen = pygame.display.set_mode(DISPLAY_SIZE)
pygame.display.set_caption(f"15 puzzle solver version {Version}")
FPS = 60

pygame.init()
gui.init()
RUNNING = True
puzzle = Puzzle()
animating = None
searching = False
animate_solution = None
builder = ida.manage_pdb.PDB(PATTERN_SET)
building = 0
if builder.check_file() : building = 2
print("building : ", building)

def move_tile(dir, start_pos) : # dir is direction empty
    global puzzle, animating
    animating = gui.MoveAnimation(start_pos, dir, puzzle.get_v_at(start_pos))
    puzzle = puzzle.make_moved(dir)

def handle_solution_process() :
    global animate_solution, puzzle, searching
    if not animate_solution : return
    if animating == None :
        next_dir = animate_solution.get_next_dir()
        print(next_dir)
        if next_dir == None : 
            animate_solution = None
            searching = False
        else : move_tile(next_dir, animate_solution.get_move_startpos(puzzle.zero))

def find_solution() :
    global puzzle, searching, animating, animate_solution
    if puzzle.is_goal() : return
    searching = True
    gui.draw(screen, puzzle, animating, animate_solution, searching, building)
    solution = ida.ida_star(puzzle, PATTERN_SET)
    print("found solution : ", solution)
    animate_solution = gui.SolutionProcess(solution)

def build_pdb() :
    global builder, building, searching
    building = 1
    gui.draw(screen, puzzle, animating, animate_solution, searching, building)
    builder.build()
    building = 2

def handleInput(event, rects, buttons) :
    global puzzle, RUNNING, animating, builder
    mouse_pos = pygame.mouse.get_pos()
    if event.type == pygame.QUIT : RUNNING = False

    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 :
        if animating is not None : return
        for i, rect in rects.items() : # rects = dict
            if rect.collidepoint(mouse_pos) : 
                move_dir = puzzle.movable_dir(i)
                if move_dir != None :
                    move_tile(move_dir, i)
                return
        for i, button in enumerate(buttons) :
            if button.collidepoint(mouse_pos) :
                if i == 0 :
                    puzzle.shuffle_board()
                if i == 1 :
                    if not builder.check_file() : continue
                    find_solution()
                if i == 2 :
                    if builder.check_file() : continue
                    build_pdb()
    return

# MAIN GAMELOOP
def GameLoop() :
    global puzzle, RUNNING, seaching, animating, animate_solution

    # Game Loop
    clock = pygame.time.Clock()
    while RUNNING :
        if animate_solution : handle_solution_process()

        rects, buttons, animating = gui.draw(screen, puzzle, animating, animate_solution, searching, building) # GUI

        for event in pygame.event.get() :
            handleInput(event, rects, buttons)

        clock.tick(FPS)
    return

GameLoop()