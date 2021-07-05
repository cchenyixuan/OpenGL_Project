import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
import pyrr
from polygon import *
from shader_src import vertex_src, fragment_src
from SAT import CheckCollision
from camera import *

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

tetra = ModelObject(r"C:\PycharmProjects\OpenGL_Project\engine\resources\model\tetra.obj", 0.1)
tetra.is_static = False
ball = ModelObject()
cube = ModelObject(r"C:\PycharmProjects\OpenGL_Project\engine\resources\model\squared_cube.obj")
cube.offset = np.array([10, 10, 0.0, 0.0])
cube.is_static = False
cube(0.1, cube.offset, False)
cubes = {}
for i in range(1, 10):
    cubes[i] = ModelObject()
    cubes[i](1.0, np.array([2*i, 0, 0.0, 0.0]), False)
ground = ModelObject(r"C:\PycharmProjects\OpenGL_Project\engine\resources\model\ground.obj")
ground(1.0, np.array([0.0, -2.0, 0.0, 0.0]), False)

skybox = ModelObject(r"C:\PycharmProjects\OpenGL_Project\engine\resources\model\skybox.obj", 100)

# TODO =======# should be put in camera #=======
cam = Camera()
model = pyrr.matrix44.create_from_x_rotation(0.0)
model_loc = glGetUniformLocation(shader, "model")
glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
view = cam.create_view()
view_loc = glGetUniformLocation(shader, "view")
glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
projection = pyrr.matrix44.create_perspective_projection_matrix(45.0, WIDTH/HEIGHT, 0.001, 10000)
projection_loc = glGetUniformLocation(shader, "projection")
glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)
mode_loc = glGetUniformLocation(shader, "mode")
glEnable(GL_DEPTH_TEST)
# TODO =======# should be put in camera #=======

glfw.window_hint(glfw.SAMPLES, 12)
def draw_polygon(polygon, scale=1.0):
    if polygon.is_static:
        glUniform1i(glGetUniformLocation(shader, "is_static"), 1)
    else:
        glUniform1i(glGetUniformLocation(shader, "is_static"), 0)
        offset_loc = glGetUniformLocation(shader, "offset")
        glUniform4fv(offset_loc, 1, polygon.offset)
    glBindVertexArray(polygon.vao)
    try:
        glBindTexture(GL_TEXTURE_2D, polygon.texture)
    except:
        pass
    glDrawElements(GL_TRIANGLES, polygon.indices_length, GL_UNSIGNED_INT, None)


def draw_polygon_with_frame(polygon, scale=1.0):
    if polygon.is_static:
        glUniform1i(glGetUniformLocation(shader, "is_static"), 1)
    else:
        glUniform1i(glGetUniformLocation(shader, "is_static"), 0)
        offset_loc = glGetUniformLocation(shader, "offset")
        glUniform4fv(offset_loc, 1, polygon.offset)
    glBindVertexArray(polygon.vao)
    try:
        glBindTexture(GL_TEXTURE_2D, polygon.texture)
    except:
        pass
    glDrawElements(GL_TRIANGLES, polygon.indices_length, GL_UNSIGNED_INT, None)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_x_rotation(0.0))
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    glBindVertexArray(polygon.frame_vao)
    glDrawElements(GL_TRIANGLES, polygon.frame_indices_length, GL_UNSIGNED_INT, None)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)


# regist glfw clb
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
    if cam.left_button_lock == True and cam.right_button_lock == True:
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
    
    if cam.right_button_lock == False:
        cam.face = pyrr.Vector3([cam.front[0], 0, cam.front[2]])
        cam.face /= np.linalg.norm(cam.face)
        cam.right_hand = pyrr.Vector3([-cam.front[2], 0, cam.front[0]])
        cam.right_hand /= np.linalg.norm(cam.right_hand)
    
    
            
    
sat = CheckCollision()
glfw.set_key_callback(window, keyboard_operation_clb)
glfw.set_mouse_button_callback(window, mouse_operation_clb)
glfw.set_cursor_pos_callback(window, mouse_position_clb)

while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, cam.create_view())
    
    draw_polygon(skybox)
    
    tetra.offset = cam.get_cursor_position()
    sat.load_polygons(tetra, ball)
    if sat.separating_axis_theorem():
        glUniform1i(mode_loc, 1)
    sat.__init__()
    for i in range(1, 10):
        sat.load_polygons(tetra, cubes[i])
        if sat.separating_axis_theorem():
            glUniform1i(mode_loc, 1)
        sat.__init__()
        

    draw_polygon_with_frame(tetra)
    glUniform1i(mode_loc, 0)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_x_rotation(glfw.get_time()))
    draw_polygon_with_frame(ball)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_x_rotation(0.0))

    # draw_polygon_with_frame(cube)


    for i in range(1, 10):
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_x_rotation(i*glfw.get_time()))
        draw_polygon_with_frame(cubes[i])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_x_rotation(0.0))
    # glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    draw_polygon(ground)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    glfw.swap_buffers(window)

glfw.terminate()

