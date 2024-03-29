import sys
import random

cell_size = 10  # mm
wall_height = 10  # mm
wall_thickness = 1  # mm

strategy_choice = 1

class Strategy:
    def __init__(self):
        self.maze = None

    def Apply(self):
        print("Applying Abstract Strategy")

    def DoSomething(self):
        pass

class Cell:
    def __init__(self, x, y):
        self.visited = False
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.x = x
        self.y = y

class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]

    def get_unvisited_neighbors(self, cell):
        neighbors = []
        directions = [('top', 0, -1), ('right', 1, 0), ('bottom', 0, 1), ('left', -1, 0)]
        for direction, dx, dy in directions:
            nx, ny = cell.x + dx, cell.y + dy
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.grid[nx][ny]
                if not neighbor.visited:
                    neighbors.append((direction, neighbor))
        return neighbors

    def remove_wall(self, current, neighbor, direction):
        current.walls[direction] = False
        opposite_directions = {'top': 'bottom', 'right': 'left', 'bottom': 'top', 'left': 'right'}
        neighbor.walls[opposite_directions[direction]] = False

    def generate(self):
        start = self.grid[0][0]
        stack = [start]

        while stack:
            current = stack[-1]
            current.visited = True
            neighbors = self.get_unvisited_neighbors(current)

            if neighbors:
                direction, next_cell = random.choice(neighbors)
                self.remove_wall(current, next_cell, direction)
                stack.append(next_cell)
            else:
                stack.pop()

class Algorithm1(Strategy):
    def Apply(self):
        print("Applying Algorithm1")
        self.maze = Maze(20, 20)  
        self.maze.generate()
        print("Maze generation complete.")

class Algorithm2(Strategy):
    def Apply(self):
        print("Applying Algorithm2")
        self.maze = Maze(20, 20) 
        self.prim_generate()

    def prim_generate(self):
        # Start with a grid full of walls.
        start_x, start_y = (0, 0)
        self.maze.grid[start_x][start_y].visited = True
        walls = self.get_cell_walls(start_x, start_y)

        while walls:
            wall = random.choice(walls)
            next_cell = self.get_next_cell(wall)
            
            if next_cell:
                self.maze.remove_wall(wall[0], next_cell, wall[2])
                walls.extend(self.get_cell_walls(next_cell.x, next_cell.y))
            
            walls.remove(wall)

    def get_cell_walls(self, x, y):
        walls = []
        directions = [('top', 0, -1), ('right', 1, 0), ('bottom', 0, 1), ('left', -1, 0)]
        for direction, dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height and not self.maze.grid[nx][ny].visited:
                walls.append((self.maze.grid[x][y], self.maze.grid[nx][ny], direction))
        return walls

    def get_next_cell(self, wall):
        current, next_cell, direction = wall
        if not next_cell.visited:
            next_cell.visited = True
            return next_cell
        return None

class Generator:
    strategy = None

    def __init__(self):
        pass

    def SetStrategy(self, new_strategy):
        self.strategy = new_strategy

    def Generate(self):
        self.strategy.Apply()
        self.strategy.DoSomething()

class Creator:
    def __init__(self, maze):
        self.maze = maze

    def export_to_scad(self, filename):
        with open(filename, 'w') as f:
            f.write('union() {\n')
            # Floor
            floor_length = self.maze.width * cell_size
            floor_width = self.maze.height * cell_size
            f.write(f'// Floor\n')
            f.write(f'translate([0, 0, -1]) cube([{floor_length}, {floor_width}, 1]);\n')

            for x in range(self.maze.width):
                for y in range(self.maze.height):
                    cell = self.maze.grid[x][y]
                    # Skip drawing the left wall at the starting point (0,0)
                    if x == 0 and y == 0:
                        cell.walls['left'] = False
                    
                    if cell.walls['top']:
                        self.draw_wall(f, x, y, x+1, y, 'top')
                    if cell.walls['right']:
                        self.draw_wall(f, x+1, y, x+1, y+1, 'right')
                    if cell.walls['bottom']:
                        self.draw_wall(f, x, y+1, x+1, y+1, 'bottom')
                    if cell.walls['left']:
                        self.draw_wall(f, x, y, x, y+1, 'left')
            f.write('}\n')

    def draw_wall(self, f, x1, y1, x2, y2, wall_type):
        x1 *= cell_size
        y1 *= cell_size
        x2 *= cell_size
        y2 *= cell_size
        height = wall_height

        if wall_type in ['top', 'bottom']:
            length = x2 - x1
            f.write(f'// Wall\n')
            f.write(f'translate([{x1}, {y1}, 0]) cube([{length}, {wall_thickness}, {height}]);\n')
        else:  # 'right' or 'left'
            length = y2 - y1
            f.write(f'// Wall\n')
            f.write(f'translate([{x1}, {y1}, 0]) cube([{wall_thickness}, {length}, {height}]);\n')


def main():
    global strategy_choice
    args = sys.argv[:]
    if len(args) >= 2:
        strategy_choice = int(args[1])

    my_generator = Generator()
    if strategy_choice == 1:
        my_generator.SetStrategy(Algorithm1())
    elif strategy_choice == 2:
        my_generator.SetStrategy(Algorithm2())
    else:
        print("Error in strategy choice")
    my_generator.Generate()

    if my_generator.strategy.maze:
        my_creator = Creator(my_generator.strategy.maze)
        my_creator.export_to_scad(f"labyrinthe_algo{strategy_choice}.scad")
    else:
        print("No maze to export.")

if __name__ == "__main__":
    main()