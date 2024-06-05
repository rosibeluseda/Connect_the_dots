'''
Rosibel Useda Viana
AI final project
Instructor: Darren Reid
April 12th, 2024

'''

import pygame
import sys
import numpy as np
import random
from squares import Square
from draw_class import draw_grid

pygame.init()

screenWidth = 1280
screenHeight = 700
game_size = 15
screen = pygame.display.set_mode((screenWidth, screenHeight))
clock = pygame.time.Clock()

pygame.font.init()
background = pygame.image.load('background.jpg') #background image
font = pygame.font.SysFont('Tahoma', 30)
font2 = pygame.font.SysFont('Tahoma', 35)
font3 = pygame.font.SysFont('Tahoma', 20)
font2.set_underline(True)
font2.set_bold(True)
red = (139, 0, 0)
blue = (0, 0, 255)

def update_square_and_neighbor(matrix, x, y, side, value):
    def check_and_update_bg(square):
        # Check if the square is complete to update bg
        if square.is_complete() and square.bg == 0:
            if value == 2:
                square.bg = 3
            else:
                square.bg = 4
                return True

    square = matrix[x][y]
    square.update_side(side, value)
    check_current = check_and_update_bg(square)  # Check and update the current square
    check_n1 = False
    check_n2 = False

    # Update the neighbor square
    neighbor_coords = find_neighbor_coordinates(x, y, side)
    nx, ny = neighbor_coords
    if 0 <= nx < game_size and 0 <= ny < game_size:  # Check bounds
        opposite_side = {"left": "right", "right": "left", "top": "bottom", "bottom": "top"}[side]
        neighbor = matrix[nx][ny]
        neighbor.update_side(opposite_side, value)
        check_n1 = check_and_update_bg(neighbor)  # Check and update the neighbor

    # Check all neighbors
    for check_side in ["left", "right", "top", "bottom"]:
        check_coords = find_neighbor_coordinates(x, y, check_side)
        cx, cy = check_coords
        if 0 <= cx < game_size and 0 <= cy < game_size:
            check_square = matrix[cx][cy]
            check_n2 = check_and_update_bg(check_square)

    return square.is_complete() or check_current or check_n1 or check_n2


def is_valid_click(event_pos, matrix):
    x_click, y_click = event_pos
    blockSize = 35
    offset_x = (screenWidth - matrix.shape[1] * blockSize) // 2
    offset_y = (screenHeight - matrix.shape[0] * blockSize) // 2

    grid_x = (x_click - offset_x) // blockSize
    grid_y = (y_click - offset_y) // blockSize

    if 0 <= grid_x < game_size and 0 <= grid_y < game_size:
        square = matrix[grid_x][grid_y]
        sides = ["left", "bottom", "right", "top"]
        side_distances = [
            abs(x_click - ((grid_x * blockSize) + offset_x)),
            abs(y_click - ((grid_y * blockSize + blockSize) + offset_y)),
            abs(x_click - ((grid_x * blockSize + blockSize) + offset_x)),
            abs(y_click - ((grid_y * blockSize) + offset_y))
        ]

        closest_side_index = side_distances.index(min(side_distances))
        closest_side = sides[closest_side_index]

        # Check if the closest side is grey and the click is close enough to the grid line
        tolerance = 10
        if getattr(square, closest_side) == 0 and side_distances[closest_side_index] <= tolerance:
            return True
    return False


def check_move(event_pos, matrix):
    x_click, y_click = event_pos
    blockSize = 35
    offset_x = (screenWidth - matrix.shape[1] * blockSize) // 2
    offset_y = (screenHeight - matrix.shape[0] * blockSize) // 2

    grid_x = (x_click - offset_x) // blockSize
    grid_y = (y_click - offset_y) // blockSize

    if 0 <= grid_x < game_size and 0 <= grid_y < game_size:
        square = matrix[grid_x][grid_y]
        sides = ["left", "bottom", "right", "top"]
        side_distances = [
            abs(x_click - ((grid_x * blockSize) + offset_x)),
            abs(y_click - ((grid_y * blockSize + blockSize) + offset_y)),
            abs(x_click - ((grid_x * blockSize + blockSize) + offset_x)),
            abs(y_click - ((grid_y * blockSize) + offset_y))
        ]

        closest_side_index = side_distances.index(min(side_distances))
        closest_side = sides[closest_side_index]

        # Validate that the click is on a grid line and the line is grey
        if getattr(square, closest_side) == 0:
            tolerance = 10  # pixels within the line that are considered a valid click
            if side_distances[closest_side_index] <= tolerance:
                completed = update_square_and_neighbor(matrix, grid_x, grid_y, closest_side, 1)

                return completed  # Returns True if a square is completed, False otherwise
    return False


def find_neighbor_coordinates(x, y, side):
    if side == "left":
        return x - 1, y
    elif side == "right":
        return x + 1, y
    elif side == "top":
        return x, y - 1
    elif side == "bottom":
        return x, y + 1
    return None, None


def cpu_move(matrix, mode):
    if (mode == 2):
        # Search for squares with exactly one grey spot free
        for x in range(game_size):
            for y in range(game_size):
                square = matrix[x][y]
                grey_sides = square.grey_sides()
                if len(grey_sides) == 1:
                    return update_square_and_neighbor(matrix, x, y, grey_sides[0], 2)

        # Otherwise, search for 3 or 4 grey sides
        for x in range(game_size):
            for y in range(game_size):
                square = matrix[x][y]
                grey_sides = square.grey_sides()
                if len(grey_sides) in [3, 4]:
                    for side in grey_sides:
                        nx, ny = find_neighbor_coordinates(x, y, side)
                        # Check if neighbor has 3 or 4 grey sides
                        if 0 <= nx < game_size and 0 <= ny < game_size:
                            neighbor = matrix[nx][ny]
                            if len(neighbor.grey_sides()) in [3, 4]:
                                return update_square_and_neighbor(matrix, x, y, side, 2)

        # Lastly, choose any grey line randomly if no squares match the second rule
        all_grey_sides = []
        for x in range(game_size):
            for y in range(game_size):
                square = matrix[x][y]
                grey_sides = square.grey_sides()
                if grey_sides:
                    all_grey_sides.extend([(x, y, side) for side in grey_sides])

        if all_grey_sides:
            x, y, chosen_side = random.choice(all_grey_sides)
            return update_square_and_neighbor(matrix, x, y, chosen_side, 2)

    elif (mode == 1):
        # Search for squares with exactly one grey spot free
        for x in range(game_size):
            for y in range(game_size):
                square = matrix[x][y]
                grey_sides = square.grey_sides()
                if len(grey_sides) == 1:
                    return update_square_and_neighbor(matrix, x, y, grey_sides[0], 2)

        # If no square with exactly one grey side, choose randomly a square with 0 or 1 grey sides
        potential_moves = []
        for x in range(game_size):
            for y in range(game_size):
                square = matrix[x][y]
                grey_sides = square.grey_sides()
                if len(grey_sides) > 0:
                    potential_moves.append((x, y, grey_sides))

        if potential_moves:
            x, y, grey_sides = random.choice(potential_moves)
            chosen_side = random.choice(grey_sides)
            return update_square_and_neighbor(matrix, x, y, chosen_side, 2)

        return False
    else:
        if random.choice([True, False]):
            for x in range(game_size):
                for y in range(game_size):
                    square = matrix[x][y]
                    grey_sides = square.grey_sides()
                    if len(grey_sides) == 1:
                        return update_square_and_neighbor(matrix, x, y, grey_sides[0], 2)

        # If no square with exactly one grey side, choose randomly a square with 0 or 1 grey sides
        potential_moves = []
        for x in range(game_size):
            for y in range(game_size):
                square = matrix[x][y]
                grey_sides = square.grey_sides()
                if len(grey_sides) > 0:
                    potential_moves.append((x, y, grey_sides))

        if potential_moves:
            x, y, grey_sides = random.choice(potential_moves)
            chosen_side = random.choice(grey_sides)
            return update_square_and_neighbor(matrix, x, y, chosen_side, 2)

        return False

    return False


def init_game(game_matrix):
    game_matrix = np.zeros((game_size, game_size), dtype=object)
    for x in range(game_size):
        for y in range(game_size):
            game_matrix[x][y] = Square()

    for x in range(game_size):
        game_matrix[x][0].top = 1
        game_matrix[x][game_size - 1].bottom = 1
        game_matrix[0][x].left = 1
        game_matrix[game_size - 1][x].right = 1

    return game_matrix


game_matrix = None
game_matrix = init_game(game_matrix)
running = True
player_turn = True  # Player will start with first turn
delay = 0
new_game = False
difficulty = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and player_turn and delay <= 0:
            if is_valid_click(event.pos, game_matrix):
                delay = 10  # Delay to see when the cpu moves
                player_completed_square = check_move(event.pos, game_matrix)
                if not player_completed_square:
                    player_turn = False  # false if the player didn't complete a square

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if new_game:
                    new_game = False
                    game_matrix = init_game(game_matrix)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                difficulty = 0

            if event.key == pygame.K_2:
                difficulty = 1

            if event.key == pygame.K_3:
                difficulty = 2

    if not player_turn and delay <= 0:  # CPU's turn
        cpu_completed_square = cpu_move(game_matrix, difficulty)
        if not cpu_completed_square:
            player_turn = True  # Switch back to player's turn if CPU didn't complete a square
    delay -= 1

    def calculate_points(matrix):
        user_points = sum(square.bg == 4 for row in matrix for square in row)
        cpu_points = sum(square.bg == 3 for row in matrix for square in row)
        return user_points, cpu_points


    user_points, cpu_points = calculate_points(game_matrix)

    screen.fill((255, 255, 255))
    # Display scores
    user_score_title = font3.render(f'Scores:', True, (0, 0, 0))
    user_score_text = font.render(f'PLAYER: {user_points}', True, red)
    cpu_score_text = font.render(f'CPU: {cpu_points}', True, blue)
    difficulty_level = font.render(f'Difficulty: {difficulty + 1}', True, (0, 0, 0))
    difficulty_text2 = font3.render(f'To change the difficulty press:', True, (0, 30, 250))
    difficulty_text3 = font3.render(f'1 EZPZ', True, (0, 0, 0))
    difficulty_text4 = font3.render(f'2 Normal', True, (0, 0, 0))
    difficulty_text5 = font3.render(f'3 Diabolical', True, (0, 0, 0))

    screen.blit(background, (0, 0))  # Blit the background
    screen.blit(user_score_title, (20, 80))
    screen.blit(user_score_text, (20, 120))
    screen.blit(cpu_score_text, (20, 160))
    screen.blit(difficulty_level, (1000, 80))
    screen.blit(difficulty_text2, (1000, 130))
    screen.blit(difficulty_text3, (1000, 160))
    screen.blit(difficulty_text4, (1000, 190))
    screen.blit(difficulty_text5, (1000, 220))


    end_game_message = ""
    if cpu_points + user_points == game_size * game_size:
        new_game = True
        if user_points > cpu_points:
            end_game_message = font.render('USER WINS! Press ENTER to start a new game', True, red)
        elif cpu_points > user_points:
            end_game_message = font.render('CPU WINS! Press ENTER to start a new game', True, blue)
        else:
            end_game_message = font.render('DRAW!! Press ENTER to start a new game', True, (0, 0, 0))

    if end_game_message:
        screen.blit(end_game_message, (330, 640))


    title = font2.render('Connect the dots', True, (0, 0, 0))
    screen.blit(title, (screenWidth/2 - 120, 20))
    draw_grid(game_matrix, screenWidth, screenHeight, screen, game_size)
    pygame.display.flip()
    clock.tick(60)

