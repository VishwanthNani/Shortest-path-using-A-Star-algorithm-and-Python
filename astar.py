import pygame
from queue import PriorityQueue

tiles=[]
source_set=0
target_set=0
SIZE = 800
ROWS=50
pygame.display.set_caption("Shortest Path Finder")
DISPLAY = pygame.display.set_mode((SIZE, SIZE))

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)


class Tile:
    def __init__(self, color, row, column, size, total_rows):
        self.color = color
        self.width = size // total_rows
        self.row = row
        self.column = column
        self.x = column * self.width
        self.y = row * self.width
        self.linear_neighbours=[]
        self.diagonal_neighbours=[]

    def get_pos(self) -> tuple:
        return self.x, self.y

    def make_source(self):
        self.color=BLUE
        self.draw_tile(DISPLAY)
        pygame.display.update()  # Updating the display

    def make_obstacle(self):
        self.color=BLACK
        self.draw_tile(DISPLAY)
        pygame.display.update()  # Updating the display

    def make_target(self):
        self.color=YELLOW
        self.draw_tile(DISPLAY)
        pygame.display.update()  # Updating the display

    def make_unfavourable_neighbour(self):
        self.color=RED
        self.draw_tile(DISPLAY)
        pygame.display.update()  # Updating the display

    def make_favourable_neighbour(self):
        self.color=GREEN
        self.draw_tile(DISPLAY)
        pygame.display.update()  # Updating the display

    def make_path(self):
        self.color=ORANGE
        self.draw_tile(DISPLAY)
        pygame.display.update()  # Updating the display

    def make_initial(self):
        self.color=WHITE
        self.draw_tile(DISPLAY)
        pygame.display.update()  # Updating the display


    def is_initial(self):
        return self.color==WHITE

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_obstacle(self):
        return self.color == BLACK

    def is_source(self):
        return self.color == BLUE

    def is_target(self):
        return self.color == YELLOW

    def update_neighbours(self):
        if self.row != 0 and self.column != 0 and not tiles[self.row - 1][self.column - 1].is_obstacle():
            self.diagonal_neighbours.append(tiles[self.row - 1][self.column - 1])
        if self.row != 0 and not tiles[self.row - 1][self.column].is_obstacle():
            self.linear_neighbours.append(tiles[self.row - 1][self.column])
        if self.row != 0 and self.column != ROWS - 1 and not tiles[self.row - 1][self.column + 1].is_obstacle():
            self.diagonal_neighbours.append(tiles[self.row - 1][self.column + 1])
        if  self.column!=0 and  not tiles[self.row][self.column-1].is_obstacle():
            self.linear_neighbours.append(tiles[self.row][self.column-1])
        if  self.row!=0 and  not tiles[self.row-1][self.column].is_obstacle():
            self.linear_neighbours.append(tiles[self.row-1][self.column])
        if  self.column!=ROWS-1 and  not tiles[self.row][self.column+1].is_obstacle():
            self.linear_neighbours.append(tiles[self.row][self.column+1])
        if  self.row!=ROWS-1 and  not tiles[self.row+1][self.column].is_obstacle():
            self.linear_neighbours.append(tiles[self.row+1][self.column])


    def draw_tile(self, display):
        rect = pygame.Rect(self.x, self.y, self.width, self.width)

        # Fill the rectangle with self.color
        pygame.draw.rect(display, self.color, rect)

        # Draw the border with BLACK color
        pygame.draw.rect(display, BLACK, rect, 1)  # Border thickness: 1 pixel


def draw_screen(display, size, rows):
    for i in range(rows):
        tiles.append([])
        for j in range(rows):
            a = Tile(WHITE, i, j, size, rows)
            tiles[i].append(a)
            a.draw_tile(display)

def get_clicked_pos(pos, rows, size):
    width = size // rows
    y,x = pos

    row = y // width
    col = x // width

    return row, col



def h_dist(start:Tile, target:Tile):
    y1=start.row
    x1=start.column
    y2=target.row
    x2=target.column
    return abs(y1-y2)+abs(x1-x2)



def trace_back_path(came_from,current,source):
    while current in came_from:
        current=came_from[current]
        if not current==source:
            current.make_path()




def algo(source, target):
    open_set = PriorityQueue()
    count = 0
    open_set.put((0, count, source))
    came_from = {}
    g_score = {tile: float("inf") for tile_row in tiles for tile in tile_row}
    g_score[source] = 0
    f_score = {tile: float("inf") for tile_row in tiles for tile in tile_row}
    f_score[source] = h_dist(source, target)
    open_set_hash = {source}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == target:
            trace_back_path(came_from, current, source)
            target.make_target()
            # Calculate and print the distance
            path_distance = g_score[target]
            print(f"Shortest path distance: {path_distance}")
            return True, path_distance

        for neighbour in current.linear_neighbours:
            if not neighbour.is_obstacle() and g_score[current] + 1 < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = g_score[current] + 1
                f_score[neighbour] = g_score[neighbour] + h_dist(neighbour, target)

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    current.make_favourable_neighbour()

        for neighbour in current.diagonal_neighbours:
            if not neighbour.is_obstacle() and g_score[current] + 1.4 < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = g_score[current] + 1.4
                f_score[neighbour] = g_score[neighbour] + h_dist(neighbour, target)

                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    current.make_favourable_neighbour()

        if current != source:
            current.make_unfavourable_neighbour()

    # If no path is found
    return False, None








def run():
    global source_set, target_set
    source = None
    source_set = 0
    target = None
    target_set = 0
    running = True
    DISPLAY.fill(WHITE)  # Fill the screen with white
    draw_screen(DISPLAY, SIZE, ROWS)  # Drawing the grid
    pygame.display.update()  # Updating the display
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # When Window is closed the game exits
                running = False
            if pygame.mouse.get_pressed()[0]:  # Left button on mouse is pressed
                pos = pygame.mouse.get_pos()
                col, row = get_clicked_pos(pos, 50, 800)  # Getting the clicked position
                tile = tiles[row][col]  # Accessing the clicked tile using clicked position
                if tile.is_initial():
                    if not source_set:
                        tile.make_source()
                        source = tile
                        source_set = 1
                    elif not target_set:
                        tile.make_target()
                        target = tile
                        target_set = 1
                    else:
                        tile.make_obstacle()

                elif tile.is_source or tile.is_target or tile.is_obstacle:
                    pass

            elif pygame.mouse.get_pressed()[2]:  # Right button on mouse is pressed
                pos = pygame.mouse.get_pos()
                col, row = get_clicked_pos(pos, 50, 800)  # Getting the clicked position
                tile = tiles[row][col]  # Accessing the clicked tile using clicked position
                if tile.is_initial():
                    pass
                if tile.is_source():
                    tile.make_initial()
                    source = None
                    source_set = 0
                if tile.is_target():
                    tile.make_initial()
                    target = None
                    target_set = 0
                if tile.is_obstacle():
                    tile.make_initial()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and source and target:
                    for tile_row in tiles:
                        for tile in tile_row:
                            tile.update_neighbours()
                    path_found, path_distance = algo(source, target)
                    if path_found:
                        print(f"Shortest path distance: {path_distance}")

                if event.key == pygame.K_r:
                    source = None
                    source_set = 0
                    target = None
                    target_set = 0
                    for tile_row in tiles:
                        for tile in tile_row:
                            tile.make_initial()
                    pygame.display.update()  # Updating the display

    pygame.quit()


run()
