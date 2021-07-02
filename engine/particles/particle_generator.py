from shaders_src import vertex_src, fragment_src
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import glfw
import numpy as np
import pyrr
from texture_manager import LoadTexture


class Particle:
    def __init__(self, position=[100, 100], velocity=[0, 0], life=1):
        self.position = np.array(position, dtype=np.float32) + \
                        np.array([np.random.normal()*3, np.random.normal()*3], dtype=np.float32)
        self.velocity = np.array(velocity, dtype=np.float32) + \
                        np.array([np.random.normal()*1, np.random.uniform()*30], dtype=np.float32)
        self.life = np.random.random()
        self.color = np.array([0.95, 0.5, 0.2, 1.0], dtype=np.float32)

    def respawn(self, position=[100, 100], velocity=[0, 6], life=1):
        self.position = np.array(position, dtype=np.float32) + \
                        np.array([np.random.normal()*3, np.random.normal()*3], dtype=np.float32)
        self.velocity = np.array(velocity, dtype=np.float32) + \
                        np.array([np.random.normal()*1, np.random.uniform()*30], dtype=np.float32)
        self.life = np.random.random()
        self.color = np.array([0.45, 0.9, 0.4, 1.0], dtype=np.float32)


particles = [Particle() for i in range(1000)]
dt = 0.1
vertex = np.array([0.0, 1.0, 0.0, 1.0,
                   1.0, 0.0, 1.0, 0.0,
                   0.0, 0.0, 0.0, 0.0,

                   0.0, 1.0, 0.0, 1.0,
                   1.0, 1.0, 1.0, 1.0,
                   1.0, 0.0, 1.0, 0.0], dtype=np.float32)

glfw.init()
window = glfw.create_window(400, 400, "particles", None, None)
glfw.make_context_current(window)

vao = glGenVertexArrays(1)
glBindVertexArray(vao)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertex.nbytes, vertex, GL_STATIC_DRAW)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 4, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
texture = LoadTexture("C:/PycharmProjects/OpenGL_Project/texture/ball.png")

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
glUseProgram(shader)
projection_loc = glGetUniformLocation(shader, "projection")
projection = pyrr.matrix44.create_orthogonal_projection_matrix(0.0, 400.0, 0.0, 400.0, 100.0, -100.0)
glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)
color_loc = glGetUniformLocation(shader, "color")
offset_loc = glGetUniformLocation(shader, "offset")


def draw_particles(position=[100, 100], velocity=[0, 6], life=1):
    offsets = []
    for step, particle in enumerate(particles):
        particle.life -= dt
        if particle.life <= 0:
            particle.respawn(position, velocity)
        else:
            particle.position += particle.velocity * dt
            particle.color[3] *= particle.life
            offsets.append([*particle.position, particle.color[2]])

    offsets = np.array(offsets, dtype=np.float32)
    glUniform4fv(color_loc, 1, particles[0].color)
    glUniform3fv(offset_loc, offsets.shape[0], offsets)
    glBindVertexArray(vao)
    glDrawArraysInstanced(GL_TRIANGLES, 0, 6, offsets.shape[0])


glClearColor(0.0, 0.1, 0.1, 1.0)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE)
start_time = 0.0
count = 0
fps = 30
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_particles()

    glfw.swap_buffers(window)
    count += 1
    current_time = glfw.get_time()
    if current_time - start_time >= 0.1:
        fps = count / (current_time - start_time)
        count = 0
        start_time = current_time
        glfw.set_window_title(window, "fps: {0:.4f}".format(fps))
