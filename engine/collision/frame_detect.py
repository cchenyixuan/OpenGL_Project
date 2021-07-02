import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import pyrr
from polygon import *
from shader_src import vertex_src, fragment_src
from SAT import CheckCollision
from camera import SphereCamera

MOUSE_PRESSED = False

cam = SphereCamera()

glfw.init()
window = glfw.create_window(800, 800, "test collision", None, None)
glfw.make_context_current(window)
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
glUseProgram(shader)

tetra = ModelObject(r"C:\PycharmProjects\OpenGL_Project\engine\resources\model\tetra.obj")
tetra.is_static = False
ball = ModelObject()
cube = ModelObject(r"C:\PycharmProjects\OpenGL_Project\engine\resources\model\squared_cube.obj")
cube.offset = np.array([-1, -1, 0.0, 0.0])
cube.is_static = False
cube(0.1, cube.offset, False)


# TODO =======# should be put in camera #=======
model = pyrr.matrix44.create_from_x_rotation(0.0)
model_loc = glGetUniformLocation(shader, "model")
glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
view = cam.get_view_matrix()
view_loc = glGetUniformLocation(shader, "view")
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
projection = pyrr.matrix44.create_perspective_projection_matrix(45.0, 1.0, 0.001, 1000)
projection_loc = glGetUniformLocation(shader, "projection")
glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)
glEnable(GL_DEPTH_TEST)
# TODO =======# should be put in camera #=======


def draw_polygon(polygon, scale=1.0):
    if polygon.is_static:
        glUniform1i(glGetUniformLocation(shader, "is_static"), 1)
    else:
        glUniform1i(glGetUniformLocation(shader, "is_static"), 0)
        offset_loc = glGetUniformLocation(shader, "offset")
        glUniform4fv(offset_loc, 1, polygon.offset)
    glBindVertexArray(polygon.vao)
    glDrawElements(GL_TRIANGLES, polygon.indices_length, GL_UNSIGNED_INT, None)


def draw_polygon_with_frame(polygon, scale=1.0):
    if polygon.is_static:
        glUniform1i(glGetUniformLocation(shader, "is_static"), 1)
    else:
        glUniform1i(glGetUniformLocation(shader, "is_static"), 0)
        offset_loc = glGetUniformLocation(shader, "offset")
        glUniform4fv(offset_loc, 1, polygon.offset)
    model = pyrr.matrix44.create_from_scale(pyrr.Vector3([scale]*3))
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    polygon(scale, polygon.offset, polygon.is_static)
    glBindVertexArray(polygon.vao)
    glDrawElements(GL_TRIANGLES, polygon.indices_length, GL_UNSIGNED_INT, None)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBindVertexArray(polygon.frame_vao)
    glDrawElements(GL_TRIANGLES, polygon.frame_indices_length, GL_UNSIGNED_INT, None)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


def mouse_position_clb(_, x_pos, y_pos):
    global MOUSE_PRESSED
    # collision check
    x_pos, y_pos = x_pos / 400 - 1, -y_pos / 400 + 1
    offset = pyrr.Vector4([x_pos, y_pos, 0.0, 0.0]) * 10 / (np.sqrt(2) + 1)
    tetra.offset = offset
    sat1 = CheckCollision()
    sat1.load_polygons(tetra, ball)
    sat2 = CheckCollision()
    sat2.load_polygons(tetra, cube)
    if sat1.separating_axis_theorem() or sat2.separating_axis_theorem():
        mode_loc = glGetUniformLocation(shader, "mode")
        glUniform1i(mode_loc, 1)
    else:
        mode_loc = glGetUniformLocation(shader, "mode")
        glUniform1i(mode_loc, 0)
    # update camera status
    try:
        x_offset = x_pos - cam.start[0]
        y_offset = y_pos - cam.start[1]
        if MOUSE_PRESSED:
            cam.process_mouse_movement(-x_offset, -y_offset)
            glUniformMatrix4fv(view_loc, 1, GL_FALSE, cam.get_view_matrix())

    except:
        pass
    cam.start = [x_pos, y_pos]


def mouse_event_clb(_, button, action, mods):
    global MOUSE_PRESSED
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        MOUSE_PRESSED = True
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
        MOUSE_PRESSED = False


glfw.set_cursor_pos_callback(window, mouse_position_clb)
glfw.set_mouse_button_callback(window, mouse_event_clb)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_polygon_with_frame(tetra)

    draw_polygon_with_frame(ball)

    draw_polygon_with_frame(cube)

    glfw.swap_buffers(window)

glfw.terminate()
