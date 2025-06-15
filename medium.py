import pygame as p
import time
import random

p.init()

class Square(p.sprite.Sprite):
    def __init__(self, x_id, y_id, number):
        super().__init__()
        self.width = 120
        self.height = 120
        self.x = x_id * self.width
        self.y = y_id * self.height
        self.content = ''
        self.number = number
        self.image = blank_image
        self.image = p.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.center = (self.x, self.y)

    def clicked(self, x_val, y_val):
        global turn, won

        if self.content == '':
            if self.rect.collidepoint(x_val, y_val):
                self.content = turn
                board[self.number] = turn

                if turn == 'x':
                    self.image = x_image
                    self.image = p.transform.scale(self.image, (self.width, self.height))
                    turn = 'o'
                    checkWinner('x')

                    if not won:
                        CompMoveMedium()
                else:
                    self.image = o_image
                    self.image = p.transform.scale(self.image, (self.width, self.height))
                    turn = 'x'
                    checkWinner('o')

def checkWinner(player):
    global background, won, startX, startY, endX, endY

    for i in range(8):
        if board[winners[i][0]] == player and board[winners[i][1]] == player and board[winners[i][2]] == player:
            won = True
            getPos(winners[i][0], winners[i][2])
            break

    if won:
        Update()
        drawLine(startX, startY, endX, endY)
        square_group.empty()
        background = p.image.load(player.upper() + ' Wins.png')
        background = p.transform.scale(background, (WIDTH, HEIGHT))

def CompMoveMedium():
    global move, compMove

    move = True

    # Medium AI: Try to win first, then block, otherwise choose randomly
    for i in range(8):
        line = winners[i]
        x_count = sum(1 for pos in line if board[pos] == 'x')
        o_count = sum(1 for pos in line if board[pos] == 'o')
        empty = [pos for pos in line if board[pos] == '']

        # Win if possible
        if o_count == 2 and len(empty) == 1:
            compMove = empty[0]
            move = False
            break
        
        # Block opponent's win
        if x_count == 2 and len(empty) == 1:
            compMove = empty[0]
            move = False
            break
    
    # If no win/block move, pick a random empty spot
    if move:
        empty_spots = [i for i in range(1, 10) if board[i] == '']
        if empty_spots:
            compMove = random.choice(empty_spots)
            move = False
    
    if not move:
        for square in squares:
            if square.number == compMove:
                square.clicked(square.x, square.y)

def getPos(n1, n2):
    global startX, startY, endX, endY

    for sqs in squares:
        if sqs.number == n1:
            startX = sqs.x
            startY = sqs.y

        elif sqs.number == n2:
            endX = sqs.x
            endY = sqs.y

def drawLine(x1, y1, x2, y2):
    p.draw.line(win, (0, 0, 0), (x1, y1), (x2, y2), 15)
    p.display.update()
    time.sleep(2)

def Update():
    win.blit(background, (0, 0))
    square_group.draw(win)
    square_group.update()
    p.display.update()

WIDTH = 500
HEIGHT = 500

win = p.display.set_mode((WIDTH, HEIGHT))
p.display.set_caption('Tic Tac Toe')
clock = p.time.Clock()

blank_image = p.image.load('Blank.png')
x_image = p.image.load('x.png')
o_image = p.image.load('o.png')
background = p.image.load('Background.png')

background = p.transform.scale(background, (WIDTH, HEIGHT))

move = True
won = False
compMove = 5

square_group = p.sprite.Group()
squares = []

winners = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]
board = ['' for i in range(10)]

startX = 0
startY = 0
endX = 0
endY = 0

num = 1
for y in range(1, 4):
    for x in range(1, 4):
        sq = Square(x, y, num)
        square_group.add(sq)
        squares.append(sq)

        num += 1

turn = 'x'
run = True
while run:
    clock.tick(60)
    for event in p.event.get():
        if event.type == p.QUIT:
            run = False

        if event.type == p.MOUSEBUTTONDOWN and turn == 'x':
            mx, my = p.mouse.get_pos()
            for s in squares:
                s.clicked(mx, my)

    Update()
