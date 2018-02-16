from random import randint

class Node(object):
    
    def __init__(self, b, move, color):
    
        self.board = b
        self.heurs = 0
        self.move = move
        self.color = color
        self.children = []
        self.start = [0, 3, 18, 21]

    def getChildren(self, np = 'W', p = 'B'):
        
        self.children = []
        if self.color == 'W': np, p = 'B', 'W'

        if not self.checkWin(p) and not self.checkWin(np):
            for grid in range(4):
                for tile in range(9):
                    if self.getTile(grid, tile) == '-':
                        for rgrid in range(4):
                            lm = '{0}/{1} {2}l'.format(grid+1, tile+1, rgrid+1)
                            rm = '{0}/{1} {2}r'.format(grid+1, tile+1, rgrid+1)
                            lNode = Node(self.board[:], lm, np)
                            rNode = Node(self.board[:], rm, np)
                            lNode.setTile(grid, tile, np)
                            rNode.setTile(grid, tile, np)
                            lNode.rotate(rgrid, 'l')
                            rNode.rotate(rgrid, 'r')
                            self.children.extend([lNode, rNode])
    
    def getHeuristic(self, p = 'B', np = 'W', h = 0):
        
        if self.checkWin(p): return float('inf')
        if self.checkWin(np): return float('-inf')

        for i in range(32):
            row, col = i/6, i%6
            if col < 2:
                if self.board[i:i+5].count(np) == 0: 
                    h += (1 + (self.board[i:i+5].count(p)**4))
                if self.board[i:i+5].count(p) == 0: 
                    h -= (1 + (self.board[i:i+5].count(np)**4))
            if row < 2:
                if self.board[i:i+30:6].count(np) == 0: 
                    h += (1 + (self.board[i:i+30:6].count(p)**4))
                if self.board[i:i+30:6].count(p) == 0: 
                    h -= (1 + (self.board[i:i+30:6].count(np)**4))
                if col < 2:
                    if self.board[i:i+35:7].count(np) == 0: 
                        h += (1 + (self.board[i:i+35:7].count(p)**4))
                    if self.board[i:i+35:7].count(p) == 0: 
                        h -= (1 + (self.board[i:i+35:7].count(np)**4))
                if col > 3:
                    if self.board[i:i+25:5].count(np) == 0: 
                        h += (1 + (self.board[i:i+25:5].count(p)**4))
                    if self.board[i:i+25:5].count(p) == 0: 
                        h -= (1 + (self.board[i:i+25:5].count(np)**4))

        return h
    
    def checkWin(self, p):
    
        for i in range(32):
            row, col = i/6, i%6
            if col < 2 and self.board[i:i+5].count(p) == 5: return True
            if row < 2:
                if self.board[i:i+30:6].count(p) == 5: return True
                if col < 2 and self.board[i:i+35:7].count(p) == 5: return True
                if col > 3 and self.board[i:i+25:5].count(p) == 5: return True
        
        return False

    def getTile(self, grid, tile):
            
        return self.board[self.start[grid] + 2*tile - tile%3]

    def setTile(self, grid, tile, color):

        self.board[self.start[grid] + 2*tile - tile%3] = color

    def rotate(self, grid, dir):

        count, tempBoard = 2, self.board[:]

        for j in range(self.start[grid], self.start[grid]+18, 6):
            idx = self.start[grid] + count
            if dir == 'l': self.board[j:j+3] = tempBoard[idx:idx+18:6]
            else: self.board[idx:idx+18:6] = tempBoard[j:j+3]
            count -= 1

class Pentago(object):

    def __init__(self):

        self.depth = 2
        self.moves = []
        self.AInext = None
        self.AI = randint(0,1)
        self.color = ['W', 'B']
        self.start = [0, 3, 18, 21]
        self.curr = Node(list('-'*36), None, 'W')
        self.names = ['Whitewalkers', 'Night\'s Watch']
        self.outFile = open('Output.txt', 'w')

        r = 0

        self.outFile.write('-------------------------\n'
                           + '---------PENTAGO---------')

        while '-' in self.curr.board:
            
            self.printBoard(self.curr.board, r)
            self.curr.color = self.color[r%2]
            self.getMove(self.color[r%2], r%2 == self.AI)
            self.moves.append((self.curr.color, self.curr.move))
            if self.curr.checkWin(self.color[r%2]): break  

            r += 1

        self.printBoard(self.curr.board, r)
        self.printWin()
        self.outFile.close()

    def getMove(self, player, AI):
        
        self.curr.player = player
        self.curr.children = []
        
        if AI:
            print('AI is thinking...')
            move = self.alphaBeta(self.curr, self.depth, True)[1]
        else: move = raw_input('Enter your move ' + player + ': ').lower()
        
        try:
            self.curr.move = move
            rotDir = move[5]
            grid = int(move[0]) - 1
            tile = int(move[2]) - 1
            rotGrid = int(move[4]) - 1

            if self.curr.getTile(grid, tile) == '-':   
                self.curr.setTile(grid, tile, player)
                if self.curr.checkWin(player): return
                self.curr.rotate(rotGrid, rotDir)
            else: 
                print('That tile is already occupied.')
                self.getMove(player, AI)
        except:
            move = ''
            print('Incorrect input.')
            self.getMove(player, AI)

    def alphaBeta(self, node, d, mx, a=float('-inf'), b=float('inf')):
        
        move = ''
        
        if d > 0: node.getChildren()
        if d == 0 or len(node.children) == 0:
            return node.getHeuristic(), None

        if mx:
            v = float('-inf')
            for child in node.children:
                m = self.alphaBeta(child, d-1, False, a, b)[0]
                if m > v: v, move = m, child.move
                a = max(a, v)
                if b <= a: break # a cut-off
            return v, move
        else:
            v = float('inf')
            for child in node.children:
                v = min(v, self.alphaBeta(child, d-1, True, a, b)[0])
                b = min(b, v)
                if b <= a: break # b cut-off
            return v, move

    def minMax(self, node, d, mx):
        
        move = ''
        
        if d > 0: node.getChildren()
        if d == 0 or len(node.children) == 0:
            return node.getHeuristic(), None

        if mx:
            v = float('-inf')
            for child in node.children:
                m = self.minMax(child, d-1, False)[0]
                if m > v: v, move = m, child.move
            return v, move
        else:
            v = float('inf')
            for child in node.children:
                v = min(v, self.minMax(child, d-1, True)[0])
            return v, move

    def printWin(self):

        if self.curr.checkWin('W'):
            if self.curr.checkWin('B'):
                out = '\nThis game ends in a tie!'
            else: out = '\nGame over, White Walkers win!'
        elif self.curr.checkWin('B'):
                out = '\nGame over, Night\'s Watch wins!'
        else: out = '\nThis game ends in a tie! Neither player wins.'

        print(out)
        self.outFile.write('\n' + out)
                
    def printBoard(self, b, r):
        
        out = ('\n-------------------------\n'
            + '\nP1: {0} - {1}'.format(self.names[0], self.color[0])
            + '\nP2: {0} - {1}'.format(self.names[1], self.color[1])
            + '\n\nNext: P{0}'.format((r%2) + 1)
            + '\n+-------+-------+')
            
        for j in range(0, 36, 6):
            l = ' '.join(b[j:j+3])
            r = ' '.join(b[j+3:j+6])
            out += '\n| {0} | {1} |'.format(l, r)
            if j == 12: out += '\n+-------+-------+'
            
        out += '\n+-------+-------+\n'
        for m in self.moves: out += '\n' + m[0] + ' - ' + m[1]

        print(out)
        self.outFile.write(out)

if __name__ == '__main__':
    Pentago()
