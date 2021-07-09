import numpy as np
import re


class LoadObject:
    def __init__(self):
        # x, y, z, u, v, nx, ny, nz
        self.vertices = []
        self.indices = []

    @staticmethod
    def search_data(data_values, data_type):
        compiled_re = {"v": re.compile(r"v ([0-9.-]*) ([0-9.-]*) ([0-9.-]*)", re.S),
                       "vt": re.compile(r"vt ([0-9.-]*) ([0-9.-]*)", re.S),
                       "vn": re.compile(r"vn ([0-9.-]*) ([0-9.-]*) ([0-9.-]*)", re.S),
                       "f": re.compile(r" ([0-9]*)/([0-9]*)/([0-9]*)", re.S)}
        find_number = compiled_re[data_type]
        data = re.findall(find_number, data_values)
        if data_type == "f":
            data = [int(item) - 1 for sub_data in data for item in sub_data]
        else:
            data = [float(item) for item in data[0]]
        return data

    def load_file(self, filename):
        vertices = []
        texture_uvs = []
        normals = []
        buffer = []
        with open(filename, "r", encoding="utf8") as f:
            for row in f.readlines():
                if row[:2] == "v ":
                    vertices.append(self.search_data(row, "v"))
                if row[:2] == "vt":
                    texture_uvs.append(self.search_data(row, "vt"))
                if row[:2] == "vn":
                    normals.append(self.search_data(row, "vn"))
                if row[:2] == "f ":
                    index = self.search_data(row, "f")
                    self.indices.append([index[0], index[3], index[6]])
                    # for i in range(len(index)//3):
                    #     vertex = vertices[index[i * 3]].copy()
                    #     vertex.extend(texture_uvs[index[i * 3 + 1]])
                    #     vertex.extend(normals[index[i * 3 + 2]])
                    #     buffer.append(vertex)
                    for i in range(3):
                        vertices[index[i * 3]].extend(texture_uvs[index[i * 3 + 1]])
                        vertices[index[i * 3]].extend(normals[index[i * 3 + 2]])
            f.close()
        averaged_vertex = []
        for vertex in vertices:
            pos = vertex[:3]
            uv_normal = np.array([0, 0, 0, 0, 0], dtype=np.float32)
            uvnnn = [np.array(vertex[3+5*j:8+5*j]) for j in range((len(vertex)-3)//5)]
            for partial in uvnnn:
                uv_normal += partial/len(uvnnn)
            averaged_vertex.append([*pos, *uv_normal])


        self.vertices = averaged_vertex
        # self.vertices = buffer
        # self.indices = [[i] for i in range(len(buffer))]

        return self.__call__()

    def __call__(self):
        self.vertices = np.array(self.vertices, dtype=np.float32)
        # self.vertices = self.vertices.reshape([self.vertices.shape[0]*self.vertices.shape[1], ])
        self.indices = np.array(self.indices, dtype=np.uint32)
        # self.indices = self.indices.reshape([self.indices.shape[0]*self.indices.shape[1], ])
        return self.vertices, self.indices

