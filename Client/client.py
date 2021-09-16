import pygame
from network import Network
from player import Player
width = 500
height = 500
# clientNumber = 0

win = pygame.display.set_mode((width, height))
pygame.display.set_caption(f"Client")

def read_pos(str):
    str = str.split(",")
    return (int(str[0]), int(str[1]))


def make_pos(tup):
    return str(tup[0]) + ',' + str(tup[1])


def redrawWindow(w, player, player2):
    w.fill((255, 255, 255))
    player.draw(w)
    player2.draw(w)
    pygame.display.update()


def main():
    run = True
    clock = pygame.time.Clock()
    n = Network()
    try:
        startPos = read_pos(n.getPos())
    except:
        print("No server connection")
    p = Player(startPos[0], startPos[1], 100, 100, (0, 255, 0))
    p2 = Player(0, 0, 100, 100, (255, 0, 0))
    redrawWindow(win, p, p2)
    print('curr_player pos',p.x,p.y,'opponent pos',p2.x,p2.y)

    while run:
        clock.tick(5000)
        try:
            p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        except:
            print("No connection")
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redrawWindow(win, p, p2)


main()
