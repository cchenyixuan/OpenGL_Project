src = """
import pyrr
scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([1/200, 1/200, 0.0]))
rotation = pyrr.matrix44.create_from_x_rotation(np.pi)

model = rotation @ scale

def mouse_position_clb(window, x, y):
    x, y, _, _ = model @ pyrr.Vector4([x, y, 0.0, 0.0]) + pyrr.Vector4([-1.0, 1.0, 0.0, 0.0])
    if -0.2 <= x <= 0.2 and -0.2 <= y <= 0.2:
        cursor_loc = glGetUniformLocation(shader, "cursor")
        glUniform1i(cursor_loc, 1)
    else:
        cursor_loc = glGetUniformLocation(shader, "cursor")
        glUniform1i(cursor_loc, 0)
        
    
    
glfw.set_cursor_pos_callback(window, mouse_position_clb)
"""

src_1 = """
import polygon
import pyrr
scale = pyrr.matrix44.create_from_scale(pyrr.Vector3([1/200, 1/200, 0.0]))
rotation = pyrr.matrix44.create_from_x_rotation(np.pi)
from SAT import *

model = rotation @ scale

def mouse_position_clb(window, x, y):
    global little_square_vao
    
    
    x, y, _, _ = model @ pyrr.Vector4([x, y, 0.0, 0.0]) + pyrr.Vector4([-1.0, 1.0, 0.0, 0.0])
    
    ls = polygon.LittleSquare()
    ls.vertices = [[-0.3+x, 0.1+y, 0.0], [-0.1+x, -0.1+y, 0.0], [-0.1+x, 0.1+y, 0.0], 
                   [0.1+x, -0.1+y, 0.0], [0.1+x, 0.1+y, 0.0], [0.2+x, 0.0+y, 0.0]]
    ls.normal = [[1, 0, 0], [0, 1, 0], [1, 1, 0], [1, -1, 0]]
    little_square = np.array(ls.vertices, dtype=np.float32)
    little_square = little_square.reshape([little_square.shape[0]*little_square.shape[1], ])
    little_square_vao = glGenVertexArrays(1)
    glBindVertexArray(little_square_vao)
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, little_square.nbytes, little_square, GL_STATIC_DRAW)
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 12, ctypes.c_void_p(0))
    
    
    sat = CheckCollision()
    # sat.load_polygon_a(polygon.ModelObject())
    # sat.load_polygon_b(ls)
    sat.load_polygons(polygon.Triangle(), ls)
    if sat.pre_check() == True:        
        if sat.separating_axis_theorem() == True:
            cursor_loc = glGetUniformLocation(shader, "cursor")
            glUniform1i(cursor_loc, 1)
        else:
            cursor_loc = glGetUniformLocation(shader, "cursor")
            glUniform1i(cursor_loc, 0)
    else:
            
        
        sat = CheckCollision()
        sat.load_polygon_a(polygon.ModelObject())
        sat.load_polygon_b(ls)    
        if sat.pre_check() == True:
            if sat.separating_axis_theorem() == True:
                cursor_loc = glGetUniformLocation(shader, "cursor")
                glUniform1i(cursor_loc, 1)
        else:
            cursor_loc = glGetUniformLocation(shader, "cursor")
            glUniform1i(cursor_loc, 0)
                
    
        

glfw.set_cursor_pos_callback(window, mouse_position_clb)
    
    

"""