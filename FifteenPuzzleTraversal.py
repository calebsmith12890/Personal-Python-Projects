import sys

class Node(object):

    # Initialize a node to be used in the tree.
    def __init__(self, depth, value):
        
        self.up = None
        self.down = None
        self.left = None
        self.right = None
        self.depth = depth
        self.value = value

    # Find all valid moves from current state.
    def validMoves(self):

        index = self.value.find(' ')
        row = index // 4
        col = index % 4

        # Set children for every direction the space can move.
        if row > 0: self.up = Node(self.depth + 1, self.swap(index, index - 4))
        if row < 3: self.down = Node(self.depth + 1, self.swap(index, index + 4))
        if col > 0: self.left = Node(self.depth + 1, self.swap(index, index - 1))
        if col < 3: self.right = Node(self.depth + 1, self.swap(index, index + 1))

    # Swap empty space with neighbor tile.
    def swap(self, index, move):

        newState = list(self.value)
        newState[index] = newState[move]
        newState[move] = ' '

        return ''.join(newState)

class Tree(object):

    # Initialize Tree to be searched.
    def __init__(self, h = 0):

        # Heuristic dictionary.
        heurs = {'h1':self.H1,
                 'h2':self.H2}

        # Function dictionary.
        funcs = {'dls':'limit',
                 'bfs':self.BFS,
                 'dfs':self.DFS,
                 'gbfs':self.Greedy,
                 'astar':self.Astar}

        # Possible goal states.
        self.goal = ['123456789abcdef ',
                     '123456789abcdfe ']

        # Added command line arguments.
        if len(sys.argv) > 1:
            
            initial, search = sys.argv[1], sys.argv[2].lower()

            if len(sys.argv) > 3:
                if search == 'dls': h = int(sys.argv[3])
                else: h = heurs[sys.argv[3].lower()]

        # Don't know how to test command line. Added input option.
        else:
            initial = input('Enter the initial state of the puzzle board.\nCombination of "123456789abcdef ": ')
            search = input('Enter the search method you want to use.\nEither DFS, BFS, DLS, GBFS, or AStar: ').lower()

            if search == 'dls':
                h = int(input('Choose a depth level to search to: '))

            elif search in ('gbfs', 'astar'):
                h = heurs[input('Choose a heuristic, H1 or H2: ').lower()]
            
        self.Search(funcs[search], Node(0, initial), self.goal, h)

    # Polymorphic Search function.
    def Search(self, funct, curr, goal, h):
        
        visited, fringe = [], []
        limit, maxFringe, created = False, 0, 1

        # If DLS selected, set function to DFS and bool to True.
        if funct == 'limit': limit, funct = True, self.DFS

        # Search until goal state is found.
        while curr.value not in goal:

            # Set current node as last in fringe if not visited before.
            while curr.value in visited: curr = fringe.pop()[1]

            curr.validMoves()
            
            children = [curr.up, curr.left, curr.down, curr.right]

            # Add each child to fringe.
            for child in children:
                if child is not None:
                    created += 1
                    funct(fringe, child, h)
            
            visited.append(curr.value)
            fringe.sort(key = lambda x: x[0], reverse = True)
  
            if len(fringe) > maxFringe: maxFringe = len(fringe)
            if (limit and fringe[-1][1].depth > h) or len(fringe) is 0: break

        created = len(fringe) + len(visited)
        depth = (lambda: curr.depth if curr.value in goal else -1)()

        print('Depth: {}\nNodes Created: {}\nNodes Visited: {}\nMax Nodes: {}'
                .format(depth, created, len(visited), maxFringe))

    # Variation for adding child in Depth First Search.
    def DFS(self, fringe, child, h):

        return fringe.append((0, child))

    # Variation for adding child in Breadth First Search.
    def BFS(self, fringe, child, h):

        return fringe.insert(0, (0, child))

    # Variation for adding child in Greedy Search.
    def Greedy(self, fringe, child, h):

        return fringe.append((h(child.value), child))
    
    # Variation for adding child in A* Search.
    def Astar(self, fringe, child, h):

        return fringe.append((self.H1(child.value) + self.H2(child.value), child))

    # Heuristic to count tiles in correct positions.
    def H1(self, value):

        return sum(c1 != c2 for c1, c2 in zip(value, self.goal[0]))

    # Heuristic to sum manhatten distance of all tiles.
    def H2(self, value):

        s, goal = 0, self.goal[0]

        for c in value:
            
            s += abs((value.find(c) % 4) - (goal.find(c) % 4))
            s += abs((value.find(c) // 4) - (goal.find(c) // 4))

        return s

if __name__ == '__main__':
    Tree()
