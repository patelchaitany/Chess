import numpy as np
import chess,chess_AI
import random

class Node():
    def __init__(self,gs):
         self.parent = None
         self.children = []
         self.rewards = 0
         self.visited = 0
         self.gs = gs
         self.done = False
         self.action = None

    def simulation(self,depth):
        ans = 0.5
        pridictor = chess_AI.Evaluate()
        z = 0
        if len(self.gs.getValidMoves()) == 0: #if the game is over
            ans = 0 if self.gs.white_to_move else 1

        for i in range(depth):
            z = z + 1
            moves = self.gs.getValidMoves()
            if len(moves) == 0:
                break
            move = np.random.choice(moves)
            self.gs.makeMove(move)

        if  len(self.gs.getValidMoves()) == 0: #if the game is over
            ans = 0 if self.gs.white_to_move else 1
        else:
            ans = pridictor.evaluate(self.gs)/(self.visited+1)

        for _ in range(z):
            self.gs.undoMove()
        
        return ans


    def cal(self,c):
        next_child = None
        max = -np.inf 
        min = np.inf  
        self.rewards = 0
        if self.gs.white_to_move:
            for i in self.children:
                if i.visited == 0:
                    i.rewards+=i.simulation(100)
                if max <(i.rewards + c*np.sqrt(np.log(self.visited)/(i.visited+1))):
                    next_child = i
                    max = i.rewards + c*np.sqrt(np.log(self.visited)/(i.visited+1))
                self.rewards = self.rewards + i.rewards
        else :
            for i in self.children:
                if i.visited == 0:
                    i.rewards+=i.simulation(100)
                if min > (i.rewards + c*np.sqrt(np.log(self.visited)/(i.visited+1))):
                    next_child = i
                    min = i.rewards + c*np.sqrt(np.log(self.visited)/(i.visited+1))
                self.rewards = self.rewards + i.rewards
            return min,next_child
        
        return max,next_child


    def add(self):

        if self.visited == 0:
            self.visited = self.visited + 1
            moves = self.gs.getValidMoves()
            if len(moves) == 0:
                self.done = True
                return
            for i in moves:
                self.gs.makeMove(i)
                self.children.append(Node(self.gs))
                self.children[len(self.children)-1].action = i
                self.children[len(self.children)-1].parent = self
                self.gs.undoMove()
        else:
            self.visited = self.visited + 1

    def update(self, reward):
        current = self
        while current!= None:
            current.rewards += (0.01)*reward
            current.visited+=1
            current = current.parent

    def start(self, depth):
        next_child = None
        reward = None
        self.add()

        if self.done:
            return None
        
        reward,next_child = self.cal(1)
        self.update(reward=reward)
        return next_child