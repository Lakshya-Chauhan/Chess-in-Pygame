from thechess import *
import pygame
from os import system
FoNt = 0
FoNtprint = 0
old_chance = 0
chance = 1
distx = 0
disty = 0
blocksize = 100
mouseDown = 2
screen_size = [800, 800]
pieceClicked = False
elemClickIndex = None
translucentOldPos = 0
check_mate = False
elemPos2 = tuple()
surfaces = [
    [None, pygame.transform.scale(pygame.image.load("images/wK.png"), (blocksize, blocksize)),
     pygame.transform.scale(pygame.image.load("images/bK.png"), (blocksize, blocksize))],

    [None, pygame.transform.scale(pygame.image.load("images/wQ.png"), (blocksize, blocksize)),
     pygame.transform.scale(pygame.image.load("images/bQ.png"), (blocksize, blocksize))],

    [None, pygame.transform.scale(pygame.image.load("images/wR.png"), (blocksize, blocksize)),
     pygame.transform.scale(pygame.image.load("images/bR.png"), (blocksize, blocksize))],

    [None, pygame.transform.scale(pygame.image.load("images/wB.png"), (blocksize, blocksize)),
     pygame.transform.scale(pygame.image.load("images/bB.png"), (blocksize, blocksize))],

    [None, pygame.transform.scale(pygame.image.load("images/wN.png"), (blocksize, blocksize)),
     pygame.transform.scale(pygame.image.load("images/bN.png"), (blocksize, blocksize))],

    [None, pygame.transform.scale(pygame.image.load("images/wP.png"), (blocksize, blocksize)),
     pygame.transform.scale(pygame.image.load("images/bP.png"), (blocksize, blocksize))]
]


PIECES = [
    chess((0, 7), 5, -1, 2, 1),
    chess((1, 7), 3, -1, 4, 2),
    chess((2, 7), 3, -1, 3, 3),
    chess((3, 7), 0, -1, 0, 4),
    chess((4, 7), 9, -1, 1, 5),
    chess((5, 7), 3, -1, 3, 6),
    chess((6, 7), 3, -1, 4, 7),
    chess((7, 7), 5, -1, 2, 8),

    chess((0, 6), 1, -1, 5, 9),
    chess((1, 6), 1, -1, 5, 10),
    chess((2, 6), 1, -1, 5, 11),
    chess((3, 6), 1, -1, 5, 12),
    chess((4, 6), 1, -1, 5, 13),
    chess((5, 6), 1, -1, 5, 14),
    chess((6, 6), 1, -1, 5, 15),
    chess((7, 6), 1, -1, 5, 16),


    chess((0, 0), 5, 1, 2, 17),
    chess((1, 0), 3, 1, 4, 18),
    chess((2, 0), 3, 1, 3, 19),
    chess((3, 0), 0, 1, 0, 20),
    chess((4, 0), 9, 1, 1, 21),
    chess((5, 0), 3, 1, 3, 22),
    chess((6, 0), 3, 1, 4, 23),
    chess((7, 0), 5, 1, 2, 24),

    chess((0, 1), 1, 1, 5, 25),
    chess((1, 1), 1, 1, 5, 26),
    chess((2, 1), 1, 1, 5, 27),
    chess((3, 1), 1, 1, 5, 28),
    chess((4, 1), 1, 1, 5, 29),
    chess((5, 1), 1, 1, 5, 30),
    chess((6, 1), 1, 1, 5, 31),
    chess((7, 1), 1, 1, 5, 32)
]

# Yin Yang


def cls():
    system("cls")


def font(a: str, b=18):
    global FoNt
    FoNt = pygame.font.SysFont(a, b, True)


def printpy(x: str, a=(100, 400), y=(128, 128, 128)):
    global FoNt, FoNtprint
    FoNtprint = FoNt.render(x, True, y)
    screen.blit(FoNtprint, ((int(a[0]/2)-int((FoNtprint.get_width())/2)),
                (int(a[1]/2)-int((FoNtprint.get_height())/2))))


pygame.init()
screen = pygame.display.set_mode((screen_size[0], screen_size[1]))
#icon = pygame.image.load('')
pygame.display.set_caption("Chess")
# pygame.display.set_icon(icon)
cls()


def board():
    global distx, disty, blocksize
    for x in range(8):
        for y in range(8):
            if x % 2 == 0:
                if y % 2 == 0:
                    pygame.draw.rect(screen, (242, 232, 168), pygame.Rect(
                        distx + x*blocksize, disty + y*blocksize, blocksize, blocksize))
                else:
                    pygame.draw.rect(screen, (125, 70, 70), pygame.Rect(
                        distx + x*blocksize, disty + y*blocksize, blocksize, blocksize))
            else:
                if y % 2 == 0:
                    pygame.draw.rect(screen, (125, 70, 70), pygame.Rect(
                        distx + x*blocksize, disty + y*blocksize, blocksize, blocksize))
                else:
                    pygame.draw.rect(screen, (242, 232, 168), pygame.Rect(
                        distx + x*blocksize, disty + y*blocksize, blocksize, blocksize))


def Chessman():
    global PIECES, surfaces, distx, disty, blocksize, elemClickIndex, translucentOldPos
    for i in PIECES:
        if i.captured == False:
            if PIECES.index(i) != elemClickIndex:
                screen.blit(surfaces[i.piece][i.color],
                            (distx + i.temp_pos[0]*blocksize, disty + i.temp_pos[1]*blocksize))
            else:
                translucentOldPos = pygame.transform.scale(
                    surfaces[i.piece][i.color], (blocksize, blocksize))
                translucentOldPos.set_alpha(150)
                screen.blit(translucentOldPos,
                            (distx + i.pos[0]*blocksize, disty + i.pos[1]*blocksize))
    if elemClickIndex != None:
        screen.blit(surfaces[PIECES[elemClickIndex].piece][PIECES[elemClickIndex].color],
                    (PIECES[elemClickIndex].temp_pos[0] - PIECES[elemClickIndex].delx, PIECES[elemClickIndex].temp_pos[1] - PIECES[elemClickIndex].dely))


def movesView():
    global elemClickIndex, pieceClicked, PIECES, distx, disty, blocksize, elemPos2
    if elemClickIndex != None and pieceClicked == True:
        for legal_pos in PIECES[elemClickIndex].legal_moves(False):
            rectangle = pygame.Surface((blocksize, blocksize))
            rectangle.set_alpha(200)
            if legal_pos == elemPos2:
                rectangle.fill((71, 214, 187))
                screen.blit(
                    rectangle, (distx + legal_pos[0]*blocksize, disty + legal_pos[1]*blocksize))
            else:
                rectangle.fill((71, 209, 69))
                screen.blit(
                    rectangle, (distx + legal_pos[0]*blocksize, disty + legal_pos[1]*blocksize))
        rectangle = pygame.Surface((blocksize, blocksize))
        rectangle.set_alpha(150)
        rectangle.fill((69, 71, 209))
        screen.blit(rectangle, (distx + PIECES[elemClickIndex].pos[0]
                    * blocksize, disty + PIECES[elemClickIndex].pos[1]*blocksize))


def lastmove():
    global PIECES, distx, disty, blocksize, check_mate, screen_size
    font("Calibri", 100)
    if len(chess.Moves) != 0 and check_mate == False:
        elem = chess.obj_from_num(chess.Moves[-1][0])
        Lastmove = pygame.Surface((blocksize, blocksize))
        Lastmove.set_alpha(150)
        Lastmove.fill((235, 225, 76))
        screen.blit(
            Lastmove, (distx + chess.Moves[-1][1][0]*blocksize, disty + chess.Moves[-1][1][1]*blocksize))
        Lastmove = pygame.Surface((blocksize, blocksize))
        Lastmove.set_alpha(150)
        Lastmove.fill((212, 203, 69))
        screen.blit(
            Lastmove, (distx + elem.pos[0]*blocksize, disty + elem.pos[1]*blocksize))
    if chess.check(-1) == True:
        for i in PIECES:
            if i.color == -1 and i.captured == False:
                if i.piece == 0:
                    if check_mate == False:
                        for a in range(blocksize, int(blocksize/2), -int(blocksize/15)-1):
                            Lastmove = pygame.Surface((a, a))
                            Lastmove.set_alpha(200-a)
                            Lastmove.fill((200, 50, 50))
                            screen.blit(Lastmove, (distx + int(blocksize/2) - int(
                                a/2) + i.pos[0]*blocksize, disty + int(blocksize/2) - int(a/2) + i.pos[1]*blocksize))
                    if len(chess.total_legal_moves(i.color)) == 0:
                        check_mate = True

                        for x in range(blocksize*8+distx, 0, -int(blocksize/2.5)):
                            for y in range(blocksize*8+disty, 0, -int(blocksize/2.5)):
                                Lastmove = pygame.Surface((x, y))
                                Lastmove.set_alpha(((int(((((blocksize*8+distx)*(blocksize*8+disty))-x*y)/(
                                    (blocksize*8+distx)*(blocksize*8+disty)))*15)) % 256))
                                Lastmove.fill((255, 255, 255))
                                screen.blit(Lastmove, ((
                                    round(screen_size[0]/2) - round(x/2)), (round(screen_size[1]/2) - round(y/2))))
                        printpy("Check Mate!",
                                screen_size, (28, 82, 156))
                        font("Calibri",40)
                        if i.color == -1:
                            printpy("White Wins",(screen_size[0],screen_size[1]+200),(28, 82, 156))
                        else:
                            printpy("Black Wins",(screen_size[0],screen_size[1]+200),(28, 82, 156))
                    elif (chess.total_cost(i.color) in [3, 0]) and (chess.total_cost(-i.color) in [3, 0]):
                        check_mate = 1

                        for x in range(blocksize*8+distx, 0, -int(blocksize/2.5)):
                            for y in range(blocksize*8+disty, 0, -int(blocksize/2.5)):
                                Lastmove = pygame.Surface((x, y))
                                Lastmove.set_alpha(((int(((((blocksize*8+distx)*(blocksize*8+disty))-x*y)/(
                                    (blocksize*8+distx)*(blocksize*8+disty)))*15)) % 256))
                                Lastmove.fill((255, 255, 255))
                                screen.blit(Lastmove, ((
                                    round(screen_size[0]/2) - round(x/2)), (round(screen_size[1]/2) - round(y/2))))
                        printpy("Draw!", screen_size, (28, 82, 156))
                    break
    elif chess.check(1) == True:
        for i in PIECES:
            if i.color == 1 and i.captured == False:
                if i.piece == 0:
                    if check_mate == False:
                        for a in range(blocksize, int(blocksize/2), -int(blocksize/15)-1):
                            Lastmove = pygame.Surface((a, a))
                            Lastmove.set_alpha(200-a)
                            Lastmove.fill((200, 50, 50))
                            screen.blit(Lastmove, (distx + int(blocksize/2) - int(
                                a/2) + i.pos[0]*blocksize, disty + int(blocksize/2) - int(a/2) + i.pos[1]*blocksize))
                    if len(chess.total_legal_moves(i.color)) == 0:
                        check_mate = True

                        for x in range(blocksize*8+distx, 0, -int(blocksize/2.5)):
                            for y in range(blocksize*8+disty, 0, -int(blocksize/2.5)):
                                Lastmove = pygame.Surface((x, y))
                                Lastmove.set_alpha(((int(((((blocksize*8+distx)*(blocksize*8+disty))-x*y)/(
                                    (blocksize*8+distx)*(blocksize*8+disty)))*15)) % 256))
                                Lastmove.fill((255, 255, 255))
                                screen.blit(Lastmove, ((
                                    round(screen_size[0]/2) - round(x/2)), (round(screen_size[1]/2) - round(y/2))))
                        printpy("Check Mate!",
                                screen_size, (28, 82, 156))
                        font("Calibri",40)
                        if i.color == -1:
                            printpy("White Wins",(screen_size[0],screen_size[1]+200),(28, 82, 156))
                        else:
                            printpy("Black Wins",(screen_size[0],screen_size[1]+200),(28, 82, 156))
                    elif (chess.total_cost(i.color) in [3, 0]) and (chess.total_cost(-i.color) in [3, 0]):
                        check_mate = 1

                        for x in range(blocksize*8+distx, 0, -int(blocksize/2.5)):
                            for y in range(blocksize*8+disty, 0, -int(blocksize/2.5)):
                                Lastmove = pygame.Surface((x, y))
                                Lastmove.set_alpha(((int(((((blocksize*8+distx)*(blocksize*8+disty))-x*y)/(
                                    (blocksize*8+distx)*(blocksize*8+disty)))*15)) % 256))
                                Lastmove.fill((255, 255, 255))
                                screen.blit(Lastmove, ((
                                    round(screen_size[0]/2) - round(x/2)), (round(screen_size[1]/2) - round(y/2))))
                        printpy("Draw!", screen_size, (28, 82, 156))
                    break
    elif (len(chess.total_legal_moves(-1)) == 0) or (len(chess.total_legal_moves(1)) == 0) or ((chess.total_cost(1) in [3, 0]) and (chess.total_cost(-1) in [3, 0])):
        check_mate = 1
        for x in range(blocksize*8+distx, 0, -int(blocksize/2.5)):
            for y in range(blocksize*8+disty, 0, -int(blocksize/2.5)):
                Lastmove = pygame.Surface((x, y))
                Lastmove.set_alpha(((int(((((blocksize*8+distx)*(blocksize*8+disty))-x*y)/(
                    (blocksize*8+distx)*(blocksize*8+disty)))*15)) % 256))
                Lastmove.fill((255, 255, 255))
                screen.blit(Lastmove, ((
                    round(screen_size[0]/2) - round(x/2)), (round(screen_size[1]/2) - round(y/2))))
        printpy("Draw!", screen_size, (28, 82, 156))


running = True
clock = pygame.time.Clock()
while running == True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseDown += 1
            if mouseDown % 3 == 0 and check_mate == False:
                mouseDown += 1
                mpos = pygame.mouse.get_pos()
                pieceClicked = False
                if mpos[0] > distx and mpos[0] < distx+blocksize*8 and mpos[1] > disty and mpos[1] < disty+blocksize*8:
                    pieceClicked = True
                    elemPos = (((mpos[0]-distx)//blocksize),
                               ((mpos[1]-disty)//blocksize))

                    for elemIndex in range(len(PIECES)):
                        if PIECES[elemIndex].captured == False:
                            if PIECES[elemIndex].pos == elemPos and PIECES[elemIndex].color == chance:
                                elemClickIndex = elemIndex
                                PIECES[elemIndex].temp_pos = mpos
                                PIECES[elemIndex].delx = mpos[0] - \
                                    (PIECES[elemIndex].pos[0]
                                     * blocksize + distx)
                                PIECES[elemIndex].dely = mpos[1] - \
                                    (PIECES[elemIndex].pos[1]
                                     * blocksize + disty)

        if event.type == pygame.MOUSEMOTION:
            if pieceClicked == True and elemClickIndex != None:
                mpos2 = pygame.mouse.get_pos()
                PIECES[elemClickIndex].temp_pos = mpos2
                elemPos2 = (((mpos2[0]-distx)//blocksize),
                            ((mpos2[1]-disty)//blocksize))
                del mpos2

        if event.type == pygame.MOUSEBUTTONUP:
            if pieceClicked == True and elemClickIndex != None:
                if mouseDown % 3 == 1:
                    mouseDown += 1
                elif mouseDown % 3 == 0:
                    mouseDown += 2
                mpos1 = pygame.mouse.get_pos()
                elemPos1 = (((mpos1[0]-distx)//blocksize),
                            ((mpos1[1]-disty)//blocksize))
                del mpos1
                if PIECES[elemClickIndex].legal_moves(True, elemPos1) == True and PIECES[elemClickIndex].color == chance:
                    chess.Moves.append(
                        [PIECES[elemClickIndex].number, PIECES[elemClickIndex].pos, elemPos1])
                    chance = -chance
                    PIECES[elemClickIndex].pos = elemPos1
                    PIECES[elemClickIndex].temp_pos = elemPos1
                    PIECES[elemClickIndex].delx = 0
                    PIECES[elemClickIndex].dely = 0
                    PIECES[elemClickIndex].moves += 1
                    if PIECES[elemClickIndex].piece == 5:
                        if PIECES[elemClickIndex].pos[1] in [0, 7]:
                            PIECES[elemClickIndex].piece = 1
                            PIECES[elemClickIndex].cost = 9

                    capturedNumber = [(i.number) for i in PIECES if ((i.pos == PIECES[elemClickIndex].pos) and
                                      (i.color != PIECES[elemClickIndex].color) and (i.captured == False))]
                    if len(capturedNumber) == 1:
                        for i in range(len(PIECES)):
                            if PIECES[i].captured == False:
                                if PIECES[i].number == capturedNumber[0]:
                                    PIECES[i].captured = True
                                    PIECES[elemClickIndex].captures += 1

                    elif PIECES[elemClickIndex].pos == PIECES[elemClickIndex].en_passant[1]:
                        for captured_elem in PIECES:
                            if captured_elem.number == PIECES[elemClickIndex].en_passant[0]:
                                captured_elem.captured = True
                                PIECES[elemClickIndex].en_passant = [
                                    False, False]
                                break
                    pieceClicked = False
                    elemClickIndex = None
                else:
                    PIECES[elemClickIndex].temp_pos = PIECES[elemClickIndex].pos
                    pieceClicked = False
                    elemClickIndex = None

    # Code Here
    if old_chance != chance:
        old_chance = chance
        for i in PIECES:
            i.pos = ((7-i.pos[0]),(7-i.pos[1]))
            i.init_pos = ((7-i.init_pos[0]),(7-i.init_pos[1]))
            i.temp_pos = ((7-i.temp_pos[0]),(7-i.temp_pos[1]))
        if len(chess.Moves) > 0:
            chess.Moves[-1][2] = ((7-chess.Moves[-1][2][0]),(7-chess.Moves[-1][2][1]))
            chess.Moves[-1][1] = ((7-chess.Moves[-1][1][0]),(7-chess.Moves[-1][1][1]))
    if check_mate == False:
        board()
        if elemClickIndex != None and pieceClicked == True:
            movesView()
        else:
            lastmove()
        Chessman()
    else:
        board()
        Chessman()
        lastmove()
    pygame.display.update()
