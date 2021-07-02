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
            self.camera_pos += self.camera_front * velocity
        if direction == "BACKWARD":
            self.camera_pos -= self.camera_front * velocity
        if direction == "LEFT":
            self.camera_pos -= self.camera_right * velocity
        if direction == "RIGHT":
            self.camera_pos += self.camera_right * velocity
        if direction == "UP":
            self.camera_pos += self.camera_up * velocity
        if direction == "DOWN":
            self.camera_pos -= self.camera_up * velocity

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
