import pyrr
import numpy as np


class Camera:
    def __init__(self):
        self.position = pyrr.Vector3([0.0, 0.0, 10.0])
        self.front = pyrr.Vector3([0.0, 0.0, -1.0])
        self.up = pyrr.Vector3([0.0, 1.0, 0.0])
        
        self.face = pyrr.Vector3([0.0, 0.0, -1.0])
        self.right = pyrr.Vector3([1.0, 0.0, 0.0])
        self.right_hand = pyrr.Vector3([1.0, 0.0, 0.0])
        
        self.front_rotate_theta = 0.0
        self.up_rotate_theta = 0.0
        
        self.keyboard_pressed = 0
        self.key_w = 0
        self.key_e = 0
        self.key_a = 0
        self.key_d = 0
        self.left_button_lock = True
        self.right_button_lock = True
        self.cursor = [0.0, 0.0]
        
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
        x = self.cursor[0]/600 - 1
        y = -self.cursor[1]/400 + 1
        self.cursor_position = self.position + self.front + y*np.cross(self.right, self.front)/(np.sqrt(2)+1) + x*self.right/((np.sqrt(2)+1)/1.2*0.8)
        return self.cursor_position
    
    def outside_call(self):
        
        pass
    
    
    
"""
from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians, sqrt


class Camera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 1.0, 10.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])

        self.mouse_sensitivity = 20
        self.jaw = -90
        self.pitch = 0
        
        self.velocity = Vector3([0.0, 0.0, 0.0])

    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_front, self.camera_up)

    def process_mouse_movement(self, x_offset, y_offset, constrain_pitch=True):
        x_offset *= self.mouse_sensitivity
        y_offset *= self.mouse_sensitivity

        self.jaw += x_offset
        self.pitch += y_offset

        if constrain_pitch:
            if self.pitch > 90:
                self.pitch = 90
            if self.pitch < -90:
                self.pitch = -90

        self.update_camera_vectors()

    def update_camera_vectors(self):
        front = Vector3([0.0, 0.0, 0.0])
        front.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        front.y = sin(radians(self.pitch))
        front.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_front = vector.normalise(front)
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, Vector3([0.0, 1.0, 0.0])))
        self.camera_up = vector.normalise(vector3.cross(self.camera_right, self.camera_front))

    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            self.velocity.x = velocity
        if direction == "BACKWARD":
            self.velocity.x = -velocity
        if direction == "LEFT":
            self.velocity.y = -velocity
        if direction == "RIGHT":
            self.velocity.y = velocity
        if direction == "UP":
            self.velocity.z = velocity
        if direction == "DOWN":
            self.velocity.z = -velocity
            
    def move(self):
        self.camera_pos += self.velocity.x * self.camera_front
        self.camera_pos += self.velocity.y * self.camera_right
        self.camera_pos += self.velocity.z * self.camera_up

    def lock_x(self):
        self.camera_pos = Vector3([10.0, 0.0, 0.0])
        self.camera_front = Vector3([-1.0, 0.0, 0.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([0.0, 0.0, -1.0])
        self.jaw = -180
        self.pitch = 0

    def lock_z(self):
        self.camera_pos = Vector3([0.0, 0.0, 10.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        self.camera_right = Vector3([1.0, 0.0, 0.0])
        self.jaw = -90
        self.pitch = 0

    def lock_y(self):
        self.camera_pos = Vector3([0.0, 10.0, 0.0])
        self.camera_front = Vector3([0.0, -1.0, 0.0])
        self.camera_up = Vector3([-1.0, 0.0, 0.0])
        self.camera_right = Vector3([0.0, 0.0, -1.0])
        self.jaw = 180
        self.pitch = -90


class SphereCamera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 0.0, 100.0])
        self.camera_front = Vector3([0.0, 0.0, -1.0])  # vector.normalise(camera_pos)
        self.camera_up = Vector3(
            [0.0, 1.0, 0.0])  # vector.normalise((sin(theta)sin(phi), cos(theta), sin(theta)cos(phi)))
        self.camera_right = Vector3([1.0, 0.0, 0.0])  # vector.normalise(cross(pos, up))

        self.mouse_sensitivity = 20
        self.theta = 0
        self.phi = 0

    def get_view_matrix(self):
        return matrix44.create_look_at(self.camera_pos, self.camera_front, self.camera_up)

    def process_mouse_movement(self, x_offset, y_offset, constrain_pitch=True):
        x_offset *= self.mouse_sensitivity
        y_offset *= self.mouse_sensitivity

        self.phi += x_offset
        self.theta += y_offset

        if constrain_pitch:
            if self.theta > 90:
                self.theta = 90
            if self.theta < -90:
                self.theta = -90

        self.update_camera_vectors()

    def update_camera_vectors(self):
        distance = sqrt(self.camera_pos[0] ** 2 + self.camera_pos[1] ** 2 + self.camera_pos[2] ** 2)
        self.camera_pos = Vector3([distance * cos(radians(self.theta)) * sin(radians(self.phi)),
                                   distance * sin(radians(self.theta)),
                                   distance * cos(radians(self.theta)) * cos(radians(self.phi))])
        self.camera_front = -vector.normalise(self.camera_pos)
        self.camera_up = Vector3([0.0, 1.0, 0.0])
        #       self.camera_up = vector.normalise((sin(radians(self.theta))*sin(radians(self.phi)), \
        #                                          cos(radians(self.theta)), \
        #                                          -sin(radians(self.theta))*cos(radians(self.phi))))
        self.camera_right = vector.normalise(vector3.cross(self.camera_front, self.camera_up))

    def process_keyboard(self, direction, velocity):
        if direction == "FORWARD":
            self.camera_pos += self.camera_front * velocity
        if direction == "BACKWARD":
            self.camera_pos -= self.camera_front * velocity


class AxisCamera:
    def __init__(self):
        self.alpha, self.beta, self.gamma = 0.0, 0.0, 0.0
        self.camera_pos = Vector3([0.0, 0.0, 10])
        self.camera_front = Vector3([0.0, 0.0, -1.0])  # vector.normalise(camera_pos)
        self.camera_up = Vector3(
            [0.0, 1.0, 0.0])  # vector.normalise((sin(theta)sin(phi), cos(theta), sin(theta)cos(phi)))
        self.camera_right = Vector3([1.0, 0.0, 0.0])  # vector.normalise(cross(pos, up))

    def get_view_matrix(self):
        roll_x = matrix44.create_from_translation(Vector3([self.alpha, self.beta, self.gamma]))
        roll_y = matrix44.create_from_axis_rotation([0.0, 1.0, 10.0], self.beta)
        roll_z = matrix44.create_from_axis_rotation([0.0, 0.0, 10.0], self.gamma)
        roll = matrix44.multiply(matrix44.multiply(roll_x, roll_y), roll_z)
        return matrix44.multiply(matrix44.create_look_at(self.camera_pos, Vector3([0.0, 0.0, 0.0]), self.camera_up),
                                 roll_x)

    def process_keyboard(self, direction, velocity):
        if 0 <= velocity <= 0.001:
            return

        if direction == "+X":
            self.alpha += velocity
        if direction == "-X":
            self.alpha -= velocity
        if direction == "+Y":
            self.beta += velocity
        if direction == "-Y":
            self.beta -= velocity
        if direction == "+Z":
            self.gamma += velocity
        if direction == "-Z":
            self.gamma -= velocity
"""