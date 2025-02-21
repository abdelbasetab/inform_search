import heapq
import argparse

class Node:
    def __init__(self, state, parent, action, depth=0):
        self.state = state      # (row, col)
        self.parent = parent    # Referenz zum Vorgängerknoten
        self.action = action    # Die Aktion, die zu diesem Zustand geführt hat
        self.depth = depth      # Kosten bis zu diesem Knoten (g)

class AStarFrontier:
    """
    Implementiert eine Prioritätswarteschlange (min-heap) für A*-Search.
    Die Priorität eines Knotens berechnet sich als: f = g + h,
    wobei g = node.depth und h die Heuristikfunktion ist.
    """
    def __init__(self, heuristic):
        self.frontier = []
        self.heuristic = heuristic  # Funktion, die h(n) für einen Zustand n berechnet
        self.counter = 0            # Hilfszähler, um bei gleichen Prioritäten die Reihenfolge zu wahren

    def add(self, node):
        # Berechne f = g + h
        f = node.depth + self.heuristic(node.state)
        heapq.heappush(self.frontier, (f, self.counter, node))
        self.counter += 1

    def contains_state(self, state):
        return any(item[2].state == state for item in self.frontier)

    def empty(self):
        return len(self.frontier) == 0

    def remove(self):
        if self.empty():
            raise Exception("empty frontier")
        else:
            _, _, node = heapq.heappop(self.frontier)
        return node

class Maze:
    def __init__(self, filename):
        with open(filename) as f:
            contents = f.read()

        if contents.count("A") != 1:
            raise Exception("Das Labyrinth muss genau einen Startpunkt (A) haben.")
        if contents.count("B") != 1:
            raise Exception("Das Labyrinth muss genau einen Zielpunkt (B) haben.")

        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # Erstelle eine Liste, die angibt, ob es sich bei einer Zelle um eine Wand handelt (True) oder nicht (False)
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i, j)
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i, j)
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
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(".", end="")
            print()
        print()

    def neighbors(self, state):
        row, col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]

        result = []
        for action, (r, c) in candidates:
            try:
                if not self.walls[r][c]:
                    result.append((action, (r, c)))
            except IndexError:
                continue
        return result

    def heuristic(self, state):
        """
        Berechnet den Manhattan-Abstand von 'state' zum Ziel.
        """
        row, col = state
        goal_row, goal_col = self.goal
        return abs(row - goal_row) + abs(col - goal_col)
    


    

    def solve_astar(self):
        """
        Löse das Labyrinth mit dem A*-Algorithmus.
        """
        self.num_explored = 0
        start = Node(state=self.start, parent=None, action=None, depth=0)
        frontier = AStarFrontier(self.heuristic)
        frontier.add(start)
        self.explored = {}  # Speichert die geringsten Kosten (depth) für jeden Zustand

        while not frontier.empty():
            node = frontier.remove()
            self.num_explored += 1

            # Zieltest
            if node.state == self.goal:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return

            # Falls dieser Zustand noch nicht erkundet wurde oder ein günstigerer Pfad gefunden wurde:
            if node.state not in self.explored or node.depth < self.explored[node.state]:
                self.explored[node.state] = node.depth

                for action, state in self.neighbors(node.state):
                    child = Node(state=state, parent=node, action=action, depth=node.depth + 1)
                    frontier.add(child)

        raise Exception("Keine Lösung gefunden.")

def main():
    parser = argparse.ArgumentParser(description="Löse ein Labyrinth mit A* Search.")
    parser.add_argument("filename", help="Die Datei, die das Labyrinth enthält.")
    args = parser.parse_args()

    maze = Maze(args.filename)
    print("Löse das Labyrinth mit A* Search...")
    maze.solve_astar()
    print("Lösung gefunden!")
    maze.print()

    print("Aktionen zum Lösen des Labyrinths:")
    for step, action in enumerate(maze.solution[0], start=1):
        print(f"Schritt {step}: {action}")
    print("Pfadkoordinaten:")
    for step, cell in enumerate(maze.solution[1], start=1):
        print(f"Schritt {step}: {cell}")

if __name__ == "__main__":
    main()