import pygame

pygame.font.init()

r = 3
row_pixel = 500

font1 = pygame.font.SysFont("comicsans", 40)
screen = pygame.display.set_mode((row_pixel, (row_pixel + 100)))


grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
       ]


def draw():
    global row_pixel
    cell_bg_clr = (120, 120, 120)
    cell_size = row_pixel / (r**2)
    for i in range(r**2):
        for j in range(r**2):

            if (i + 1) % r == 0:
                cell_size_1 = (cell_size - 5)
            else:
                cell_size_1 = (cell_size - 1)

            if (j + 1) % r == 0:
                cell_size_2 = (cell_size - 5)
            else:
                cell_size_2 = (cell_size - 1)

            if i == 0:
                cell_stt1 = 4
                cell_size_1 -= 4
            else:
                cell_stt1 = i * cell_size

            if j == 0:
                cell_stt2 = 4
                cell_size_2 -= 4
            else:
                cell_stt2 = j * cell_size

            pygame.draw.rect(screen, cell_bg_clr, (cell_stt1, cell_stt2, cell_size_1, cell_size_2))


while True:

    screen.fill((200, 200, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

    draw()

    pygame.display.update()

pygame.quit()
