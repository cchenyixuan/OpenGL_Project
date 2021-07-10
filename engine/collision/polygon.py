from OpenGL.GL import *
import numpy as np
from pyrr.matrix44 import create_from_translation, create_from_axis_rotation, create_from_scale


class ModelObject:
    def __init__(self, filename=r"D:\pythonstudio\OpenGL_Project\engine\resources\model\ball.obj"):
        from ObjLoader import LoadObject
        object_loader = LoadObject()
        from MtlLoader import LoadMaterial
        material_loader = LoadMaterial()
        # load vertices(x y z u v nx ny nz), indices and normals
        self.vertices, self.indices = object_loader.load_file(filename)
        self.normal = [np.array(vertex[5:]) for vertex in self.vertices]
        self.vertex = [np.array(vertex[:3]) for vertex in self.vertices]
        # create frame with vertices, indices and normals
        self.frame_vertices, self.frame_indices = self.create_frame(self.vertex)
        self.frame_normal = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], dtype=np.float32)
        self.frame_vertex = [np.array(vertex[:3]) for vertex in self.frame_vertices]
        # create vao for model and its frame
        self.vao = self.create_vao(self.vertices, self.indices)
        self.texture = material_loader.load_file(filename[:-3] + "mtl")
        self.frame_vao = self.create_vao(self.frame_vertices, self.frame_indices)
        # attributes
        self.indices_length = self.indices.nbytes // 4
        self.frame_indices_length = self.frame_indices.nbytes // 4
        self.is_static = True
        self.scale = np.array([1.0, 1.0, 1.0])
        self.rotation = [np.array([1.0, 0.0, 0.0], dtype=np.float32), 0.0]
        self.offset = np.array([0.0, 0.0, 0.0, 0.0])
        self.selected = False
        # additional attributes for frame detection

    def get_model_matrix(self):
        return create_from_axis_rotation(*self.rotation) @ create_from_scale(self.scale) @ create_from_translation(
            self.offset)

    def get_frame_model_matrix(self):
        return create_from_translation(self.offset)

    def set_attribute(self, **kwargs):
        for key in kwargs:
            value = kwargs[key]
            self.__setattr__(key, value)
        # type check for scale: float --> [float, float, float]
        if type(self.scale) is not np.ndarray:
            self.scale = np.array([self.scale] * 3)
        self.__call__()

    def __call__(self):
        # update vertex status
        model = create_from_translation(self.offset).T @ create_from_axis_rotation(*self.rotation).T @ create_from_scale(self.scale)
        self.vertex = [model @ np.array([*vertex[:3], 1.0]) for vertex in self.vertices]
        self.normal = [create_from_axis_rotation(*self.rotation) @ np.array([*vertex[5:8], 1.0]) for vertex in self.vertices]
        # create frame
        frame_model = create_from_scale(self.scale) @ create_from_axis_rotation(*self.rotation).T
        vertex_for_frame = [frame_model @ np.array([*vertex[:3], 1.0]) for vertex in self.vertices]
        self.frame_vertices, self.frame_indices = self.create_frame(vertex_for_frame)
        # update frame vao
        glDeleteVertexArrays(1, (self.frame_vao,))
        self.frame_vao = self.create_vao(self.frame_vertices, self.frame_indices)
        # update frame_vertex status
        frame_vertex_model = self.get_frame_model_matrix().T
        self.frame_vertex = [frame_vertex_model @ np.array([*vertex[:3], 1.0]) for vertex in self.frame_vertices]
        self.frame_vertex = [vertex[:3] for vertex in self.frame_vertex]

    @staticmethod
    def create_frame(vertex):
        x_min = 1e8
        x_max = -1e8
        y_min = 1e8
        y_max = -1e8
        z_min = 1e8
        z_max = -1e8
        for _vertex in vertex:
            if _vertex[0] >= x_max:
                x_max = _vertex[0]
            if _vertex[1] >= y_max:
                y_max = _vertex[1]
            if _vertex[2] >= z_max:
                z_max = _vertex[2]
            if _vertex[0] <= x_min:
                x_min = _vertex[0]
            if _vertex[1] <= y_min:
                y_min = _vertex[1]
            if _vertex[2] <= z_min:
                z_min = _vertex[2]
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
