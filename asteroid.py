from circleshape import CircleShape
import pygame
from logger import log_event
import random
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self._shape_points = self._generate_lumpy_shape()

    def _generate_lumpy_shape(self):
        points = []
        vertex_count = random.randint(10, 14)
        for i in range(vertex_count):
            angle = (360 / vertex_count) * i
            # Random radial jitter gives each asteroid a unique "lumpy" silhouette.
            jitter = random.uniform(0.75, 1.25)
            length = self.radius * jitter
            point_offset = pygame.Vector2(0, 1).rotate(angle) * length
            points.append(point_offset)
        return points

    def _translated_shape_points(self):
        return [self.position + offset for offset in self._shape_points]

    @staticmethod
    def _distance_point_to_segment(point, seg_start, seg_end):
        segment = seg_end - seg_start
        if segment.length_squared() == 0:
            return (point - seg_start).length()

        t = (point - seg_start).dot(segment) / segment.length_squared()
        t = max(0.0, min(1.0, t))
        projection = seg_start + segment * t
        return (point - projection).length()

    @staticmethod
    def _point_in_polygon(point, polygon_points):
        # Ray-casting test.
        inside = False
        j = len(polygon_points) - 1
        for i in range(len(polygon_points)):
            pi = polygon_points[i]
            pj = polygon_points[j]
            intersects = ((pi.y > point.y) != (pj.y > point.y)) and (
                point.x
                < (pj.x - pi.x) * (point.y - pi.y) / ((pj.y - pi.y) + 1e-9) + pi.x
            )
            if intersects:
                inside = not inside
            j = i
        return inside

    @staticmethod
    def _point_in_triangle(point, a, b, c):
        v0 = c - a
        v1 = b - a
        v2 = point - a

        dot00 = v0.dot(v0)
        dot01 = v0.dot(v1)
        dot02 = v0.dot(v2)
        dot11 = v1.dot(v1)
        dot12 = v1.dot(v2)

        denom = dot00 * dot11 - dot01 * dot01
        if denom == 0:
            return False

        inv_denom = 1.0 / denom
        u = (dot11 * dot02 - dot01 * dot12) * inv_denom
        v = (dot00 * dot12 - dot01 * dot02) * inv_denom
        return (u >= 0) and (v >= 0) and (u + v <= 1)

    @staticmethod
    def _segments_intersect(p1, p2, q1, q2):
        def orientation(a, b, c):
            val = (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)
            if abs(val) < 1e-9:
                return 0
            return 1 if val > 0 else 2

        def on_segment(a, b, c):
            return (
                min(a.x, c.x) <= b.x <= max(a.x, c.x)
                and min(a.y, c.y) <= b.y <= max(a.y, c.y)
            )

        o1 = orientation(p1, p2, q1)
        o2 = orientation(p1, p2, q2)
        o3 = orientation(q1, q2, p1)
        o4 = orientation(q1, q2, p2)

        if o1 != o2 and o3 != o4:
            return True

        if o1 == 0 and on_segment(p1, q1, p2):
            return True
        if o2 == 0 and on_segment(p1, q2, p2):
            return True
        if o3 == 0 and on_segment(q1, p1, q2):
            return True
        if o4 == 0 and on_segment(q1, p2, q2):
            return True

        return False

    def _collides_with_circle(self, center, radius):
        points = self._translated_shape_points()

        # Circle center inside polygon.
        if self._point_in_polygon(center, points):
            return True

        # Any polygon edge close enough to circle center.
        for i in range(len(points)):
            a = points[i]
            b = points[(i + 1) % len(points)]
            if self._distance_point_to_segment(center, a, b) <= radius:
                return True

        return False

    def _collides_with_triangle(self, triangle_points):
        points = self._translated_shape_points()
        a, b, c = triangle_points

        # Triangle vertex inside asteroid polygon.
        for t_point in triangle_points:
            if self._point_in_polygon(t_point, points):
                return True

        # Asteroid polygon vertex inside triangle.
        for p_point in points:
            if self._point_in_triangle(p_point, a, b, c):
                return True

        # Edge intersection test.
        tri_edges = [(a, b), (b, c), (c, a)]
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            for t1, t2 in tri_edges:
                if self._segments_intersect(p1, p2, t1, t2):
                    return True

        return False

    def collides_with(self, other):
        if hasattr(other, "triangle"):
            return self._collides_with_triangle(other.triangle())
        if hasattr(other, "position") and hasattr(other, "radius"):
            return self._collides_with_circle(other.position, other.radius)
        return super().collides_with(other)

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self._translated_shape_points(), LINE_WIDTH)

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        log_event("asteroid_split")
        angle = random.uniform(20, 50)
        new_vel1 = self.velocity.rotate(angle)
        new_vel2 = self.velocity.rotate(-angle)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        if new_radius > 0:
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = new_vel1 * 1.2
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2.velocity = new_vel2 * 1.2
        

