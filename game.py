import turtle
import math
import time

from consts import Board, Color, Edge, NUM_NODES
from sim_board import GameBoard
from player2 import Player2

"""
Code that handles running the game.
This provides a GUI for you to test your implementation.
You should not need to modify it.
"""

screen = turtle.Screen()
screen.setup(800, 800)
screen.title("Game of Sim")
screen.setworldcoordinates(-1.5, -1.5, 1.5, 1.5)
screen.tracer(0, 0)
turtle.hideturtle()


def draw_dot(x, y, color):
    turtle.up()
    turtle.goto(x, y)
    turtle.color(color)
    turtle.dot(15)


def gen_dots():
    r = []
    for angle in range(0, 360, 60):
        r.append((math.cos(math.radians(angle)), math.sin(math.radians(angle))))
    return r


def draw_line(p1, p2, color):
    turtle.up()
    turtle.pensize(3)
    turtle.goto(p1)
    turtle.down()
    turtle.color(color)
    turtle.goto(p2)


def draw_edge(edge, color):
    p1 = (math.cos(math.radians(edge[0] * 60)), math.sin(math.radians(edge[0] * 60)))
    p2 = (math.cos(math.radians(edge[1] * 60)), math.sin(math.radians(edge[1] * 60)))
    draw_line(p1, p2, color)


def draw_empty_board():
    global selection

    for i in range(len(dots)):
        if i in selection:
            draw_dot(dots[i][0], dots[i][1], "red")
        else:
            draw_dot(dots[i][0], dots[i][1], "dark gray")


def draw_board(board: Board):
    draw_empty_board()
    for i in range(NUM_NODES):
        for j in range(NUM_NODES):
            if board[i][j] == Color.P1:
                draw_edge((i, j), "red")
            elif board[i][j] == Color.P2:
                draw_edge((i, j), "blue")
            elif board[i][j] == Color.UNCOLORED:
                draw_edge((i, j), "grey")
    screen.update()


def play(x, y):
    global selection

    # Decide if they clicked a dot
    for i in range(len(dots)):
        dist = (dots[i][0] - x) ** 2 + (dots[i][1] - y) ** 2
        if dist < 0.001:
            # Select / unselect
            if i in selection:
                selection.remove(i)
            else:
                selection.append(i)
            break

    # If 2 dots have been selected, the player has made their move
    if len(selection) == 2:
        # Player 1 move
        if myGame.board[selection[0]][selection[1]] == Color.UNCOLORED:
            myGame.color_edge((selection[0], selection[1]), Color.P1)
            draw_board(myGame.board)

            # Check if that move ended the game
            winner = myGame.get_winner()
            print(winner)
            if winner != None:
                screen.textinput("Game Over", Color(winner).name + " won!")
                turtle.bye()

            # Player 2 move
            time.sleep(0.05)
            move = Player2.get_move(myGame.board)
            myGame.color_edge(move, Color.P2)
        selection = []
    draw_board(myGame.board)

    winner = myGame.get_winner()
    if winner != None:
        screen.textinput("Game Over", Color(winner).name + " won!")
        turtle.bye()


selection = []
dots = gen_dots()
myGame = GameBoard()
draw_board(myGame.board)
screen.onclick(play)
turtle.mainloop()
