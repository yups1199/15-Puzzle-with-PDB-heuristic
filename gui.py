import pygame

# BACKGROUND
BACKGROUND_COLOR = (30,30,30)

# TILE
TILE_SIZE = 120
TILE_GAP_SIZE = 4
TILE_COLOR = (0,101,169)
HOVER_TILE_COLOR = 	(0,152,255)
TITLE_FONT = None #init()
TILE_TEXT_COLOR = (250, 250, 250)

# Buttons
BUTTON_COLOR = (0,101,169)
HOVER_BUTTON_COLOR = 	(0,152,255)
BUTTON_FONT = None #init()
BUTTON_TEXT_COLOR = (250, 250, 250)
SEARCHING_BUTTON_COLOR = (255,188,0)
BUTTON1_WIDTH = 300
BUTTON1_HEIGHT = 90
BUTTON1_Y = 50
BUTTON1_X = 550
BUTTON2_Y = 160

# TEXT
SOLUTION_FONT = None #init()
SOLUTION_TEXT_COLOR = (164,212,163)
SOL_TEXT_POS = (560, 270)

class MoveAnimation :
    def __init__(self, start_idx, dir, v, duration = 10, pz_size = 4) :
        self.v = v
        self.progress = 0.0
        self.single_tick = 1.0 / duration

        s_row, s_col = divmod(start_idx, pz_size)
        self.sy = (s_row + 1) * TILE_GAP_SIZE + s_row * TILE_SIZE
        self.sx = (s_col + 1) * TILE_GAP_SIZE + s_col * TILE_SIZE

        d_row, d_col = (0, -1, 0, 1), (-1, 0, 1, 0) # oposite
        e_row, e_col = s_row + d_row[dir], s_col + d_col[dir]
        self.ey = (e_row + 1) * TILE_GAP_SIZE + e_row * TILE_SIZE
        self.ex = (e_col + 1) * TILE_GAP_SIZE + e_col * TILE_SIZE
        return
    
    def get_pos(self) :
        return (self.sy + (self.ey - self.sy) * self.progress, 
                self.sx + (self.ex - self.sx) * self.progress)
    
    def next_tick(self) :
        self.progress += self.single_tick
        return self.progress >= 1.0
    
    def get_tile_rect(self) :
        y, x = self.get_pos()
        return pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    
    def get_tile_text(self) :
        return TITLE_FONT.render(str(self.v), True, TILE_TEXT_COLOR)

class SolutionProcess :
    def __init__(self, sol) :
        self.solution = sol
        self.l = len(sol)
        self.progress = -1 
    def get_next_dir(self) :
        self.progress += 1
        if self.progress >= self.l : return None
        else : return self.solution[self.progress]
    def get_move_startpos(self, zero) : # for 4*4
        dir = self.solution[self.progress]
        dy, dx = (0, 1, 0, -1), (1, 0, -1, 0)
        zy, zx = zero // 4, zero % 4
        start_pos = (zy+dy[dir]) * 4 + (zx+dx[dir])
        return start_pos

def init() :
    global TITLE_FONT, BUTTON_FONT, SOLUTION_FONT
    TITLE_FONT = pygame.font.SysFont("Arial", 60)
    SOLUTION_FONT = pygame.font.SysFont("Arial", 30)
    BUTTON_FONT = pygame.font.SysFont("Arial", 60)

def make_tile_rects(pz) -> dict :
    rects = dict() # key = pos

    for i, v in enumerate(pz.board) :
        if v == 0 : continue
        row, col = divmod(i, pz.size)
        y = (row + 1) * TILE_GAP_SIZE + row * TILE_SIZE
        x = (col + 1) * TILE_GAP_SIZE + col * TILE_SIZE
        rects[i] = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    return rects

def draw_pz(screen, pz, animating, pause_hover, mouse_pos) -> dict :
    rects = make_tile_rects(pz)
    for i, v in enumerate(pz.board) :
        if v == 0 : continue
        if animating != None and animating.v == v : continue
        tile_rect = rects[i]

        if not pause_hover and pz.movable_dir(i) != None and tile_rect.collidepoint(mouse_pos) : 
            color = HOVER_TILE_COLOR
        else : color = TILE_COLOR
        pygame.draw.rect(screen, color, tile_rect)

        tile_text = TITLE_FONT.render(str(v), True, TILE_TEXT_COLOR)
        tile_text_rect = tile_text.get_rect(center=tile_rect.center)
        screen.blit(tile_text, tile_text_rect)
    return rects

def draw_buttons(screen, searching, pause_hover, mouse_pos) -> tuple :
    # BUTTON 1 rect
    button1 = pygame.Rect(BUTTON1_X, BUTTON1_Y, BUTTON1_WIDTH, BUTTON1_HEIGHT)
    if not pause_hover and button1.collidepoint(mouse_pos) : 
        b1_color = HOVER_BUTTON_COLOR
    else : b1_color = BUTTON_COLOR
    pygame.draw.rect(screen, b1_color, button1)

    # BUTTON 1 text
    b1_text = BUTTON_FONT.render("randomize", True, BUTTON_TEXT_COLOR)
    b1_text_rect = b1_text.get_rect(center=button1.center)
    screen.blit(b1_text, b1_text_rect)

    # BUTTON 2 rect
    button2 = pygame.Rect(BUTTON1_X, BUTTON2_Y, BUTTON1_WIDTH, BUTTON1_HEIGHT)
    if searching : b2_color = SEARCHING_BUTTON_COLOR
    elif not pause_hover and button2.collidepoint(mouse_pos) : 
        b2_color = HOVER_BUTTON_COLOR
    else : b2_color = BUTTON_COLOR
    pygame.draw.rect(screen, b2_color, button2)

    # BUTTON 2 text
    if searching : b2_str = "searching..."
    else : b2_str = "find solution"
    b2_text = BUTTON_FONT.render(b2_str, True, BUTTON_TEXT_COLOR)
    b2_text_rect = b2_text.get_rect(center=button2.center)
    screen.blit(b2_text, b2_text_rect)

    return (button1, button2)

def draw_anim(screen, animating) -> bool :
    tile_rect = animating.get_tile_rect()
    pygame.draw.rect(screen, TILE_COLOR, tile_rect)
    tile_text = animating.get_tile_text()
    tile_text_rect = tile_text.get_rect(center=tile_rect.center)
    screen.blit(tile_text, tile_text_rect)
    return animating.next_tick()

def draw_text(screen, sol) :
    solution_str = "optimal solution : " + str(sol) + " turns"
    solution_text = SOLUTION_FONT.render(solution_str, True, SOLUTION_TEXT_COLOR)
    screen.blit(solution_text, SOL_TEXT_POS)

def draw(screen, pz, animating, sol, searching = False) : # -> dict, tuple, MoveAnimation
    pause_hover = searching or animating

    screen.fill(BACKGROUND_COLOR)

    mouse_pos = pygame.mouse.get_pos()
    rects = draw_pz(screen, pz, animating, pause_hover, mouse_pos)
    if animating != None : 
        if draw_anim(screen, animating) : 
            animating = None
    buttons = draw_buttons(screen, searching, pause_hover, mouse_pos)
    if sol == None : draw_text(screen, 0)
    else : draw_text(screen, sol.l)
    pygame.display.flip()
    return rects, buttons, animating