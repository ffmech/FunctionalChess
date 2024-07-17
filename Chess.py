import pygame
from sys import exit

pygame.init()
screen = pygame.display.set_mode((700,700))
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()

en_passant_piece = None
active_color = True

class ChessSurface(pygame.Surface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tenant = None

    def change_color(self,color):
        self.fill(color)
        self.orig_color = color

class MyScaledSurface(pygame.Surface):
    def __init__(self, surface, size):
        super().__init__(size)
        self.scaled_surface = pygame.transform.scale(surface, size).convert_alpha()

    def compare_piece(self,piece):
        print(bin(self.piece_type)[1:],bin(piece)[1:])
        if bin(self.piece_type)[1:] == bin(piece)[1:]:
            return True
        else:
            return False

    def is_active_clr(self):
        #print("heeellloooo")
        if int(bin(self.piece_type)[-4:-3]) == int(active_color):
            return True
        else:
            return False


def reset_board(tiles=None):
    if tiles == None:
        tiles = backg

    num = 0
    for tile in tiles:
        print(tile.brd_index)
        num = (tile.brd_index//8)+1

        if (tile.brd_index+num)%2 == 0:
            color = (118,150,86)
        else:
            color = (245,245,220)

        tile.orig_color = color
        tile.fill(color)

def chess_board():
    chess_squares = []

    color = (245,245,220)
    size = 80
    nums = 0
    letters = 0
    board_index = 0
    tile_pos = [58,57]
    while True:
        if nums >= 8:
            nums = 0
            letters += 1
            tile_pos[0] = 58
            tile_pos[1] += 80
        if letters >= 8:
            break
        sq_surf = ChessSurface((size,size))
        color = (245,245,220)
        if ((nums%2) == 0) and ((letters%2) == 0):
            sq_surf.fill(color)
        elif ((nums%2) != 0) and ((letters%2) != 0):
            sq_surf.fill(color)
        else:
            color = (118,150,86)
            sq_surf.fill(color)

        sq_rect = sq_surf.get_rect(topleft = (nums*size+30,letters*size+30))
        sq_surf.bound_box = sq_rect
        sq_surf.orig_color = color
        sq_surf.brd_index = board_index
        sq_surf.piece_pos = tuple(tile_pos)
        #print(sq_surf)

        chess_squares.append(sq_surf)
        #[sq_surf,sq_rect,color,board_index])
        board_index += 1
        nums += 1
        tile_pos[0] += 80

    return chess_squares

backg = chess_board()
# if en_passant_piece != None:
#     backg[en_passant_piece].fill("Brown")

board = [0]*64

previous_board = board.copy()

def board_to_fen():
    type_pieces = {8:"K",
    9:"Q",
    10:"B",
    11:"N",
    12:"R",
    13:"P",
    16:"k",
    17:"q",
    18:"b",
    19:"n",
    20:"r",
    21:"p"}

    positions = ""
    num_variable = 0
    count = 0
    ac = "w"
    if not active_color:
        ac = "b"

    for i in board:
        if count >= 8:
            count = 0
            if num_variable > 0:
                positions += str(num_variable)
                num_variable = 0

            if i == 0:
                positions += "/"
                num_variable += 1
            else:
                positions += "/" + type_pieces[i]

            count += 1
            continue

        if i == 0:
            num_variable += 1
            count += 1
        elif num_variable > 0:
            positions += str(num_variable) + type_pieces[i]
            count += 1
            num_variable = 0
        else:
            positions += type_pieces[i]
            count += 1

    return positions + f" {ac} KQkq e4 0 1"

def renderPieces(fen):
    global active_color
    piece_types = {"K": 8,
    "Q": 9,
    "B": 10,
    "N": 11,
    "R": 12,
    "P": 13,
    "k": 16,
    "q": 17,
    "b": 18,
    "n": 19,
    "r": 20,
    "p": 21}
    pieces = []
    fen = fen.split()
    piece_pos = fen[0]
    #print(piece_pos)

    if fen[1] == "w":
        print(fen[1])
        active_color = True
    else:
        active_color = False

    i_pos = [70,70]
    board_index = 0
    for i in piece_pos:
        #print(piece_pos)
        try:
            a = piece_types[i]
        except KeyError:
            if i == "/":
                #board_index += 1
                i_pos[1] += 80
                i_pos[0] = 70
            elif i.isnumeric():
                board_index += int(i)
                i_pos[0] += 80*int(i)
            continue

        board[board_index] = a

        piece_surf = pygame.image.load("pieces.png")
        piece_surf = MyScaledSurface(piece_surf,(500,166))

        texture = [0,0]
        a_type = a - 8
        if a_type >= 8:
            #print(a)
            texture[1] = 85
            a_type -= 8
            #print(pieza)

        texture[0] = 83*a_type

        piece_rect = piece_surf.get_rect(center=(208+i_pos[0],40+i_pos[1]),size=(60,60))
        piece_surf.bound_box = piece_rect
        piece_surf.texture = texture
        piece_surf.brd_index = board_index
        piece_surf.piece_type = a

        movies = board_index

        piece_surf.good_moves = pieceMoves

        backg[board_index].tenant = piece_surf
        #print(backg[0].tenant)
        #piece_surf.fill((255,177,77))     278          110
        #piece_rect = piece_surf.get_rect(center=tuple(i_pos))
        pieces.append(piece_surf)
        #[piece_surf,piece_rect,texture,board_index-1,a])
        i_pos[0] += 80
        if board_index < 64:
            board_index += 1

    board_range = "abcdefgh12345678"
    global en_passant_piece
    if fen[3] == "-":
        print("Nope")
        en_passant_piece = None
    else:
        print("Yeah")
        en_passant_index = board_range.index(fen[3][0])*8 + board_range.index(fen[3][1])
        en_passant_piece = backg[en_passant_index].tenant

    print(fen)
    print(board)
    return pieces

def is_touching_walls(self_pos,angle):
    if angle%8 == 0:
        return False
    if self_pos%8 == 0 or (self_pos+1)%8 == 0:
        return True
    else:
        return False

def row_difference(pos_1,pos_2):
    return abs((pos_1//8) - (pos_2//8))

def is_on_same_row(self_pos,orig_pos,angle):
    if self_pos == orig_pos:
        return False
    if angle%8 == 0:
        return False
    if angle < 5:
        return False
    if self_pos//8 == orig_pos//8:
        print("This should work")
        return True
    else:
        return False

def piece_occupancy(self_pos,orig_pos):
    print(self_pos)
    if board[self_pos] != 0 and self_pos != orig_pos:
        if is_same_color(backg[orig_pos].tenant,backg[self_pos].tenant):
            print("Same color")
            return 1
        else:
            return 2
    else:
        return 0

moveType = {8:(1,(1,7,8,9),False),
9:(8,(1,7,8,9),False),
10:(8,(7,9),False),
11:(1,(6,10,15,17),False),
12:(8,(1,8),False),
13:(1,(7,8,9),True),
16:(1,(1,7,8,9),False),
17:(8,(1,7,8,9),False),
18:(8,(7,9),False),
19:(1,(6,10,15,17),False),
20:(8,(1,8),False),
21:(1,(7,8,9),True)}

def pieceMoves(piece,scope=1,angles=(6,10,15,17),pawn=False):
    possible_moves = []
    self_pos = piece.brd_index
    orig_pos = self_pos
    if isinstance(angles, int):
        angles = [angles]

    for angle in angles:
        self_pos = orig_pos
        times_mag = 0
        if angle == 8 and pawn == True and self_pos//8 in (6,1):
            scope = 2
            print(scope)
        elif pawn == True:
            scope = 1
            print(scope)

        for i in range(scope):
            if pawn == True and piece.piece_type < 16:
                break
            if self_pos > (63 - angle):
                print("too big")
                break
            if is_touching_walls(self_pos,angle) and is_touching_walls(self_pos+angle,angle):
                print("bottom touched walls")
                break

            self_pos += angle
            times_mag += 1

            if piece_occupancy(self_pos,orig_pos) == 1:
                self_pos -= angle
                times_mag -= 1
                break
            elif piece_occupancy(self_pos,orig_pos) == 2:
                if angle == 8 and pawn == True:
                    self_pos -= angle
                    times_mag -= 1
                break
            elif angle in (7,9) and pawn == True:
                self_pos -= angle
                times_mag -= 1


        #print(self_pos)

        for i in range(1+scope+times_mag):
            if pawn == True and piece.piece_type > 14 and self_pos == orig_pos:
                break
            if self_pos < 0:
                print("Too small")
                break
            if is_touching_walls(self_pos,angle) and is_touching_walls(self_pos-angle,angle):
                if self_pos != orig_pos:
                    if piece_occupancy(self_pos,orig_pos) == 0 or piece_occupancy(self_pos,orig_pos) == 2:
                        if angle in (7,9) and pawn == True and piece_occupancy(self_pos,orig_pos) == 0:
                            break
                        possible_moves.append(self_pos)
                    #possible_moves.append(self_pos)
                print("top touched walls")
                break
            if angle > 4 and row_difference(self_pos,orig_pos) == 0:
                self_pos -= angle
                continue
            if angle < 15 and angle > 9 and row_difference(self_pos,orig_pos) > 1:
                self_pos -= angle
                continue
            if angle > 14 and row_difference(self_pos,orig_pos)%2 != 0:
                self_pos -= angle
                continue

            if self_pos < orig_pos and board[self_pos] != 0:
                #if not is_same_color(backg[orig_pos].tenant,backg[self_pos].tenant):
                if piece_occupancy(self_pos,orig_pos) == 2:
                    if angle == 8 and pawn == True:
                        break
                    possible_moves.append(self_pos)
                break
            if piece_occupancy(self_pos,orig_pos) == 0:
                if angle in (7,9) and pawn == True:
                    # if en_passant_piece != None and self_pos in [en_passant_piece.brd_index+8,en_passant_piece.brd_index-8]:
                    #     possible_moves.append(self_pos)
                    break

            if self_pos != orig_pos:
                #if piece_occupancy(self_pos,orig_pos) == 2:
                possible_moves.append(self_pos)

            self_pos -= angle
        #print(self_pos)

    return [backg[x] for x in possible_moves]


pieces = renderPieces("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

#rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR
#PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP/PPPPPPPP
def process_ep():
    pass

def focus_piece(piece):
    global piece_dragging, current_piece
    reset_board()
    backg[piece.brd_index].orig_color = (255,255,0)
    backg[piece.brd_index].fill("Yellow")
    print("Collision")
    current_piece = piece
    pieces.remove(piece)
    pieces.append(current_piece)
    piece_dragging = True
    mouse_x, mouse_y = event.pos
    # offset_x = current_piece.bound_box.x - mouse_x
    # offset_y = current_piece.bound_box.y - mouse_y

def is_same_color(p1,p2):
    isc = len(bin(p1.piece_type)) == len(bin(p2.piece_type))
    return isc

piece_dragging = False
current_piece = None
active_moves = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.MOUSEMOTION:
            if piece_dragging:

                mouse_x, mouse_y = event.pos
                current_piece.bound_box.center = mouse_x-15, mouse_y# + offset_x
                #current_piece.bound_box.y = mouse_y# + offset_y

            for i in backg:
                if i.bound_box.collidepoint(event.pos):
                    i.fill(tuple(0.7*x for x in i.orig_color))
                else:
                    i.fill(i.orig_color)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            if current_piece != None and current_piece.bound_box.collidepoint(event.pos):
                piece_dragging = True

            rev_pieces = pieces.copy()
            rev_pieces.reverse()
            #for piece in rev_pieces:
            #    if piece.bound_box.collidepoint(event.pos) and current_piece != None and is_same_color(piece,current_piece):
            #        current_piece.bound_box.center = backg[current_piece.brd_index].piece_pos
            #        if not piece_dragging: focus_piece(piece)
            #        break

            #    if piece.bound_box.collidepoint(event.pos) and current_piece == None:
            #        focus_piece(piece)
            for i in backg:
                if i.tenant == None:
                    continue

                if not i.tenant.is_active_clr():
                    continue

                if i.bound_box.collidepoint(event.pos) and current_piece == None:
                    focus_piece(i.tenant)
                    break

                if i.bound_box.collidepoint(event.pos) and current_piece != None and is_same_color(i.tenant, current_piece):
                    current_piece.bound_box.center = backg[current_piece.brd_index].piece_pos
                    if not piece_dragging: focus_piece(i.tenant)


            print(current_piece)
            if current_piece != None:
                active_moves = current_piece.good_moves(current_piece,*moveType[current_piece.piece_type])
                # for i in active_moves:
                #     i.change_color((255,0,0))
                    # i.orig_color = (255,0,0)
                    # i.fill((255,0,0))

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and current_piece != None:
            for i in backg:

                if i.bound_box.collidepoint(event.pos) and current_piece.brd_index != i.brd_index:

                    if i not in active_moves:
                        print(active_moves, i)
                        current_piece.bound_box.center = backg[current_piece.brd_index].piece_pos
                        break

                    if i.tenant != None:
                        if is_same_color(i.tenant,current_piece):
                            current_piece.bound_box.center = backg[current_piece.brd_index].piece_pos
                            break
                        pieces.remove(i.tenant)

                    # print("THIS IS THE DIFFERENCE: ", abs(i.brd_index - current_piece.brd_index))
                    # if current_piece.compare_piece(13) and abs(i.brd_index - current_piece.brd_index) == 16:
                    #     en_passant_piece = current_piece
                    #     print("THIS IS EP: ",en_passant_piece)
                    #     i.change_color((0,0,0))
                    # else:
                    #     en_passant_piece = None

                    backg[current_piece.brd_index].tenant = None
                    i.tenant = current_piece
                    current_piece.bound_box.center = i.piece_pos
                    board[current_piece.brd_index] = 0
                    board[i.brd_index] = current_piece.piece_type
                    current_piece.brd_index = i.brd_index
                    active_color = not active_color

                    current_piece = None

                    reset_board(active_moves)
                    i.orig_color = (255,0,255)
                    i.fill((255,0,255))
                    break
                #elif i.bound_box.collidepoint(event.pos):
                else:
                    current_piece.bound_box.center = backg[current_piece.brd_index].piece_pos

            new_board = board_to_fen()

            print(new_board)
            piece_dragging = False

    screen.fill("Black")

    for i in backg:
        screen.blit(i,i.bound_box)
        if i.tenant != None:
            screen.blit(i.tenant.scaled_surface,i.tenant.bound_box,(i.tenant.texture[0],i.tenant.texture[1],80,80))

        if current_piece != None and i in active_moves:
            if i.tenant != None:
             # or (en_passant_piece != None and i.brd_index in [en_passant_piece.brd_index-8,en_passant_piece.brd_index+8]):
                i.change_color((255,0,0))
            else:
                pygame.draw.circle(screen, tuple(x*0.8 for x in i.orig_color), i.bound_box.center, 20)

    for i in pieces:
         screen.blit(i.scaled_surface,i.bound_box,(i.texture[0],i.texture[1],80,80))

    pygame.display.update()
    clock.tick(60)
