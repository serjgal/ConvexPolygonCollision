import math

import pygame


class Polygon:
    """A class to represent a polygon as defined by a center point, list of points and scale factor."""

    center: pygame.Vector2
    points: list[pygame.Vector2]
    rotated_points: list[pygame.Vector2]
    rotation: float

    width: int
    name: str

    def __init__(self, name, x: int, y: int, points: list[pygame.Vector2], scale: float = 1, width: int = 3):

        if len(points) < 3:
            raise ValueError("A polygon must have at least 3 points.")

        self.center = pygame.Vector2(x, y)
        self.points = [point * scale for point in points]
        self.rotated_points = self.points[:]

        self.width = width
        self.rotation = 0

        self.name = name

    def draw(self, screen: pygame.Surface, color: tuple[int, int, int], highlight_color: tuple[int, int, int] | None = None):
        """Draw the polygon on the screen."""
        pygame.draw.line(screen, color, self.center, self.center + self.rotated_points[0], self.width)
        for i in range(0, len(self.points)):
            if highlight_color:
                pygame.draw.line(screen, highlight_color,
                                 self.center + self.rotated_points[i],
                                 self.center + self.rotated_points[(i + 1) % len(self.rotated_points)],
                                 self.width * 2)
            pygame.draw.line(screen, color,
                             self.center + self.rotated_points[i],
                             self.center + self.rotated_points[(i + 1) % len(self.rotated_points)],
                             self.width)

    def contains(self, x, y):
        """Check if a point is inside the polygon using the ray-casting algorithm."""
        world_point = [self.center + point for point in self.points]
        n = len(world_point)
        inside = False

        # Iterate over each edge of the polygon
        j = n - 1  # Previous vertex index
        for i in range(n):
            xi, yi = world_point[i]
            xj, yj = world_point[j]

            # Check if the ray crosses the edge
            if ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi):
                inside = not inside  # Toggle state

            j = i  # Move to the next edge

        return inside

    def move_by(self, d: pygame.Vector2):
        """Move the polygon by a given amount."""
        self.center += d

    def rotate_by(self, angle):
        """Rotate the polygon by a given angle."""
        self.rotation += angle
        self.rotated_points = [point.rotate(self.rotation) for point in self.points]

    def reset_rotation(self):
        """Reset the rotation of the polygon."""
        self.rotated_points = self.points[:]
        self.rotation = 0

    def get_vertices (self):
        return [self.center + point for point in self.rotated_points]

    def __str__(self):
        return self.name


def generate_polygon_points(sides: int, radius = 1, center = pygame.Vector2(0, 0)):
    """Generates a set of points for a regular polygon."""
    points = []
    angle_step = 2 * math.pi / sides  # The angle between each vertex

    for i in range(sides):
        angle = i * angle_step - math.pi / 2  + (angle_step / 2  if sides % 2 == 0 else 0)
        x = center[0] + radius * math.cos(angle)
        y = center[1] + radius * math.sin(angle)
        points.append(pygame.math.Vector2(round(x, 2), round(y, 2)))  # Add the point as a Vector2

    return points


def get_coalitions(polygons: list[Polygon]) -> list[tuple[Polygon, Polygon]]:
    collections = []

    for i in range(len(polygons) - 1):
        for j in range(i + 1, len(polygons)):
            if sat_coalition(polygons[i].get_vertices(), polygons[j].get_vertices()):
                collections.append((polygons[i], polygons[j]))

    return collections


def sat_coalition(vertices_a: list[pygame.Vector2], vertices_b: list[pygame.Vector2]) -> bool:
    """Check if two polygons are colliding using the Separating Axis Theorem."""

    for i in range(len(vertices_a)):
        va = vertices_a[i]
        vb = vertices_a[(i + 1) % len(vertices_a)]
        edge = va - vb
        axis = pygame.Vector2(edge.y, -edge.x)
        if not axis.length_squared() == 0: axis.normalize_ip()

        min_a = min([v.dot(axis) for v in vertices_a])
        max_a = max([v.dot(axis) for v in vertices_a])
        min_b = min([v.dot(axis) for v in vertices_b])
        max_b = max([v.dot(axis) for v in vertices_b])

        if max_a < min_b or max_b < min_a:
            return False
    for i in range(len(vertices_b)):
        va = vertices_b[i]
        vb = vertices_b[(i + 1) % len(vertices_b)]
        edge = va - vb
        axis = pygame.Vector2(edge.y, -edge.x)
        if not axis.length_squared() == 0: axis.normalize_ip()

        min_a = min([v.dot(axis) for v in vertices_a])
        max_a = max([v.dot(axis) for v in vertices_a])
        min_b = min([v.dot(axis) for v in vertices_b])
        max_b = max([v.dot(axis) for v in vertices_b])

        if max_a < min_b or max_b < min_a:
            return False
    return True
