#! Python3
import pygame
import tkinter as tk
import random
from tkinter import messagebox

squares_pos = [(83, 83), (249, 83), (415, 83),
               (83, 249), (249, 249), (415, 249),
               (83, 415), (249, 415), (415, 415)]

marks = [((0, 0), 0), ((0, 0), 0), ((0, 0), 0),
         ((0, 0), 0), ((0, 0), 0), ((0, 0), 0),
         ((0, 0), 0), ((0, 0), 0), ((0, 0), 0)]


class Mark:
    def __init__(self, x, y):
        self.colorO = (255, 0, 0)  # Red
        self.colorX = (0, 153, 255)  # Blue
        self.radius = 80
        self.x = x
        self.y = y

    # draws a X or O
    def draw(self, surface, turnO):
        if turnO:
            pygame.draw.circle(surface, self.colorO, (self.x, self.y), self.radius, 5)  # draw a circle
        elif not turnO:
            pygame.draw.line(surface, self.colorX, (self.x - self.radius, self.y - self.radius), (self.x + self.radius, self.y + self.radius), 5)
            pygame.draw.line(surface, self.colorX, (self.x - self.radius, self.y + self.radius), (self.x + self.radius, self.y - self.radius), 5)


# draws grid
def drawGrid(w, rows, surface):
    sizeBtwn = w // rows
    x = 0
    y = 0

    for l in range(rows):
        x += sizeBtwn
        y += sizeBtwn

        pygame.draw.line(surface, (255, 255, 255), (x, 0), (x, w))
        pygame.draw.line(surface, (255, 255, 255), (0, y), (w, y))


# draws our current view of game
def redrawWindow(surface, rows, width):
    surface.fill((0, 0, 0))
    drawGrid(width, rows, surface)
    for mark in marks:
        if mark == ((0, 0), 0):
            continue
        else:
            Mark(mark[0][0], mark[0][1]).draw(surface=surface, turnO=mark[1])
    pygame.display.update()


# resets the game settings
def reset():
    global turnO, marks, squares_pos, player_first
    turnO = True
    squares_pos = [(83, 83), (249, 83), (415, 83),
                   (83, 249), (249, 249), (415, 249),
                   (83, 415), (249, 415), (415, 415)]
    marks = [((0, 0), 0), ((0, 0), 0), ((0, 0), 0),
             ((0, 0), 0), ((0, 0), 0), ((0, 0), 0),
             ((0, 0), 0), ((0, 0), 0), ((0, 0), 0)]

    # reverse the first player every round
    if player_first:
        player_first = False
    elif not player_first:
        player_first = True


# sends a message which mark won
def message_box(subject, content):
    root = tk.Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    messagebox.showinfo(subject, content)
    root.destroy()


# checks for a tie
def check_draw():
    occupied_pos = []
    for mark in marks:
        if isinstance(mark[1], bool):
            occupied_pos.append(mark[1])
    if len(occupied_pos) == 9:
        return True
    else:
        return False


# this func places a X or O in our game
def marking(pos):
    global turnO, player_turn
    #  square 1
    if pos[0] < 166 and pos[1] > 332 and marks[0] == ((0, 0), 0):
        marks[0] = ((83, 415), turnO)
        squares_pos.remove((83, 415))
        if turnO:
            turnO = False
        else:
            turnO = True
    #  square 2
    elif 166 < pos[0] < 332 < pos[1] and marks[1] == ((0, 0), 0):
        marks[1] = ((249, 415), turnO)
        squares_pos.remove((249, 415))
        if turnO:
            turnO = False
        else:
            turnO = True
    #  square 3
    elif pos[0] > 332 and pos[1] > 332 and marks[2] == ((0, 0), 0):
        marks[2] = ((415, 415), turnO)
        squares_pos.remove((415, 415))
        if turnO:
            turnO = False
        else:
            turnO = True
    #  square 4
    elif pos[0] < 166 < pos[1] < 332 and marks[3] == ((0, 0), 0):
        marks[3] = ((83, 249), turnO)
        squares_pos.remove((83, 249))
        if turnO:
            turnO = False
        else:
            turnO = True
    #  square 5
    elif 166 < pos[0] < 332 and 166 < pos[1] < 332 and marks[4] == ((0, 0), 0):
        marks[4] = ((249, 249), turnO)
        squares_pos.remove((249, 249))
        if turnO:
            turnO = False
        else:
            turnO = True
    #  square 6
    elif pos[0] > 332 > pos[1] > 166 and marks[5] == ((0, 0), 0):
        marks[5] = ((415, 249), turnO)
        squares_pos.remove((415, 249))
        if turnO:
            turnO = False
        else:
            turnO = True
    #  square 7
    elif pos[0] < 166 and pos[1] < 166 and marks[6] == ((0, 0), 0):
        marks[6] = ((83, 83), turnO)
        squares_pos.remove((83, 83))
        if turnO:
            turnO = False
        else:
            turnO = True
    #  square 8
    elif 332 > pos[0] > 166 > pos[1] and marks[7] == ((0, 0), 0):
        marks[7] = ((249, 83), turnO)
        squares_pos.remove((249, 83))
        if turnO:
            turnO = False
        else:
            turnO = True
    #  square 9
    elif pos[0] > 332 and pos[1] < 166 and marks[8] == ((0, 0), 0):
        marks[8] = ((415, 83), turnO)
        squares_pos.remove((415, 83))
        if turnO:
            turnO = False
        else:
            turnO = True

    #  this enables the bot to make a move
    if player_turn:
        player_turn = False
    elif not player_turn:
        player_turn = True


# the main func
def main():
    global turnO, player_turn, player_first
    turnO = True
    player_first = True
    player_turn = player_first
    rows = 3
    width = 500
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption('tic tac toe')

    clock = pygame.time.Clock()

    # main loop
    while True:
        # game speed
        pygame.time.delay(50)
        clock.tick(10)

        # handles game event like using mouse buttons etc
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            # only for bot places a mark in a random square
            if not player_turn:
                marking(random.choice(squares_pos))

            # checks if any mouse button was clicked, saves it to pos
            if event.type == pygame.MOUSEBUTTONUP and player_turn:
                if pygame.mouse.get_pressed():
                    marking(pygame.mouse.get_pos())

        # calls function too draw new window
        redrawWindow(win, rows, width)

        # checks if X or O is in row and shows who won and restarts the game
        if marks[0][1] == marks[1][1] == marks[2][1] and (isinstance(marks[0][1], bool)) and (
                isinstance(marks[1][1], bool)) and (isinstance(marks[2][1], bool)):
            if marks[0][1] and marks[1][1] and marks[2][1] and not 0:
                message_box('O won!', 'Play again...')
                reset()
            elif (marks[0][1] == marks[1][1] == marks[2][1]) and (isinstance(marks[0][1], bool)) and (
                    isinstance(marks[1][1], bool)) and (isinstance(marks[2][1], bool)):
                message_box('X won!', 'Play again...')
                reset()

        elif marks[3][1] == marks[4][1] == marks[5][1] and (isinstance(marks[3][1], bool)) and (
                isinstance(marks[4][1], bool)) and (isinstance(marks[5][1], bool)):
            if marks[3][1] and marks[4][1] and marks[5][1] and not 0:
                message_box('O won!', 'Play again...')
                reset()
            elif (marks[3][1] == marks[4][1] == marks[5][1]) and (isinstance(marks[3][1], bool)) and (
                    isinstance(marks[4][1], bool)) and (isinstance(marks[5][1], bool)):
                message_box('X won!', 'Play again...')
                reset()

        elif marks[6][1] == marks[7][1] == marks[8][1] and (isinstance(marks[6][1], bool)) and (
                isinstance(marks[7][1], bool)) and (isinstance(marks[8][1], bool)):
            if marks[6][1] and marks[7][1] and marks[8][1] and not 0:
                message_box('O won!', 'Play again...')
                reset()
            elif (marks[6][1] == marks[7][1] == marks[8][1]) and (isinstance(marks[6][1], bool)) and (
                    isinstance(marks[7][1], bool)) and (isinstance(marks[8][1], bool)):
                message_box('X won!', 'Play again...')
                reset()

        elif marks[0][1] == marks[3][1] == marks[6][1] and (isinstance(marks[0][1], bool)) and (
                isinstance(marks[3][1], bool)) and (isinstance(marks[6][1], bool)):
            if marks[0][1] and marks[3][1] and marks[6][1] and not 0:
                message_box('O won!', 'Play again...')
                reset()
            elif (marks[0][1] == marks[3][1] == marks[6][1]) and (isinstance(marks[0][1], bool)) and (
                    isinstance(marks[3][1], bool)) and (isinstance(marks[6][1], bool)):
                message_box('X won!', 'Play again...')
                reset()

        elif marks[1][1] == marks[4][1] == marks[7][1] and (isinstance(marks[1][1], bool)) and (
                isinstance(marks[4][1], bool)) and (isinstance(marks[7][1], bool)):
            if marks[1][1] and marks[4][1] and marks[7][1] and not 0:
                message_box('O won!', 'Play again...')
                reset()
            elif (marks[1][1] == marks[4][1] == marks[7][1]) and (isinstance(marks[1][1], bool)) and (
                    isinstance(marks[4][1], bool)) and (isinstance(marks[7][1], bool)):
                message_box('X won!', 'Play again...')
                reset()

        elif marks[2][1] == marks[5][1] == marks[8][1] and (isinstance(marks[2][1], bool)) and (
                isinstance(marks[5][1], bool)) and (isinstance(marks[8][1], bool)):
            if marks[2][1] and marks[5][1] and marks[8][1] and not 0:
                message_box('O won!', 'Play again...')
                reset()
            elif (marks[2][1] == marks[5][1] == marks[8][1]) and (isinstance(marks[2][1], bool)) and (
                    isinstance(marks[5][1], bool)) and (isinstance(marks[8][1], bool)):
                message_box('X won!', 'Play again...')
                reset()

        elif marks[0][1] == marks[4][1] == marks[8][1] and (isinstance(marks[0][1], bool)) and (
                isinstance(marks[4][1], bool)) and (isinstance(marks[8][1], bool)):
            if marks[0][1] and marks[4][1] and marks[8][1] and not 0:
                message_box('O won!', 'Play again...')
                reset()
            elif (marks[0][1] == marks[4][1] == marks[8][1]) and (isinstance(marks[0][1], bool)) and (
                    isinstance(marks[4][1], bool)) and (isinstance(marks[8][1], bool)):
                message_box('X won!', 'Play again...')
                reset()

        elif marks[2][1] == marks[4][1] == marks[6][1] and (isinstance(marks[2][1], bool)) and (
                isinstance(marks[4][1], bool)) and (isinstance(marks[6][1], bool)):
            if marks[2][1] and marks[4][1] and marks[6][1] and not 0:
                message_box('O won!', 'Play again...')
                reset()
            elif (marks[2][1] == marks[4][1] == marks[6][1]) and (isinstance(marks[2][1], bool)) and (
                    isinstance(marks[4][1], bool)) and (isinstance(marks[6][1], bool)):
                message_box('X won!', 'Play again...')
                reset()

        elif check_draw():
            message_box('No one won!', 'Play again...')
            reset()
        else:
            continue


main()
