import chess,mstc
import numpy as np
import copy
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import os

class GenrateMove:

    def __init__(self) -> None:
        self.games= chess.GameState()
        self.Evaluate = Evaluate()

    def trains(self,gs):
        games = copy.deepcopy(gs)
        node = mstc.Node(games)
        next_node = node.start(100)

        for i in range(5):

            for _ in range(5):
                if next_node == None:
                    break
                next_node = next_node.start(100)

            next_node = node
        
        next_node = node.start(100)

        if node == None:
            print("error")
        print("rewards : ",next_node.rewards)
        print("probs : ",self.Evaluate.evaluate(next_node.gs))
        return next_node.action
        
        


    
    def genrate_move(self,gameState,moves,train):
        self.games = gameState
        gs = self.games
        turn = 0 if gs.white_to_move else 1
        move = np.random.choice(moves)
        gs.makeMove(move)
        score = self.Evaluate.evaluate(gs)
        gs.undoMove()
        good_move = move
        # print("*")
        # print(turn)
        # print("*\n")
        if not train:
            for  m in moves:
                gs.makeMove(m)
                print(gs.board)
                print("\n\n")
                temp = self.Evaluate.evaluate(gs)
                print(temp)
                gs.undoMove()

                if (pow(-1,turn))*temp > (pow(-1,turn))*score:
                    good_move = m
                    score = temp
            
        else:
            good_move = self.trains(gs)

        #print("Score %d"%score)
        return good_move
    
    def getpiece(self, gameState):
        self.games = gameState
        gs = self.games
        board = gs.board
        n_piece = 0
        for i in range(len(board)):
            for j in range(len(board[0])):
                piece = board[i][j]
                if piece != "--":
                    n_piece = n_piece + 1
        return n_piece



        
class ChessBot(nn.Module):
    def __init__(self):
        super(ChessBot, self).__init__()
        # Define convolutional layers
        self.conv0 = nn.Conv2d(in_channels=1, out_channels=16, kernel_size=1)
        self.conv1 = nn.Conv2d(in_channels=16, out_channels=64, kernel_size=5)
        self.conv2 = nn.Conv2d(in_channels=64, out_channels=128, kernel_size=3)
        self.conv3 = nn.Conv2d(in_channels=128, out_channels=512, kernel_size=2)

        self.bn1 = nn.BatchNorm2d(64)
        self.bn2 = nn.BatchNorm2d(128)

        self.relu = nn.ReLU(inplace=True)

        # Define fully connected layers
        self.fc1 = nn.Linear(512, 256)
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128,1)

        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        
        x = self.conv0(x)
        x = self.relu(x)

        x = self.conv1(x)
        x = self.bn1(x)
        x = self.relu(x)

        x = self.conv2(x)
        x = self.bn2(x)
        x = self.relu(x)

        x = self.conv3(x)


        x = x.view(x.size(0), -1)

        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)

        x = self.sigmoid(x)
        return x


class Evaluate():

    def __init__(self) -> None:
        self.model = ChessBot()
        if os.path.exists('chessbot.pth'):
            # Load the saved model weights
            checkpoint = torch.load('chessbot.pth')
            self.model.load_state_dict(checkpoint)
            #print("Loaded model weights from disk")


    def evaluate(self, gameState):
        encoding_table = {'bp':-1,'bR':-8,'wR':8,'bB':-7,'wB':7,'bN':-7,'wN':7,'bQ':-9,'wQ':9,'bK':-10,'wK':10,'wp':1,'--':0}
        new_data = []
        board = gameState.board
 
        encoded_board = [[encoding_table[piece] for piece in row] for row in board]

        new_data = np.array(encoded_board)
        input_data = torch.tensor(new_data).float()
        input_data = input_data.view(1, 1, 8, 8)
        pridiction = self.model(input_data)
        return pridiction.item()
    


class  train():
    def getscore(self, gameState,win,data):
        encoding_table = {'bp':-1,'bR':-8,'wR':8,'bB':-7,'wB':7,'bN':-7,'wN':7,'bQ':-9,'wQ':9,'bK':-10,'wK':10,'wp':1,'--':0,'-':0}
        new_data = []
        target = []
        batch_size = 32
        shuffle = True

        for batch in data:
            inputs, targets = batch
            encoded_board = [[encoding_table[piece] for piece in row] for row in inputs]
            target.append(targets)
            new_data.append(encoded_board)

        

        X_train, X_test, y_train, y_test = train_test_split(new_data, target, test_size=0.1, random_state=42)
        model = ChessBot()

        if os.path.exists('chessbot.pth'):
            # Load the saved model weights
            checkpoint = torch.load('chessbot.pth')
            model.load_state_dict(checkpoint)
            print("Loaded model weights from disk")

        criterion = nn.MSELoss()
        optimizer = optim.Adam(model.parameters(), lr=0.001)


        for i in range(0,len(X_train),batch_size):
            inputs = X_train[i:i+batch_size]
            targets = y_train[i:i+batch_size]
            model.train()
            run_loss = 0
            print("train")
            optimizer.zero_grad()
            input_data = torch.tensor(inputs).float()
            targets = torch.tensor(targets).float()
            targets = targets.view(-1, 1) 
            input_data = input_data.view(-1, 1, 8, 8)
            output = model(input_data)
            loss = criterion(output,targets)
            loss.backward()
            optimizer.step()

            print("LOSS",loss.item())


        torch.save(model.state_dict(), 'chessbot.pth')
