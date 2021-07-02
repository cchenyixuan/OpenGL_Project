import glfw
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
from outside_links import src, src_1

vertex_src = """
# version 440 core
layout(location=0) in vec3 pos;
void main(){
    gl_Position = vec4(pos, 1.0);
}
"""
fragment_src = """
# version 440 core
uniform int cursor;
out vec4 color;
void main(){
    switch(cursor){
        case 0:
            color = vec4(1.0, 1.0, 1.0, 1.0);
            break;
        case 1:
            color = vec4(1.0, 0.0, 1.0, 1.0);
            break;
    }
    
}
"""

glfw.init()
window = glfw.create_window(400, 400, "test collision", None, None)
glfw.make_context_current(window)
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
glUseProgram(shader)
exec(src_1)

square = np.array([-0.2, -0.2, 0.0, -0.2, 0.2, 0.0, 0.2, -0.2, 0.0, 0.2, 0.2, 0.0], dtype=np.float32)
triangle = np.array([-0.3, -0.3, 0.0, -0.25, -0.3, 0.0, -0.25, -0.25, 0.0], dtype=np.float32)
import polygon
square = polygon.ModelObject()
square.vertices = np.array(square.vertices)

square_vao = glGenVertexArrays(1)
glBindVertexArray(square_vao)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, square.vertices.nbytes, square.vertices, GL_STATIC_DRAW)
ebo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, square.indices.nbytes, square.indices, GL_STATIC_DRAW)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
triangle_vao = glGenVertexArrays(1)
glBindVertexArray(triangle_vao)
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, triangle.nbytes, triangle, GL_STATIC_DRAW)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

little_square_vao = None
while not glfw.window_should_close(window):
    glfw.poll_events()

    glClear(GL_COLOR_BUFFER_BIT)

    glBindVertexArray(square_vao)
    glDrawElements(GL_TRIANGLES, square.indices.shape[0], GL_UNSIGNED_INT, None)
    glBindVertexArray(triangle_vao)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    try:
        glBindVertexArray(little_square_vao)
        glDrawArrays(GL_TRIANGLE_STRIP, 0, 6)
    except:
        pass

    glfw.swap_buffers(window)

glfw.terminate()
