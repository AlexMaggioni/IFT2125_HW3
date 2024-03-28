import random
import sys

cell_size = 10  # Taille d'une cellule en mm
wall_height = 10  # Hauteur d'un mur en mm
wall_thickness = 1  # Épaisseur d'un mur en mm

class Strategy:
    def Apply(self):
        pass

    def DoSomething(self):
        pass
# Le code ici je l'ai pris sur ce lien : 
# https://artofproblemsolving.com/community/c3090h2221709_wilsons_maze_generator_implementation
# J'ai trouvé ce lien qui est aussi intéressant parce qu'il faut vraiment gérer c'est l'orientation des murs : https://weblog.jamisbuck.org/2011/1/20/maze-generation-wilson-s-algorithm 
class WilsonMazeGenerator(Strategy):
    """Maze Generator using Wilson's Loop Erased Random Walk Algorithm"""

    def __init__(self,height,width):
        """WilsonMazeGenerator(int,int) -> WilsonMazeGenerator
        Creates a maze generator with specified width and height.
        width: width of generated mazes
        height: height of generated mazes"""        
        self.width = 2*(width//2) + 1   # Make width odd
        self.height = 2*(height//2) + 1 # Make height odd

        # grid of cells
        self.grid = [[0 for j in range(self.width)] for i in range(self.height)]

        # declare instance variable
        self.visited = []    # visited cells
        self.unvisited = []  # unvisited cells
        self.path = dict()   # random walk path

        # valid directions in random walk
        self.directions = [(0,1),(1,0),(0,-1),(-1,0)]

        # indicates whether a maze is generated
        self.generated = False

        # shortest solution
        self.solution = []
        self.showSolution = False
        self.start = (self.height-1,0)
        self.end = (0,self.width-1)

    def __str__(self):
        """WilsonMazeGenerator.__str__() -> str
        outputs a string version of the grid"""
        out = "##"*(self.width+1)+"\n"
        for i in range(self.height):
            out += "#"
            for j in range(self.width):
                if self.grid[i][j] == 0:
                    out += "##"
                else:
                    if not self.showSolution:
                        out += "  "
                    elif (i,j) in self.solution:
                        out += "**"
                    else:
                        out += "  "
            out += "#\n"
        return out + "##"*(self.width+1)

    def get_grid(self):
        """WilsonMazeGenerator.get_grid() -> list
        returns the maze grid"""
        return self.grid

    def get_solution(self):
        """WilsonMazeGenerator.get_solution() -> list
        Returns the solution to the maze as a list
        of tuples"""
        return self.solution

    def show_solution(self,show):
        """WilsonMazeGenerator.show_solution(boolean) -> None
        Set whether WilsonMazeGenerator.__str__() outputs the
        solution or not"""
        self.showSolution = show
    
    def generate_maze(self):
        """WilsonMazeGenerator.generate_maze() -> None
        Generates the maze according to the Wilson Loop Erased Random
        Walk Algorithm"""
        # reset the grid before generation
        self.initialize_grid()

        # choose the first cell to put in the visited list
        # see Step 1 of the algorithm.
        current = self.unvisited.pop(random.randint(0,len(self.unvisited)-1))
        self.visited.append(current)
        self.cut(current)

        # loop until all cells have been visited
        while len(self.unvisited) > 0:
            # choose a random cell to start the walk (Step 2)
            first = self.unvisited[random.randint(0,len(self.unvisited)-1)]
            current = first
            # loop until the random walk reaches a visited cell
            while True:
                # choose direction to walk (Step 3)
                dirNum = random.randint(0,3)
                # check if direction is valid. If not, choose new direction
                while not self.is_valid_direction(current,dirNum):
                    dirNum = random.randint(0,3)
                # save the cell and direction in the path
                self.path[current] = dirNum
                # get the next cell in that direction
                current = self.get_next_cell(current,dirNum,2)
                if (current in self.visited): # visited cell is reached (Step 5)
                    break

            current = first # go to start of path
            # loop until the end of path is reached
            while True:
                # add cell to visited and cut into the maze
                self.visited.append(current)
                self.unvisited.remove(current) # (Step 6.b)
                self.cut(current)

                # follow the direction to next cell (Step 6.a)
                dirNum = self.path[current]
                crossed = self.get_next_cell(current,dirNum,1)
                self.cut(crossed) # cut crossed edge

                current = self.get_next_cell(current,dirNum,2)
                if (current in self.visited): # end of path is reached
                    self.path = dict() # clear the path
                    break
                
        self.generated = True
                
    ## Private Methods ##
    ## Do Not Use Outside This Class ##
                
    def get_next_cell(self,cell,dirNum,fact):
        """WilsonMazeGenerator.get_next_cell(tuple,int,int) -> tuple
        Outputs the next cell when moved a distance fact in the the
        direction specified by dirNum from the initial cell.
        cell: tuple (y,x) representing position of initial cell
        dirNum: int with values 0,1,2,3
        fact: int distance to next cell"""
        dirTup = self.directions[dirNum]
        return (cell[0]+fact*dirTup[0],cell[1]+fact*dirTup[1])

    def is_valid_direction(self,cell,dirNum):
        """WilsonMazeGenerator(tuple,int) -> boolean
        Checks if the adjacent cell in the direction specified by
        dirNum is within the grid
        cell: tuple (y,x) representing position of initial cell
        dirNum: int with values 0,1,2,3"""
        newCell = self.get_next_cell(cell,dirNum,2)
        tooSmall = newCell[0] < 0 or newCell[1] < 0
        tooBig = newCell[0] >= self.height or newCell[1] >= self.width
        return not (tooSmall or tooBig)

    def initialize_grid(self):
        """WilsonMazeGenerator.initialize_grid() -> None
        Resets the maze grid to blank before generating a maze."""
        for i in range(self.height):
            for j in range(self.width):
                self.grid[i][j] = 0
                
        # fill up unvisited cells
        for r in range(self.height):
            for c in range(self.width):
                if r % 2 == 0 and c % 2 == 0:
                    self.unvisited.append((r,c))

        self.visited = []
        self.path = dict()
        self.generated = False

    def cut(self,cell):
        """WilsonMazeGenerator.cut(tuple) -> None
        Sets the value of the grid at the location specified by cell
        to 1
        cell: tuple (y,x) location of where to cut"""
        self.grid[cell[0]][cell[1]] = 1

class Algorithm1(WilsonMazeGenerator):
    def __init__(self, height, width):
        super().__init__(height, width)
    
    def Apply(self):
        self.generate_maze()
        print("Applying Algorithm1")

    def DoSomething(self):
        pass

class Algorithm2(Strategy):
    def Apply(self):
        print("Applying Algorithm2")

    def DoSomething(self):
        pass

class Generator:
    def __init__(self):
        self.strategy = None

    def SetStrategy(self, new_strategy):
        self.strategy = new_strategy

    def Generate(self):
        self.strategy.Apply()
        self.strategy.DoSomething()

class Creator:
    def __init__(self, maze):
        self.maze = maze

    def PrintLabyrinth(self, filename):
        walls = self.GenerateWalls()
        lines = []
        lines.append("// Labyrinth generated for openscad")
        lines.append("// IFT2125 - H24")
        lines.append("// Authors : Canelle Wagner et Alex Maggioni")
        lines.append("difference(){")
        lines.append("union(){")
        lines.append("// base plate")
        lines.append(f"translate([-0.5,-0.5,-1]){{")
        lines.append(f"cube([{self.maze.width * cell_size + 1},{self.maze.height * cell_size + 1},1], center=false);")
        lines.append("}")
        for wall in walls:
            lines.append("translate([%s,%s,%s]){" % (wall[0], wall[1], wall_height / 2))
            if wall[2]:  # If wall is vertical
                lines.append(f"cube([{cell_size},{wall_thickness},{wall_height}], center=true);")
            else:
                lines.append(f"cube([{wall_thickness},{cell_size},{wall_height}], center=true);")
            lines.append("}")
        # Attention je dois rajouer les bordure et le logo
        lines.append("}}")

        # Enregistrement des lignes dans un fichier .scad
        with open(filename, 'w') as file:
            file.write('\n'.join(lines))

    def GenerateWalls(self):
        walls = []
        for i in range(self.maze.height):
            for j in range(self.maze.width):
                if self.maze.grid[i][j] == 0:  # If there's a wall at this cell
                    # Translate the grid position to OpenSCAD coordinates
                    x = j * cell_size
                    y = i * cell_size
                    walls.append((x, y, False))  # Horizontal wall
                    walls.append((x, y, True))  # Vertical wall
        return walls

def main():
    strategy_choice = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    my_generator = Generator()
    if strategy_choice == 1:
        my_generator.SetStrategy(Algorithm1(10, 10))  # Taille de labyrinthe 10x10
    elif strategy_choice == 2:
        my_generator.SetStrategy(Algorithm2())
    else:
        print("error strategy choice")
        return
    my_generator.Generate()

    # Création du fichier .scad
    my_creator = Creator(my_generator.strategy)
    output_filename = 'labyrinth3.scad'
    my_creator.PrintLabyrinth(output_filename)
    print(f"Generated {output_filename}")

if __name__ == "__main__":
    main()
