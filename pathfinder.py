import math
import sys

import pygame
from pygame.locals import *

DGREY = (100, 100, 100)
GREY = (125, 125, 125)
WHITE = (255, 255, 255)
ORANGE = (230, 140, 0)
BLUE = (5, 5, 240)
GREEN = (5, 240, 5)
RED = (240, 5, 5)
BLACK = (5, 5, 5)

FPS = 30

# sizes of window in pixels
WINDOWWIDTH = 500
WINDOWHEIGHT = WINDOWWIDTH

BOARDWIDTH = 10  # number of columns of icons
BOARDHEIGHT = BOARDWIDTH  # number of rows of icons

BOXSIZE = (WINDOWWIDTH/BOARDWIDTH)-WINDOWWIDTH/500  # size of box height & width in pixels
GAPSIZE = WINDOWWIDTH/500  # size of gap between boxes in pixels

# outer border width
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))  # surface that pygame will draw on


def main():
    pygame.init()
    setup()


class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def setup():
    maze = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ]  # 0s are passable, 1s are 'walls'

    running = False  # whether A* is running, or whether the program is in setup
    # initialising start and end nodes
    start = None
    end = None
    setupComplete = False  # the first time the mouse is clicked, it's the start, the second is the end node
    drawBoard(maze, None, None, None, None, running, False)  # draws the basic board
    while not setupComplete:
        # Setup loop. Waits until user has picked start and end nodes
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                if event.button == 1:
                    start = getBoxAtPixel(mousex, mousey)
                elif event.button == BUTTON_RIGHT:
                    end = getBoxAtPixel(mousex, mousey)
                elif event.button == BUTTON_MIDDLE:
                    x, y = getBoxAtPixel(mousex, mousey)
                    maze[y][x] = 1
            if event.type == KEYUP and event.key == K_SPACE:
                setupComplete = True

        drawBoard(maze, None, None, start, end, running, False)  # draws the board with the known start/end node
        pygame.display.update()

    astar(maze, start, end)  # calls A* method


def astar(maze, start, end):
    """Uses A* pathfinding to return a path from a given start to an end"""
    running = True
    finish = False
    # Creates start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    open_list = []
    closed_list = []
    path = []

    open_list.append(start_node)

    # Loops until end is found
    while not finish:

        # Gets the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pops current off open list, adds to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            finish = True

        # Generate children
        children = []
        # Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:

            # Gets node position
            try:
                node_position = (
                    current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])
            except (IndexError, TypeError):
                print('I think you clicked a gap not a box')
                pygame.quit()
                sys.exit()

            # Make sure within maze
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) - 1) or node_position[1] < 0:
                continue

            # Make sure passable (not 'wall')
            if maze[node_position[1]][node_position[0]] != 0:
                continue

            # Creates new child node, add to children
            new_node = Node(current_node, node_position)
            children.append(new_node)

        # Loops through children
        for child in children:
            append = True
            # If child is on closed list, don't append it
            for closed_child in closed_list:
                if child == closed_child:
                    append = False

            # Creates the f, g, and h values
            child.g = current_node.g + 1
            try:
                child.h = math.sqrt(((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2))
            except (IndexError, TypeError):
                print('I think you clicked a gap not a box')
                pygame.quit()
                sys.exit()
            child.f = child.g + child.h

            # If child is on open list, don't append it
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    append = False

            # Add the child to the open list
            if append:
                open_list.append(child)
        drawBoard(maze, open_list, closed_list, start, end, running, finish, path)
        try:
            gameLoop(open_list[-1], finish)
        except IndexError:
            print('No valid path')
            pygame.quit()
            sys.exit()


def gameLoop(box, finish):
    """Controls FPS and handles events"""
    FPSCLOCK = pygame.time.Clock()
    for event in pygame.event.get():  # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
    if finish:
        while finish:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if (event.type == KEYUP and event.key == K_SPACE) or (event.type == KEYUP and event.key == K_ESCAPE):
                    finish = False
            pygame.display.update()
        setup()
    pygame.display.update()
    FPSCLOCK.tick(FPS)


def drawBoard(maze, open_list, closed_list, start, end, running, finish, path=None):
    """Fills in the board with colours based on the state of each node"""
    SCREEN.fill(WHITE)
    for indexY, boxY in enumerate(maze):
        for indexX, boxX in enumerate(boxY):
            left, top = leftTopCoordsOfBox(indexX, indexY)
            pygame.draw.rect(SCREEN, GREY, (left, top, BOXSIZE, BOXSIZE))
            if start is not None and indexX == start[0] and indexY == start[1]:
                # Fills in starting box
                pygame.draw.rect(SCREEN, GREEN, (left, top, BOXSIZE, BOXSIZE))
            if end is not None and indexX == end[0] and indexY == end[1]:
                # Fills in ending box
                pygame.draw.rect(SCREEN, RED, (left, top, BOXSIZE, BOXSIZE))
            if running:
                for box in open_list:
                    # Fills in open list
                    if box.position[0] == indexX and box.position[1] == indexY:
                        pygame.draw.rect(SCREEN, ORANGE, (left, top, BOXSIZE, BOXSIZE))
                for box in closed_list:
                    # Fills in closed list
                    if box.position[0] == indexX and box.position[1] == indexY:
                        pygame.draw.rect(SCREEN, BLUE, (left, top, BOXSIZE, BOXSIZE))
                if finish:
                    # Fills in the path that A* found
                    for box in path:
                        if box[0] == indexX and box[1] == indexY:
                            pygame.draw.rect(SCREEN, GREEN, (left, top, BOXSIZE, BOXSIZE))
            if boxX == 1:
                # Fills in 'walls'
                pygame.draw.rect(SCREEN, BLACK, (left, top, BOXSIZE, BOXSIZE))


def getBoxAtPixel(x, y):
    """Converts pixel coordinates to board coordinates"""
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)


def leftTopCoordsOfBox(boxx, boxy):
    """Converts board coordinates to pixel coordinates"""
    left = boxx * (BOXSIZE + GAPSIZE) + XMARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)


if __name__ == '__main__':
    main()
