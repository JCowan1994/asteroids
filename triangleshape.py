from circleshape import CircleShape


class TriangleShape(CircleShape):
    def triangle(self):
        raise NotImplementedError

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
    def _point_in_triangle(point, a, b, c):
        # Barycentric technique for stable point-in-triangle checks.
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

    def collides_with(self, other):
        # Triangle hitbox vs circular target hitbox.
        if not hasattr(other, "position") or not hasattr(other, "radius"):
            return False

        points = self.triangle()
        a, b, c = points

        # If any triangle point is inside the other circle.
        for point in points:
            if (point - other.position).length() <= other.radius:
                return True

        # If circle center is inside the triangle.
        if self._point_in_triangle(other.position, a, b, c):
            return True

        # If the circle touches any triangle edge.
        edges = [(a, b), (b, c), (c, a)]
        for edge_start, edge_end in edges:
            if (
                self._distance_point_to_segment(other.position, edge_start, edge_end)
                <= other.radius
            ):
                return True

        return False
