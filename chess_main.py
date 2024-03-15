import pygame as p
import time
import sys,copy
import chess
import chess_AI
import torch
import argparse

WIDTH = HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}

def loadImages():
    pieces = ['bp','bR','wR','bB','wB','bN','wN','bQ','wQ','bK','wK','wp']

    for i in pieces:
        IMAGES[i] = p.image.load("images/"+i+".png")

def main(mode):
    p.init()
    gs = chess.GameState()  

    run = True
    sqselected = ()
    playerclick = []
    validMoves = gs.getValidMoves()
    moveMade = False
    human = False
    gen = chess_AI.GenrateMove()
    eval  = chess_AI.Evaluate()
    win = None
    data = []
    game_end = False
    bot = chess_AI.train()
    games = []
    play = 0
    train = True
    if mode == "train":
        train = True
        human = False
    elif mode == "human":
        train = False
        human = True
    elif mode == "ai":
        train = False
        human = True


    if not train:
        screen = p.display.set_mode((WIDTH,HEIGHT))
        clock= p.time.Clock()
        screen.fill(p.Color("white"))
        loadImages()
    while run:
        
    
        if human:
            for event in p.event.get():
                if event.type == p.QUIT:
                    run = False
                elif event.type ==p.MOUSEBUTTONDOWN:
                    location = p.mouse.get_pos()
                    col = location[0]//SQ_SIZE
                    row = location[1]//SQ_SIZE
                    # print(row,"<row","col>",col)
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
                            # print("-"*30)
                        else :
                            sqselected = ()
                            playerclick = []    

                elif event.type == p.KEYDOWN:
                    if event.key == p.K_z:
                        gs.undoMove()
                        moveMade = False
                        human = True
                        validMoves = gs.getValidMoves()
                        # print("*"*30)
                if moveMade:
                    validMoves = gs.getValidMoves()
                    moveMade = False
                    if mode == "ai":
                        human = False
                    elif mode == "human":
                        human = True

        elif len(validMoves)>=1 and gen.getpiece(gs)>2 and not game_end and (mode == "train" or mode == "ai"):
            if play < 60:
                print("moves",play)
                play = play + 1
                score = eval.evaluate(gs)
                games.append([gs.board,score])
                validMoves = gs.getValidMoves()
                m_move = gen.genrate_move(gs, validMoves,train=train)
                gs.makeMove(m_move)
                validMoves = gs.getValidMoves()
                if mode == "ai":
                    human = True
                gs.print_board()
                print("\n\n\n\n")
            else:
                game_end = True

        elif not game_end and (mode == "train" or mode == "ai") :
            game_end = True

        elif game_end:
            game_end = True
            print(len(games))
            bot.getscore(gameState=gs,win=win,data=games)
            play = 0
            games = []
            gs.__init__()
            game_end = False
            gs = copy.deepcopy(chess.GameState())
            validMoves = gs.getValidMoves()
            play = play + 1
            time.sleep(5)

        if not train:
            if (len(sqselected)==0 and len(playerclick)==0):
                drawGameState(screen,gs)
                clock.tick(MAX_FPS)
                p.display.flip() 
            if len(validMoves) == 0:
                print("game over")
                run = False

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



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chess AI")
    parser.add_argument("--mode", choices=["train", "human", "ai"], required=True, help="Mode of the game. 'train' for training the AI, 'human' for playing against a human, 'ai' for playing against an AI.")
    args = parser.parse_args()
    main(args.mode)
