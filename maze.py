class Node:

    def __init__(self, state, parent, action) :
        self.state = state
        self.parent = parent
        self.action = action


# class for DFS 
class StackFrontier():
    def __init__(self):
         self.frontier = []


    def add(self, node):
         self.frontier.append(node)
    

    def contains_state(self, state):
         return any(node.state == state for node in self.frontier)

    def empty(self):
         return len(self.frontier) == 0
    

    def remove(self):
         if self.empty():
             raise Exception("empty frontier")
        
         else:
             node = self.frontier[-1] # last node 
             self.frontier = self.frontier[:-1] # delete the last one 
         return node


# class for BFS
class QueueFrontier(StackFrontier):

  # the only deference from Stack is this methode

    def remove(self):
         if self.empty():
             raise Exception("empty frontier")
         else:
             node = self.frontier[0] # first node 
             self.frontier = self.frontier[1:] # delete the last one 
         return node
  





class Maze():

    def __init__(self, filename):
        
         with open(filename) as f:
             contents = f.read()


             if contents.count("A") != 1:
                 raise Exception("maze must have exactly one start point")

             if contents.count("B") != 1:
                 raise Exception("maze must have exactly one goal")

             contents = contents.splitlines()

             self.height = len(contents)
             self.width = max(len(line) for line in contents)


             # keep track the walls
             self.walls = []
             for i in range(self.height):
                 row = []
                 for j in range(self.width):
                     try:
                        if contents[i][j] == "A":
                            self.start =(i,j)
                            row.append(False)
                        elif contents[i][j] == "B":
                            self.goal =(i,j)
                            row.append(False)
                        elif contents[i][j] == " ":
                            row.append(False)
                        else:
                            row.append(True)
                     except IndexError:
                        row.append(False)
                 self.walls.append(row)

             self.solution = None

    
    def print(self):
      
        solution = self.solution[1] if self.solution is not None else None

        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("#", end="")
                elif (i, j) == self.start:
                    print("A",end="")
                elif (i, j) == self.goal:
                    print("B",end="")
                elif solution is not None and  (i, j) in solution:
                    print("*",end="")
                else:
                    print(".", end="")
            print()
        print()


    def neighbors(self, state):
        row, col = state
        condidates = [
            ("up",(row - 1, col)),
            ("down",(row + 1, col)),
            ("left",(row, col - 1)),
            ("right",(row , col + 1))
        ]

        # ensure actions are valid
        result = []

        for action, (r, c) in condidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result
    

    def solve(self):

        # keep track of number of states explored
        self.num_explored = 0

        # Initialize frontier to just the starting position
        start = Node(state=self.start, parent=None, action=None)
        frontier = StackFrontier() # this for DFS
        #frontier = QueueFrontier() # this for BFS
        frontier.add(start)


        # Initialze an empty explored set
        self.explored = set()

        # keep looping until solution found

        while True:
            # if nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")
            
            # choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1

            # if node is the goal, the we have a solution
            if node.state == self.goal:
                actions = []
                cells = []

                # back track to know what actions i took
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells) 

                return
            
            # if is not the goal
            self.explored.add(node.state)

            # add neighbors tor frontier

            for action, state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state= state, parent=node, action=action)
                    frontier.add(child)





import argparse

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Solve a maze.")
    parser.add_argument("filename", help="The file containing the maze to solve.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Instantiate the Maze class with the provided filename
    maze = Maze(args.filename)
    
    # Solve the maze
    print("Solving the maze...")
    maze.solve()
    
    # Print the solution
    print("Solution found!")
    maze.print()

    # Print the list of actions:
    print("State Explored: ", maze.num_explored)



    #for step, action in enumerate(maze.solution[0], start=1):
     #   print(f"Step {step}: {action}")
    

if __name__ == "__main__":
    main()