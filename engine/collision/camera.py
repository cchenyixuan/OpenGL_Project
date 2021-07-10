import pyrr
import numpy as np


class Camera:
    def __init__(self):
        # base attribute
        self.position = pyrr.Vector3([0.0, 0.0, 10.0])
        self.front = pyrr.Vector3([0.0, 0.0, -1.0])
        self.up = pyrr.Vector3([0.0, 1.0, 0.0])
        self.right = pyrr.Vector3([1.0, 0.0, 0.0])
        # role attribute
        self.face = pyrr.Vector3([0.0, 0.0, -1.0])
        self.right_hand = pyrr.Vector3([1.0, 0.0, 0.0])
        # rotate value
        self.front_rotate_theta = 0.0
        self.up_rotate_theta = 0.0
        # devices callback
        self.keyboard_pressed = 0
        self.key_w = 0
        self.key_e = 0
        self.key_a = 0
        self.key_d = 0
        self.left_button_lock = True
        self.right_button_lock = True
        self.cursor = [0.0, 0.0]
        self.cursor_position = self.position + self.front
        # special status
        self.jump = 0
        self.jump_situation = np.array([self.key_w, self.key_e])
        self.jump_model = [-3*(-1+i/100)**2 - 3*(-1+i/100) for i in range(100)]
        
    def create_view(self):
        self.movement()
        return pyrr.matrix44.create_look_at(self.position, self.position+self.front, self.up)
    
    def movement(self):
        if self.jump:
            self.position[1] = self.jump_model[self.jump]
            self.jump -= 1
            self.position += self.jump_situation @ np.array([self.face, self.right]) *0.05
            if self.front_rotate_theta != 0.0:
                self.front = pyrr.matrix33.multiply(pyrr.matrix33.create_from_y_rotation(self.front_rotate_theta), self.front)
                self.right = pyrr.Vector3([-self.front[2], 0, self.front[0]])
                self.right /= np.linalg.norm(self.right)
    
            return
        if not self.keyboard_pressed:
            return
        else:
            self.position += np.array([self.key_w, self.key_e]) @ np.array([self.face, self.right]) *0.05
            if self.front_rotate_theta != 0.0:
                self.front = pyrr.matrix33.multiply(pyrr.matrix33.create_from_y_rotation(self.front_rotate_theta), self.front)
                self.right = pyrr.Vector3([-self.front[2], 0, self.front[0]])
                self.right /= np.linalg.norm(self.right)

    def mouse_movement(self, dx, dy):
        if dx != 0.0 or dy != 0.0:
            self.front = pyrr.matrix33.multiply(pyrr.matrix33.create_from_y_rotation(dx/300), self.front)
            self.front = pyrr.matrix33.multiply(pyrr.matrix33.create_from_axis_rotation(pyrr.Vector3([self.front[2], 0.0, -self.front[0]]), dy/300), self.front)
    
    def get_cursor_position(self):
        # translate from [0,0,WIDTH,HEIGHT] to [-1, 1, 1, -1]
        x = self.cursor[0]/600 - 1
        y = -self.cursor[1]/400 + 1
        self.cursor_position = self.position + self.front*3 + y*np.cross(self.right, self.front*3)/(np.sqrt(2)+1) + x*self.right*3/((np.sqrt(2)+1)/1.2*0.8)
        return self.cursor_position
    
    def outside_call(self):
        
        pass
