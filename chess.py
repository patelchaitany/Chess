import pygame
import sys
import os
import time
import math

class GameState():
    def __init__(self):
        #8x8 chess board
        self.board= [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"]
        ]
        self.whiteToMove = True
        self.moveLog = []
        self.whiteKing = (7,4)
        self.blackKing = (0,4)
        self.pinPiece = []
        self.chakeByPiece = []
        

    def makeMove(self,move):
            self.board[move.startRow][move.startCol] = "--"
            self.board[move.endRow][move.endCol] = move.piceMoved
            self.moveLog.append(move)
            self.whiteToMove = not self.whiteToMove
            if move.piceMoved == "wK":
                 self.whiteKing = (move.endRow,move.endCol)
            elif move.piceMoved == "bK":
                 self.blackKing = (move.endRow,move.endCol)


    def undoMove(self):
         if(len(self.moveLog)!=0):
              move = self.moveLog.pop()
              self.board[move.startRow][move.startCol] = move.piceMoved
              self.board[move.endRow][move.endCol] = move.piceCaptured  
              self.whiteToMove = not self.whiteToMove
              if move.piceMoved == "wK":
                 self.whiteKing = (move.startRow,move.startCol)
              elif move.piceMoved == "bK":
                 self.blackKing = (move.startRow,move.startCol)  
    def getvalidMove(self):  
          
          kingDefance = self.inChake()
          
          print("hello")
          return self.getAllpossibleMove(kingDefance)
    def inChake(self):
          #single chake 
          self.chakeByPiece = []
          self.pinPiece = []
          dir = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(-1,-1),(1,-1)]
          for j in range(len(dir)):
               if j in range(0,4):
                    #chake by Rook or Queen
                    if self.whiteToMove:
                         z = 0
                         p = 0
                         for i in range(1,8):
                              
                              r = self.whiteKing[0] + (dir[j][0])*i
                              c = self.whiteKing[1] + (dir[j][1])*i
                              if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                                   if self.board[r][c][0] == "w":
                                        z =  z + 1
                                        self.pinPiece.append([self.board[r][c],r,c,dir[j]]) 
                                        print(len(self.pinPiece),dir[j],self.board[r][c],(self.pinPiece))    
                                        if len(self.pinPiece)>=2:
                                             z = z - 2
                                             if(self.pinPiece[len(self.pinPiece)-1][3])==(self.pinPiece[len(self.pinPiece)-2][3]):
                                                  del self.pinPiece[len(self.pinPiece)-2:len(self.pinPiece)]
                                                  self.chakeByPiece = []
                                                  break
                                            
                              if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                                   if self.board[r][c][0]=="b":
                                        if self.board[r][c] == "bR" or self.board[r][c] == "bQ":
                                             p = p+1
                                             self.chakeByPiece.append([self.board[r][c],r,c,dir[j]])
                                             print("bB",self.chakeByPiece)
                                             break
                                        else :
                                             break
                         if p==0:
                              for i in range(z):
                                   self.pinPiece.pop()
                                   

                                              
                    else:
                         z = 0
                         p = 0
                         for i in range(1,8):
                              
                              r = self.blackKing[0] + (dir[j][0])*i
                              c = self.blackKing[1] + (dir[j][1])*i
                              if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                                   if self.board[r][c][0] == "b":
                                        z =  z + 1
                                        self.pinPiece.append([self.board[r][c],r,c,dir[j]])
                                        print(len(self.pinPiece),dir[j],self.board[r][c],self.pinPiece)       
                                        if len(self.pinPiece)>=2:
                                             z = z - 2
                                             if(self.pinPiece[len(self.pinPiece)-1][3])==(self.pinPiece[len(self.pinPiece)-2][3]):
                                                  del self.pinPiece[len(self.pinPiece)-2:len(self.pinPiece)]
                                                  self.chakeByPiece = []
                                                  break
                              if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                                   if self.board[r][c][0]=="w":
                                        if self.board[r][c] == "wR" or self.board[r][c] == "wQ":
                                             p = p+1
                                             self.chakeByPiece.append([self.board[r][c],r,c,dir[j]])
                                             print("wB",self.chakeByPiece)
                                             break
                                        else :
                                             break
                         if p==0:
                              for i in range(z):
                                   self.pinPiece.pop()                                   
               if j>=4 and j<8:
                    #chake by Bishop or Queen
                    if self.whiteToMove:
                         z = 0
                         p = 0
                         for i in range(1,8):
                              
                              r = self.whiteKing[0] + (dir[j][0])*i
                              c = self.whiteKing[1] + (dir[j][1])*i
                              if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                                   if self.board[r][c][0] == "w":
                                        z =  z + 1
                                        self.pinPiece.append([self.board[r][c],r,c,dir[j]]) 
                                        print(len(self.pinPiece),dir[j],self.board[r][c],self.pinPiece)     
                                        if len(self.pinPiece)>=2:
                                             z = z - 2
                                             if(self.pinPiece[len(self.pinPiece)-1][3])==(self.pinPiece[len(self.pinPiece)-2][3]):
                                                  del self.pinPiece[len(self.pinPiece)-2:len(self.pinPiece)]
                                                  self.chakeByPiece = []
                                                  break
                              if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                                   if self.board[r][c][0]=="b":
                                        if self.board[r][c] == "bB" or self.board[r][c] == "bQ":
                                             p = p+1
                                             self.chakeByPiece.append([self.board[r][c],r,c,dir[j]])
                                             print("bB",self.chakeByPiece)
                                             break
                                        else :
                                             break
                         if p==0:
                              for i in range(z):
                                   self.pinPiece.pop()                

                    else:
                         z = 0
                         p = 0
                         for i in range(1,8):
                              r = self.blackKing[0] + (dir[j][0])*i
                              c = self.blackKing[1] + (dir[j][1])*i
                              if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                                   if self.board[r][c][0] == "b":
                                        z =  z + 1
                                        self.pinPiece.append([self.board[r][c],r,c,dir[j]])  
                                        print(len(self.pinPiece),dir[j],self.board[r][c],self.pinPiece)      
                                        if len(self.pinPiece)>=2:
                                             z = z - 2
                                             if(self.pinPiece[len(self.pinPiece)-1][3])==(self.pinPiece[len(self.pinPiece)-2][3]):
                                                  del self.pinPiece[len(self.pinPiece)-2:len(self.pinPiece)]
                                                  self.chakeByPiece = []
                                                  break
                              if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                                   if self.board[r][c][0]=="w":
                                        if self.board[r][c] == "wB" or self.board[r][c] == "wQ":
                                             p = p+1
                                             self.chakeByPiece.append([self.board[r][c],r,c,dir[j]])
                                             print("wB",self.chakeByPiece)
                                             break
                                        else :
                                             break
                         if p==0:
                              for i in range(z):
                                   self.pinPiece.pop()                    
          #chake by knigth
          if self.whiteToMove:
               c = self.whiteKing[1]
               r = self.whiteKing[0]
               if (r+2)<=7 and (c+1)<=7 and (self.board[r+2][c+1]== "bN") :
                   self.chakeByPiece.append([self.board[r+2][c+1],r+2,c+1,[0,0]])
               if (r+2)<=7 and (c-1)>=0 and (self.board[r+2][c-1]== "bN") :
                   self.chakeByPiece.append([self.board[r+2][c-1],r+2,c-1,[0,0]])   
               if (r-2)>=0 and (c+1)<=7 and (self.board[r-2][c+1]== "bN") :
                   self.chakeByPiece.append([self.board[r-2][c+1],r-2,c+1,[0,0]])
               if (r-2)>=0 and (c-1)>=0 and (self.board[r-2][c-1]== "bN") :
                   self.chakeByPiece.append([self.board[r-2][c-1],r-2,c-1,[0,0]])
               if (c+2)<=7 and (r+1)<=7 and (self.board[r+1][c+2]== "bN") :
                   self.chakeByPiece.append([self.board[r+1][c+2],r+1,c+2,[0,0]])
               if (c+2)<=7 and (r-1)>=0 and (self.board[r-1][c+2]== "bN") :
                   self.chakeByPiece.append([self.board[r-1][c+2],r-1,c+2,[0,0]])   
               if (c-2)>=0 and (r+1)<=7 and (self.board[r+1][c-2]== "bN") :
                   self.chakeByPiece.append([self.board[r+1][c-2],r+1,c-2,[0,0]]) 
               if (c-2)>=0 and (r-1)>=0 and (self.board[r-1][c-2]== "bN") :
                   self.chakeByPiece.append([self.board[r-1][c-2],r-1,c-2,[0,0]])       
          else :
               r = self.blackKing[0]
               c = self.blackKing[1]
               if (r+2)<=7 and (c+1)<=7 and (self.board[r+2][c+1]== "wN") :
                   self.chakeByPiece.append([self.board[r+2][c+1],r+2,c+1,[0,0]])
               if (r+2)<=7 and (c-1)>=0 and (self.board[r+2][c-1]== "wN") :
                   self.chakeByPiece.append([self.board[r+2][c-1],r+2,c-1,[0,0]])   
               if (r-2)>=0 and (c+1)<=7 and (self.board[r-2][c+1]== "wN") :
                   self.chakeByPiece.append([self.board[r-2][c+1],r-2,c+1,[0,0]])
               if (r-2)>=0 and (c-1)>=0 and (self.board[r-2][c-1]== "wN") :
                   self.chakeByPiece.append([self.board[r-2][c-1],r-2,c-1,[0,0]])
               if (c+2)<=7 and (r+1)<=7 and (self.board[r+1][c+2]== "wN") :
                   self.chakeByPiece.append([self.board[r+1][c+2],r+1,c+2,[0,0]])
               if (c+2)<=7 and (r-1)>=0 and (self.board[r-1][c+2]== "wN") :
                   self.chakeByPiece.append([self.board[r-1][c+2],r-1,c+2,[0,0]])   
               if (c-2)>=0 and (r+1)<=7 and (self.board[r+1][c-2]== "wN") :
                   self.chakeByPiece.append([self.board[r+1][c-2],r+1,c-2,[0,0]]) 
               if (c-2)>=0 and (r-1)>=0 and (self.board[r-1][c-2]== "wN") :
                   self.chakeByPiece.append([self.board[r-1][c-2],r-1,c-2,[0,0]])  

          print("<","final",">",self.chakeByPiece,"<","by pin ",">",self.pinPiece)
          r  = [self.pinPiece,self.chakeByPiece]
          if (len(self.chakeByPiece)>=1):
               return r
          else :
               return r                 

                    

    def getAllpossibleMove(self,kingdefance):
        moves  = []
        newMove = []
        for row in range(8):
             for col in range(8):
                  turn = self.board[row][col][0]
                  if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                       piece = self.board[row][col][1]
                       if piece == 'p':
                            self.getPawnMove(row,col,moves)
                       elif piece == 'R':     
                            self.getRookMove(row,col,moves)
                       elif piece == 'B':
                            self.getBishopMove(row,col,moves)
                       elif piece == 'N':
                            self.getKnightMove(row,col,moves)
                       elif piece == 'Q':
                            self.getQueenMove(row,col,moves)
                       if len(kingdefance[0])!=0:
                            for i in (kingdefance[0]):
                                 for j in (moves):
                                      if j.startRow == i[1] and j.startCol == i[2]:
                                           moves.remove(j)
                       if len(kingdefance[1])!=0:
                            if self.whiteToMove :
                                 for i in kingdefance[1]:
                                        for j in (moves):
                                             if ((self.whiteKing[0]-j.startCol)/abs(self.whiteKing[0]-j.startCol)!= i[3][0]) and (self.whiteKing[1]-j.startRow)/abs(self.whiteKing[1]-j.startRow)!= i[3][1] :
                                                  moves.remove(j)
                            else:
                                 for i in kingdefance[1]:
                                        for j in (moves):
                                             if ((self.blackKing[0]-j.startCol)/abs(self.blackKing[0]-j.startCol)!= i[3][0]) and (self.blackKing[1]-j.startRow)/abs(self.blackKing[1]-j.startRow)!= i[3][1] :
                                                  moves.remove(j)
                                                       


                                           
        return moves                    
    def getPawnMove(self,r,c,moves):
        if self.whiteToMove:
             if self.board[r-1][c] == "--":
                  moves.append(Move((r,c),(r-1,c),self.board))
                  if r == 6 and self.board[r-2][c] == "--":
                       moves.append(Move((r,c),(r-2,c),self.board))
             if c-1 >= 0 and r-1>=0 :
                  if self.board[r-1][c-1][0] == 'b':
                       moves.append(Move((r,c),(r-1,c-1),self.board))
             if c+1<=7 and r-1>=0:
                  if self.board[r+1][c+1][0] == 'b':
                       moves.append(Move((r,c),(r-1,c+1),self.board)) 

        else :
             if self.board[r+1][c] == "--":
                  moves.append(Move((r,c),(r+1,c),self.board))
                  if r == 1 and self.board[r+2][c] == "--":
                       moves.append(Move((r,c),(r+2,c),self.board))
             if c-1 >= 0 and r+1<=7 :
                  if self.board[r+1][c-1][0] == 'w':
                        moves.append(Move((r,c),(r+1,c-1),self.board))
             if c+1<=7 and r+1<=7:
                  if self.board[r+1][c+1][0] == 'w':
                       moves.append(Move((r,c),(r+1,c+1),self.board))
             
                       
             
    def getRookMove(self,row,col,moves):
         if self.whiteToMove:
               d = [(1,0),(0,1),(-1,0),(0,-1)]
               for j in range(len(d)):
                    for i in range(1,8):
                         r = row + (d[j][0])*i
                         c = col + (d[j][1])*i
                         if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                              if self.board[r][c][0] == 'b':
                                   moves.append(Move((row,col),(r,c),self.board))
                                   break
                              elif self.board[r][c][0] == 'w':
                                   break
                              elif self.board[r][c] == "--":
                                   moves.append(Move((row,col),(r,c),self.board))

                                  
         else :
               d = [(1,0),(0,1),(-1,0),(0,-1)]
               for j in range(len(d)):
                    for i in range(1,8):
                         r = row + (d[j][0])*i
                         c = col + (d[j][1])*i
                         if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                              if self.board[r][c][0] == 'w':
                                   moves.append(Move((row,col),(r,c),self.board))
                                   break
                              elif self.board[r][c][0] == 'b':
                                   break
                              elif self.board[r][c] == "--":
                                   moves.append(Move((row,col),(r,c),self.board))
                                 
    def getBishopMove(self,row,col,moves):
          if self.whiteToMove:
               d = [(1,1),(-1,1),(-1,-1),(1,-1)]
               for j in range(len(d)):
                    for i in range(1,8):
                         r = row + (d[j][0])*i
                         c = col + (d[j][1])*i
                         if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                              if self.board[r][c][0] == 'b':
                                   moves.append(Move((row,col),(r,c),self.board))
                                   break
                              elif self.board[r][c][0] == 'w':
                                   break
                              elif self.board[r][c] == "--":
                                   moves.append(Move((row,col),(r,c),self.board))
          else :
               d = [(1,1),(-1,1),(-1,-1),(1,-1)]
               for j in range(len(d)):
                    for i in range(1,8):
                         r = row + (d[j][0])*i
                         c = col + (d[j][1])*i
                         if ((r>=0) and (r<=7)) and ((c>=0) and (c<=7)):
                              if self.board[r][c][0] == 'w':
                                   moves.append(Move((row,col),(r,c),self.board))
                                   break
                              elif self.board[r][c][0] == 'b':
                                   break
                              elif self.board[r][c] == "--":
                                   moves.append(Move((row,col),(r,c),self.board))



    def getKnightMove(self,row,col,moves):
          if self.whiteToMove:
               r = row
               c = col
               if (r+2)<=7 and (c+1)<=7 and (self.board[r+2][c+1] == "--" or self.board[r+2][c+1][0]== "b") :
                   moves.append(Move((r,c),(r+2,c+1),self.board))
               if (r+2)<=7 and (c-1)>=0 and (self.board[r+2][c-1] == "--" or self.board[r+2][c-1][0]== "b") :
                   moves.append(Move((r,c),(r+2,c-1),self.board))    
               if (r-2)>=0 and (c+1)<=7 and (self.board[r-2][c+1] == "--" or self.board[r-2][c+1][0]== "b") :
                   moves.append(Move((r,c),(r-2,c+1),self.board))
               if (r-2)>=0 and (c-1)>=0 and (self.board[r-2][c-1] == "--" or self.board[r-2][c-1][0]== "b") :
                   moves.append(Move((r,c),(r-2,c-1),self.board)) 
               if (c+2)<=7 and (r+1)<=7 and (self.board[r+1][c+2] == "--" or self.board[r+1][c+2][0]== "b") :
                   moves.append(Move((r,c),(r+1,c+2),self.board))
               if (c+2)<=7 and (r-1)>=0 and (self.board[r-1][c+2] == "--" or self.board[r-1][c+2][0]== "b") :
                   moves.append(Move((r,c),(r-1,c+2),self.board))    
               if (c-2)>=0 and (r+1)<=7 and (self.board[r+1][c-2] == "--" or self.board[r+1][c-2][0]== "b") :
                   moves.append(Move((r,c),(r+1,c-2),self.board))
               if (c-2)>=0 and (r-1)>=0 and (self.board[r-1][c-2] == "--" or self.board[r-1][c-2][0]== "b") :
                   moves.append(Move((r,c),(r-1,c-2),self.board))       
          else :
               r = row
               c = col
               if (r+2)<=7 and (c+1)<=7 and (self.board[r+2][c+1] == "--" or self.board[r+2][c+1][0]== "w") :
                   moves.append(Move((r,c),(r+2,c+1),self.board))
               if (r+2)<=7 and (c-1)>=0 and (self.board[r+2][c-1] == "--" or self.board[r+2][c-1][0]== "w") :
                   moves.append(Move((r,c),(r+2,c-1),self.board))    
               if (r-2)>=0 and (c+1)<=7 and (self.board[r-2][c+1] == "--" or self.board[r-2][c+1][0]== "w") :
                   moves.append(Move((r,c),(r-2,c+1),self.board))
               if (r-2)>=0 and (c-1)>=0 and (self.board[r-2][c-1] == "--" or self.board[r-2][c-1][0]== "w") :
                   moves.append(Move((r,c),(r-2,c-1),self.board)) 
               if (c+2)<=7 and (r+1)<=7 and (self.board[r+1][c+2] == "--" or self.board[r+1][c+2][0]== "w") :
                   moves.append(Move((r,c),(r+1,c+2),self.board))
               if (c+2)<=7 and (r-1)>=0 and (self.board[r-1][c+2] == "--" or self.board[r-1][c+2][0]== "w") :
                   moves.append(Move((r,c),(r-1,c+2),self.board))    
               if (c-2)>=0 and (r+1)<=7 and (self.board[r+1][c-2] == "--" or self.board[r+1][c-2][0]== "w") :
                   moves.append(Move((r,c),(r+1,c-2),self.board))
               if (c-2)>=0 and (r-1)>=0 and (self.board[r-1][c-2] == "--" or self.board[r-1][c-2][0]== "w") :
                   moves.append(Move((r,c),(r-1,c-2),self.board)) 
                   
    def getQueenMove(self,row,col,moves):
         if self.whiteToMove:
              self.getRookMove(row,col,moves)
              self.getBishopMove(row,col,moves)
         else:
              self.getRookMove(row,col,moves)
              self.getBishopMove(row,col,moves)    

              

class Move():

    ranksToRows = {"1":7,"2":6,"3":5,"4":4,"5":3,"6":2,"7":1,"8":0}
    rowToRanks = {v:k for k , v in ranksToRows.items()}
    filesToCols  = {
        "a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7
    }
    colsTofiles = {v:k for k,v in filesToCols.items()}

    def __eq__(self,other):
         if isinstance(other,Move):
              return self.moveID == other.moveID
         return False
              
         

    def __init__(self,startSq,endSq,board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.piceMoved = board[self.startRow][self.startCol]
        self.piceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow*1000 + self.startCol*100 + self.endRow*10 + self.endCol
        print(self.moveID)
        

    def getChessNotation(self):
        return self.getRankFile(self.startRow,self.startCol)+self.getRankFile(self.endRow,self.startCol)

    def getRankFile(self,r,c):
        return self.colsTofiles[c]+self.rowToRanks[r]    
        