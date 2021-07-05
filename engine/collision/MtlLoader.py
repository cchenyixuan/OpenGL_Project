import re
from PIL import Image
from OpenGL.GL import *


class LoadMaterial:
    def __init__(self):
        self.texture = None
        pass

    def __call__(self):
        return self.texture

    @staticmethod
    def search_data(data_values, data_type):
        compiled_re = {"Ns": re.compile(r"Ns ([0-9.-]*)", re.S),
                       "Ka": re.compile(r"Ka ([0-9.-]*) ([0-9.-]*) ([0-9.-]*)", re.S),
                       "Kd": re.compile(r"Kd ([0-9.-]*) ([0-9.-]*) ([0-9.-]*)", re.S),
                       "Ks": re.compile(r"Ks ([0-9.-]*) ([0-9.-]*) ([0-9.-]*)", re.S),
                       "Ke": re.compile(r"Ke ([0-9.-]*) ([0-9.-]*) ([0-9.-]*)", re.S),
                       "Ni": re.compile(r"Ni ([0-9.-]*)", re.S),
                       "d ": re.compile(r"d ([0-9.-]*)", re.S),
                       "il": re.compile(r"illum ([0-9.-]*)", re.S),
                       "ma": re.compile(r"map_Kd (.*)\n", re.S)}
        find_data = compiled_re[data_type]
        data = re.findall(find_data, data_values)
        if data_type == "ma":
            data = data[0]
        return data

    def load_file(self, filename):
        with open(filename, "r", encoding="utf8") as f:
            for row in f:
                if row[:2] == "ma":
                    image_dir = self.search_data(row, "ma")
            f.close()
        try:
            image = Image.open(image_dir)
            width, height = image.size
            image = image.convert("RGBA")
            image = image.tobytes()

            self.texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
            glGenerateMipmap(GL_TEXTURE_2D)
        except UnboundLocalError:
            pass

        return self.__call__()


