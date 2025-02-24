import pygame
from polygon import Polygon, get_coalitions, generate_polygon_points

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 800, 600
DISPLAY_CAPTION = "Convex Polygon Collision Detection"
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(DISPLAY_CAPTION)

clock = pygame.time.Clock()
FPS = 60

# Text
font = pygame.font.Font(None, 24)
coalition_text: str = "Coalition: {p1} with {p2}"
text_rect = pygame.Rect(10, 10, 0, 0)

# Colors
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)
RED: tuple[int, int, int] = (255, 0, 0)
BLUE: tuple[int, int, int] = (0, 0, 255)

# shapes
name_of_shapes = ["Square", "Triangle", "Pentagon", "Hexagon", "Heptagon", "Octagon", "Nonagon", "Decagon"]
pos_of_shapes = generate_polygon_points(len(name_of_shapes), 200, pygame.Vector2(WIDTH // 2, HEIGHT // 2))

polygon_move_speed: int = 50
polygon_rotation_speed: int = 90
polygon_scale: int = 40

polygons = [Polygon(name_of_shapes[i],
                    pos_of_shapes[i].x, pos_of_shapes[i].y,
                    generate_polygon_points(3 + i),
                    polygon_scale)
            for i in range(len(name_of_shapes))]
selected_polygon = None


def game_loop(screen: pygame.Surface, delta_time: float = 1.0):
    global selected_polygon

    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouse_clicked_l, mouse_clicked_m, mouse_clicked_r, scroll_up, scroll_down = pygame.mouse.get_pressed(5)

    keys = pygame.key.get_pressed()
    arrow_vector = pygame.Vector2(-1 if keys[pygame.K_LEFT] else 1 if keys[pygame.K_RIGHT] else 0,
                                  -1 if keys[pygame.K_UP] else 1 if keys[pygame.K_DOWN] else 0)
    rotation = -1 if keys[pygame.K_z] else 1 if keys[pygame.K_c] else 0

    if mouse_clicked_l:
        for polygon in polygons:
            if polygon.contains(mouse_x, mouse_y):
                selected_polygon = polygon
                break

    if selected_polygon:
        selected_polygon.move_by(arrow_vector * polygon_move_speed * delta_time)
        selected_polygon.rotate_by(rotation * polygon_rotation_speed * delta_time)

        if keys[pygame.K_x]:
            selected_polygon.reset_rotation()

        if keys[pygame.K_SPACE]:
            selected_polygon = None

    coalitions = get_coalitions(polygons)
    for coalition in coalitions:
        text_surface = font.render(coalition_text.format(p1 = coalition[0], p2 = coalition[1]), True, WHITE)
        screen.blit(text_surface, text_rect)

    for polygon in polygons:
        polygon.draw(screen,
                     RED if any(polygon in coalition for coalition in coalitions) else WHITE,
                     BLUE if polygon == selected_polygon else None)


if __name__ == "__main__":
    # Game loop
    running = True
    previous_time = pygame.time.get_ticks()  # Time of the previous frame
    while running:
        screen.fill(BLACK)  # Fill the screen with a background color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        current_time = pygame.time.get_ticks()
        delta_time = (current_time - previous_time) / 1000  # Convert to seconds
        game_loop(screen, delta_time)  # Call the game loop function
        previous_time = current_time

        pygame.display.update()  # Update the display
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
