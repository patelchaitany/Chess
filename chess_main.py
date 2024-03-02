import pygame as p
import time
import sys 
import chess

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['bp','bR','wR','bB','wB','bN','wN','bQ','wQ','bK','wK','wp']

    for i in pieces:
        IMAGES[i] = p.image.load("images/"+i+".png")

def main():
    p.init()
    screen = p.display.set_mode((WIDTH,HEIGHT))
    clock= p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chess.GameState()  
    loadImages()
    run = True
    sqselected = ()
    playerclick = []
    validMoves = gs.getValidMoves()
    moveMade = False

    while run:
        for event in p.event.get():
            if event.type == p.QUIT:
                run = False
            elif event.type ==p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                print(row,"<row","col>",col)
                pices = gs.board[row][col]
                if pices != "--":
                    color = p.Color("dark gray")
                    p.draw.rect(screen,color,p.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))
                    screen.blit(IMAGES[pices],p.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))
                    p.display.flip()
                else:
                    color = p.Color("red")
                    p.draw.rect(screen,color,p.Rect(col*SQ_SIZE,row*SQ_SIZE,SQ_SIZE,SQ_SIZE))
                    p.display.flip()


                if sqselected == (row,col):
                    sqselected = ()
                    playerclick = [] 
                else :
                    sqselected = (row,col)
                    playerclick.append(sqselected)
                if len(playerclick)==2 :
                    move = chess.Move(playerclick[0],playerclick[1],gs.board)
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                        sqselected = ()
                        playerclick = []
                        print("-"*30)
                    else :
                        sqselected = ()
                        playerclick = []    

            elif event.type == p.KEYDOWN:
                if event.key == p.K_z:
                    gs.undoMove()
                    moveMade = True
                    print("*"*30)
            if moveMade:
                validMoves = gs.getValidMoves()
                moveMade = False

        if (len(sqselected)==0 and len(playerclick)==0):
         drawGameState(screen,gs)
         clock.tick(MAX_FPS)
         p.display.flip() 

def drawGameState(screen,gs):
    drawBoard(screen)
    drawPieces(screen,gs.board)

def drawBoard(screen):
    colors = [p.Color("light gray"),p.Color("gray")]
    for i in range(DIMENSION):
        for j in range(DIMENSION):
            color = colors[((i+j)%2)]
            p.draw.rect(screen,color,p.Rect(i*SQ_SIZE,j*SQ_SIZE,SQ_SIZE,SQ_SIZE))

def drawPieces(screen,board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            pices = board[r][c]
            if pices != "--":
                screen.blit(IMAGES[pices],p.Rect(c*SQ_SIZE,r*SQ_SIZE,SQ_SIZE,SQ_SIZE))


main()
