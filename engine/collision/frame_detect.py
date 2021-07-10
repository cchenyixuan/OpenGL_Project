import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import pyrr
from polygon import *
from shader_src import vertex_src, fragment_src
from SAT import CheckCollision
from camera import *
import os

print(os.getcwd())
print(os.path.dirname(os.getcwd()))
os.chdir(os.path.dirname(os.getcwd()))

# %% global var an init 
MOUSE_PRESSED = False
KEYBOARD_PRESSED = False
WIDTH, HEIGHT = 1200, 800
glfw.init()
window = glfw.create_window(WIDTH, HEIGHT, "test collision", None, None)
glfw.make_context_current(window)

# %% init glfw model 
shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
glUseProgram(shader)

tetra = ModelObject(r".\resources\model\cube_group.obj")
tetra.set_attribute(scale=0.01, is_static=False)
ball = ModelObject(r".\resources\model\cube_group.obj")
ball.set_attribute(scale=0.1, rotation=[np.array([1.0, 1.0, 2.0]), 1])
cubes = {}
for i in range(1, 10):
    cubes[i] = ModelObject(r".\resources\model\ball.obj")
    cubes[i].set_attribute(scale=1 / i, offset=np.array([2 * i, 0, 0.0, 0.0]))
ground = ModelObject(r".\resources\model\ground.obj")
ground.set_attribute(offset=np.array([0.0, -8.0, 0.0, 0.0]))

skybox = ModelObject(r".\resources\model\skybox.obj")
skybox.set_attribute(scale=1000)

# TODO =======# should be put in camera #=======
cam = Camera()
model = pyrr.matrix44.create_identity()
model_loc = glGetUniformLocation(shader, "model")
glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
view = cam.create_view()
view_loc = glGetUniformLocation(shader, "view")
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
projection = pyrr.matrix44.create_perspective_projection_matrix(45.0, WIDTH / HEIGHT, 0.001, 10000)
projection_loc = glGetUniformLocation(shader, "projection")
glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)
mode_loc = glGetUniformLocation(shader, "mode")
glEnable(GL_DEPTH_TEST)
# TODO =======# should be put in camera #=======

glfw.window_hint(glfw.SAMPLES, 12)


def draw_polygon(polygon):
    # draw polygon
    glBindVertexArray(polygon.vao)
    glBindTexture(GL_TEXTURE_2D, polygon.texture)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, polygon.get_model_matrix())
    glDrawElements(GL_TRIANGLES, polygon.indices_length, GL_UNSIGNED_INT, None)
    # return to idV
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_identity())


def draw_polygon_with_frame(polygon):
    # draw polygon
    glBindVertexArray(polygon.vao)
    glBindTexture(GL_TEXTURE_2D, polygon.texture)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, polygon.get_model_matrix())
    glDrawElements(GL_TRIANGLES, polygon.indices_length, GL_UNSIGNED_INT, None)
    # draw frame
    glBindVertexArray(polygon.frame_vao)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, polygon.get_frame_model_matrix())
    glDrawElements(GL_TRIANGLES, polygon.frame_indices_length, GL_UNSIGNED_INT, None)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    # return to idV
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_identity())


# register glfw clb
def keyboard_operation_clb(window, key, scancode, action, mods):
    if key == glfw.KEY_W and action == glfw.PRESS:
        cam.keyboard_pressed += 1
        cam.key_w += 1
    if key == glfw.KEY_W and action == glfw.RELEASE:
        cam.keyboard_pressed -= 1
        cam.key_w -= 1
    if key == glfw.KEY_S and action == glfw.PRESS:
        cam.keyboard_pressed += 1
        cam.key_w -= 1
    if key == glfw.KEY_S and action == glfw.RELEASE:
        cam.keyboard_pressed -= 1
        cam.key_w += 1

    if key == glfw.KEY_Q and action == glfw.PRESS:
        cam.keyboard_pressed += 1
        cam.key_e -= 1
    if key == glfw.KEY_Q and action == glfw.RELEASE:
        cam.keyboard_pressed -= 1
        cam.key_e += 1
    if key == glfw.KEY_E and action == glfw.PRESS:
        cam.keyboard_pressed += 1
        cam.key_e += 1
    if key == glfw.KEY_E and action == glfw.RELEASE:
        cam.keyboard_pressed -= 1
        cam.key_e -= 1

    if key == glfw.KEY_A and action == glfw.PRESS:
        cam.keyboard_pressed += 1
        cam.front_rotate_theta += 0.004
    if key == glfw.KEY_A and action == glfw.RELEASE:
        cam.keyboard_pressed -= 1
        cam.front_rotate_theta -= 0.004
    if key == glfw.KEY_D and action == glfw.PRESS:
        cam.keyboard_pressed += 1
        cam.front_rotate_theta -= 0.004
    if key == glfw.KEY_D and action == glfw.RELEASE:
        cam.keyboard_pressed -= 1
        cam.front_rotate_theta += 0.004

    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        if cam.jump == 0:
            cam.jump = 99
            cam.jump_situation = np.array([cam.key_w, cam.key_e])


def mouse_operation_clb(window, button, action, mods):
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        cam.left_button_lock = False
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE:
        cam.left_button_lock = True
    if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        cam.right_button_lock = False
    if button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.RELEASE:
        cam.right_button_lock = True


def mouse_position_clb(window, xpos, ypos):
    if cam.left_button_lock and cam.right_button_lock:
        cam.cursor = [xpos, ypos]
    else:
        dx = cam.cursor[0] - xpos
        dy = cam.cursor[1] - ypos
        cam.cursor = [xpos, ypos]
        if cam.front[1] <= -0.9 and dy < 0.0:
            dy = 0.0
        if cam.front[1] >= 0.9 and dy > 0.0:
            dy = 0.0
        cam.mouse_movement(dx, dy)
        # move tetra with mouse
        cam.right = pyrr.Vector3([-cam.front[2], 0, cam.front[0]])
        cam.right /= np.linalg.norm(cam.right)

    if not cam.right_button_lock:
        cam.face = pyrr.Vector3([cam.front[0], 0, cam.front[2]])
        cam.face /= np.linalg.norm(cam.face)
        cam.right_hand = pyrr.Vector3([-cam.front[2], 0, cam.front[0]])
        cam.right_hand /= np.linalg.norm(cam.right_hand)


def collision_detect():
    pass


sat = CheckCollision()
glfw.set_key_callback(window, keyboard_operation_clb)
glfw.set_mouse_button_callback(window, mouse_operation_clb)
glfw.set_cursor_pos_callback(window, mouse_position_clb)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, cam.create_view())
    # skybox.set_attribute(offset=cam.position)

    draw_polygon_with_frame(skybox)

    tetra.set_attribute(offset=cam.get_cursor_position(), rotation=[np.array([glfw.get_time(), glfw.get_time()*2, glfw.get_time()*3]), glfw.get_time()])
    sat.load_polygon_frames(tetra, ball)
    if sat.separating_axis_theorem():
        glUniform1i(mode_loc, 1)
    sat.__init__()
    draw_polygon_with_frame(ball)
    for i in range(1, 10):
        sat.load_polygon_frames(tetra, cubes[i])
        if sat.separating_axis_theorem():
            glUniform1i(mode_loc, 1)
        sat.__init__()
    draw_polygon_with_frame(tetra)
    glUniform1i(mode_loc, 0)

    # draw_polygon_with_frame(cube)

    for i in range(1, 10):
        # cubes[i].set_attribute(rotation=[np.array([1.0, 0.0, 0.0]), glfw.get_time()])
        draw_polygon_with_frame(cubes[i])
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    draw_polygon(ground)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glfw.swap_buffers(window)

glfw.terminate()
