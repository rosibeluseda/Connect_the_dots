import pygame


def draw_grid(matrix, screenWidth, screenHeight, screen, game_size):
    blockSize = 35
    offset_x = (screenWidth - matrix.shape[1] * blockSize) // 2
    offset_y = (screenHeight - matrix.shape[0] * blockSize) // 2

    # Colors
    grey = (211, 211, 211)
    red = (139, 0, 0)
    blue = (0, 0, 255)
    light_blue = (99, 155, 255)
    light_red = (217, 87, 99)
    color_map = {0: grey, 1: red, 2: blue, 3: light_blue, 4: light_red}

    for x in range(game_size):
        for y in range(game_size):
            square = matrix[x][y]

            if square.bg != 0:  # If bg is not 0, draw the rect with the corresponding color
                rect = pygame.Rect(
                    (x * blockSize) + offset_x,
                    (y * blockSize) + offset_y,
                    blockSize, blockSize
                )
                pygame.draw.rect(screen, color_map[square.bg], rect)

            points = [
                ((x * blockSize) + offset_x, (y * blockSize) + offset_y),
                ((x * blockSize) + offset_x, (y * blockSize + blockSize) + offset_y),
                ((x * blockSize + blockSize) + offset_x, (y * blockSize + blockSize) + offset_y),
                ((x * blockSize + blockSize) + offset_x, (y * blockSize) + offset_y)
            ]

            for i in range(4):
                pygame.draw.line(screen, color_map[getattr(square, ["left", "bottom", "right", "top"][i])], points[i],
                                 points[(i + 1) % 4], 7)

            for px, py in points:
                pygame.draw.circle(screen, (0, 0, 0), (px, py), 4)
