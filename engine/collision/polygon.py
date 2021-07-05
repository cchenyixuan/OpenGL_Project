from OpenGL.GL import *
import numpy as np


class ModelObject:
    def __init__(self, filename=r"C:\PycharmProjects\OpenGL_Project\engine\resources\model\ball.obj", scale=1.0):
        from ObjLoader import LoadObject
        object_loader = LoadObject()
        from MtlLoader import LoadMaterial
        material_loader = LoadMaterial()
        # load vertices(x y z u v nx ny nz), indices and normals
        self.vertices, self.indices = object_loader.load_file(filename)
        self.vertices *= scale
        self.normal = [np.array(vertex[5:]) for vertex in self.vertices]
        self.vertex = [np.array(vertex[:3]) for vertex in self.vertices]
        # create frame with vertices, indices and normals
        self.frame_vertices, self.frame_indices = self.create_frame()
        self.frame_normal = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
        self.frame_vertex = [np.array(vertex[:3]) for vertex in self.frame_vertices]
        # create vao for model and its frame
        self.vao = self.create_vao(self.vertices, self.indices)
        self.texture = material_loader.load_file(filename[:-3] + "mtl")
        print(self.texture)
        self.frame_vao = self.create_vao(self.frame_vertices, self.frame_indices)
        # attributes
        self.indices_length = self.indices.nbytes // 4
        self.frame_indices_length = self.frame_indices.nbytes // 4
        self.is_static = True
        self.offset = np.array([0.0, 0.0, 0.0, 0.0])
        self.selected = False

    def __call__(self, scale=float, offset=np.ndarray, static=bool):
        # update vertices with scale
        self.vertex = [np.array(vertex[:3])*scale for vertex in self.vertices]
        self.frame_vertex = [np.array(vertex[:3])*scale for vertex in self.frame_vertices]
        # update attributes
        self.is_static = static
        self.offset = offset

    def create_frame(self):
        x_min = 1e8
        x_max = -1e8
        y_min = 1e8
        y_max = -1e8
        z_min = 1e8
        z_max = -1e8
        _vertices = self.vertex
        for vertex in _vertices:
            if vertex[0] > x_max:
                x_max = vertex[0]
            if vertex[1] > y_max:
                y_max = vertex[1]
            if vertex[2] > z_max:
                z_max = vertex[2]
            if vertex[0] < x_min:
                x_min = vertex[0]
            if vertex[1] < y_min:
                y_min = vertex[1]
            if vertex[2] < z_min:
                z_min = vertex[2]
        frame = np.array([[x_min, y_min, z_min, 0.0, 0.0, 1.0, 0.0, 0.0],
                          [x_min, y_min, z_max, 0.0, 0.0, 1.0, 0.0, 0.0],
                          [x_min, y_max, z_min, 0.0, 0.0, 1.0, 0.0, 0.0],
                          [x_max, y_min, z_min, 0.0, 0.0, 1.0, 0.0, 0.0],
                          [x_max, y_max, z_min, 0.0, 0.0, 1.0, 0.0, 0.0],
                          [x_min, y_max, z_max, 0.0, 0.0, 1.0, 0.0, 0.0],
                          [x_max, y_min, z_max, 0.0, 0.0, 1.0, 0.0, 0.0],
                          [x_max, y_max, z_max, 0.0, 0.0, 1.0, 0.0, 0.0]], dtype=np.float32)
        frame_indices = np.array([0, 1, 2,
                                  1, 2, 5,
                                  0, 1, 3,
                                  1, 3, 6,
                                  1, 5, 6,
                                  5, 6, 7,
                                  0, 2, 3,
                                  2, 3, 4,
                                  2, 4, 5,
                                  4, 5, 7,
                                  3, 4, 6,
                                  4, 6, 7], dtype=np.uint32)
        return frame, frame_indices

    @staticmethod
    def create_vao(vertices, indices):
        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        vbo, ebo = glGenBuffers(2)
        # vbo
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))
        # ebo
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        return vao
