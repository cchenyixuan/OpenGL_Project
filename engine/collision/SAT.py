import numpy as np


class CheckCollision:
    def __init__(self):
        self.polygon_a = []
        self.polygon_b = []
        self.normals = []

    def __call__(self):
        pass

    def clear(self):
        self.polygon_a = []
        self.polygon_b = []
        self.normals = []

    def load_polygons(self, polygon_a, polygon_b):
        self.normals.extend(polygon_a.frame_normal)
        self.normals.extend(polygon_b.frame_normal)
        self.polygon_a.extend(polygon_a.frame_vertex)
        self.polygon_a = [vertex + polygon_a.offset[:3] for vertex in self.polygon_a]
        self.polygon_b.extend(polygon_b.frame_vertex)
        self.polygon_b = [vertex + polygon_b.offset[:3] for vertex in self.polygon_b]

    def load_polygon_a(self, polygon):
        self.normals.extend(polygon.normal)
        self.polygon_a.extend(polygon.vertex)

    def load_polygon_b(self, polygon):
        self.normals.extend(polygon.normal)
        self.polygon_b.extend(polygon.vertex)

    def separating_axis_theorem(self):
        collision = True
        for axis in self.normals:
            distribution_a = []
            distribution_b = []
            for vertex in self.polygon_a:
                distribution_a.append(np.array(vertex) @ np.array(axis))
            for vertex in self.polygon_b:
                distribution_b.append(np.array(vertex) @ np.array(axis))
            distribution_a.sort()
            distribution_b.sort()
            if distribution_b[0] > distribution_a[-1] or distribution_a[0] > distribution_b[-1]:
                collision = False
                break
            else:
                pass
        return collision
