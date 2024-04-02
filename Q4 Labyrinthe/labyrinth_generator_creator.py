#Alex Maggioni, 20266243
#Canelle Wagner, 20232321

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
        # Initialisation du labyrinthe avec des dimensions spécifiques
        self.width = width  
        self.height = height  
        # Création d'une grille de cellules (width x height) non visitées
        self.grid = [[Cell(x, y) for y in range(height)] for x in range(width)]

    ### _________________________________________________________________________________________ ###
    ### Implémentation de l'algorithme : Depth-First Search (Algorithme de backtracking récursif) ###
    ### _________________________________________________________________________________________ ###
            
    def get_unvisited_neighbors(self, cell):
        # Récupère les voisins non visités d'une cellule donnée
        neighbors = []  
        # Directions possibles à vérifier 
        directions = [('top', 0, -1), ('right', 1, 0), ('bottom', 0, 1), ('left', -1, 0)]
        for direction, dx, dy in directions:
            # Calcul des coordonnées du voisin potentiel
            nx, ny = cell.x + dx, cell.y + dy  
            # Vérifie si le voisin est dans les limites de la grille et non visité
            if 0 <= nx < self.width and 0 <= ny < self.height:
                neighbor = self.grid[nx][ny]
                if not neighbor.visited:
                    neighbors.append((direction, neighbor))
        return neighbors  # Retourne la liste des voisins non visités

    def remove_wall(self, current, neighbor, direction):
        # Enlève le mur entre deux cellules adjacentes
        current.walls[direction] = False  # Enlève le mur de la cellule actuelle
        # Définit les directions opposées pour chaque direction
        opposite_directions = {'top': 'bottom', 'right': 'left', 'bottom': 'top', 'left': 'right'}
         # Enlève le mur de la cellule voisine
        neighbor.walls[opposite_directions[direction]] = False 

    def generate(self):
        # Génère le labyrinthe
        # Commence par la cellule en haut à gauche
        start = self.grid[0][0]  
        stack = [start] 

        while stack:
            current = stack[-1]  
            # Marque la cellule comme visitée
            current.visited = True 
            # Obtient les voisins non visités
            neighbors = self.get_unvisited_neighbors(current)  

            if neighbors:
                # S'il y a des voisins non visités, choisit aléatoirement l'un d'eux
                direction, next_cell = random.choice(neighbors)
                 # Enlève le mur entre les cellules
                self.remove_wall(current, next_cell, direction) 
                # Ajoute le voisin choisi à la pile
                stack.append(next_cell)  
            else:
                # S'il n'y a pas de voisins non visités, revient en arrière (backtrack)
                stack.pop()

class Algorithm1(Strategy):
    def Apply(self):
        print("Applying Algorithm1")
        self.maze = Maze(25, 25)  
        self.maze.generate()
        print("Maze generation complete.")
    
class Algorithm2(Strategy):
    def Apply(self):
        print("Applying Algorithm2")
        self.maze = Maze(25, 25)  # Initialise un labyrinthe de taille 13x13
        self.prim_generate() 

    def prim_generate(self):
        # Implémentation de l'algorithme de Prim modifié
        # Commence par la cellule en haut à gauche
        start_x, start_y = (0, 0) 
        # Marque la cellule de départ comme visitée 
        self.maze.grid[start_x][start_y].visited = True  
         # Récupère les murs entourant la cellule de départ
        walls = self.get_cell_walls(start_x, start_y) 
        while walls:
             # Choisissez un mur aléatoirement
            wall = random.choice(walls) 
             # Obtient la cellule de l'autre côté du mur choisi
            next_cell = self.get_next_cell(wall) 
            
            if next_cell:
                # Si la cellule de l'autre côté n'a pas été visitée, enlève le mur et marque la cellule comme visitée
                self.maze.remove_wall(wall[0], next_cell, wall[2])
                # Ajoute les murs de la nouvelle cellule à la liste.
                walls.extend(self.get_cell_walls(next_cell.x, next_cell.y))  

            # Retire le mur traité de la liste
            walls.remove(wall) 

    def get_cell_walls(self, x, y):
        # Récupère tous les murs potentiels autour d'une cellule spécifique
        walls = []  
        # Directions possibles pour vérifier les murs
        directions = [('top', 0, -1), ('right', 1, 0), ('bottom', 0, 1), ('left', -1, 0)]
        for direction, dx, dy in directions:
            # Calcule la position de la cellule voisine
            nx, ny = x + dx, y + dy  
            # Vérifie si le voisin est dans les limites du labyrinthe et n'a pas été visité
            if 0 <= nx < self.maze.width and 0 <= ny < self.maze.height and not self.maze.grid[nx][ny].visited:
                walls.append((self.maze.grid[x][y], self.maze.grid[nx][ny], direction))
        return walls  

    def get_next_cell(self, wall):
        # Détermine la cellule de l'autre côté d'un mur donné
        _, next_cell, _ = wall  
        if not next_cell.visited:
            # Si la cellule de l'autre côté n'a pas été visitée, la marque comme visitée et la retourne
            next_cell.visited = True
            return next_cell
        
        # Retourne None si la cellule a déjà été visitée.
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

    def PrintLabyrinth(self):

        filename = f"labyrinthe_algo{strategy_choice}.scad"

        # Exporte le labyrinthe au format SCAD pour OpenSCAD
        with open(filename, 'w') as f:
            f.write('union() {\n')
            f.write("// Labyrinth generated for openscad\n")
            f.write("// IFT2125 - H24\n")
            f.write("// Authors : Canelle Wagner et Alex Maggioni\n")
            # Dessine le sol du labyrinthe
            floor_length = self.maze.width * cell_size
            floor_width = self.maze.height * cell_size
            f.write(f'// Floor\n')
            f.write(f'translate([0, 0, -1]) cube([{floor_length}, {floor_width}, 1]);\n')

            # Itère sur chaque cellule du labyrinthe pour dessiner les murs
            for x in range(self.maze.width):
                for y in range(self.maze.height):
                    cell = self.maze.grid[x][y]
                    # Omet le dessin du mur de gauche pour la cellule de départ
                    if x == 0 and y == 0:
                        cell.walls['left'] = False
                    
                    # Dessine les murs 
                    if cell.walls['top']:
                        self.draw_wall(f, x, y, x+1, y, 'top')
                    if cell.walls['right']:
                        self.draw_wall(f, x+1, y, x+1, y+1, 'right')
                    if cell.walls['bottom']:
                        self.draw_wall(f, x, y+1, x+1, y+1, 'bottom')
                    if cell.walls['left']:
                        self.draw_wall(f, x, y, x, y+1, 'left')

            # Ajoute le logo
            f.write('// Logo\n')
            f.write('translate([1, -0.2,  1]){\n')  
            f.write('rotate([90, 0, 0]){\n')
            f.write('linear_extrude(1) text("IFT2125 CW & AM", size=7.0);\n')
            f.write('}\n')
            f.write('}\n')

            # Ferme la fonction union
            f.write('}\n')  

    def draw_wall(self, f, x1, y1, x2, y2, wall_type):
        # Calcule les dimensions et dessine un mur
        x1 *= cell_size
        y1 *= cell_size
        x2 *= cell_size
        y2 *= cell_size
        height = wall_height

        # Dessine les murs
        # Murs horizontaux
        if wall_type in ['top', 'bottom']:
            length = x2 - x1
            f.write(f'// Wall\n')
            f.write(f'translate([{x1}, {y1}, 0]) cube([{length}, {wall_thickness}, {height}]);\n')
        # Murs verticaux
        else:  
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
        my_creator.PrintLabyrinth()
    else:
        print("No maze to export.")

if __name__ == "__main__":
    main()