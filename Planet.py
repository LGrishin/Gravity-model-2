from Physic import *
from collections import deque


class Planet:
    time_interval = 0.1
    x0 = 0
    y0 = 0
    Vx = 0
    Vy = 0
    V = 0
    Ax = 0
    Ay = 0
    A = 0
    Fx = 0
    Fy = 0
    F = 0
    m = 0
    r = 10
    orbital_velocity = 0
    escape_velocity = 0
    Col = False
    color = (255, 0, 0)
    Vel_vec_coords = (0, 0)
    trajectory = deque()
    trajectory_depth = 1000

    def __init__(self, t=0.1):
        self.time_interval = t

    def time_interval_p(self, t):
        self.time_interval += t

    def time_interval_m(self, t):
        self.time_interval *= t

    def coordinates(self, x0, y0):
        self.x0, self.y0 = x0, y0
        self.Vel_vec_coords = (x0, y0)

    def collision_true(self):
        self.Col = True

    def velocity(self, Vx, Vy):
        self.Vx, self.Vy = Vx, Vy
        self.V = module2(self.Vx, self.Vy)

    def force_sum(self, Fx, Fy):
        self.Fx += Fx
        self.Fy += Fy
        self.F = module2(self.Fx, self.Fy)

    def force(self, Fx, Fy):
        self.Fx, self.Fy = Fx, Fy
        self.F = module2(Fx, Fy)

    def acceleration(self, Ax, Ay):
        self.Ax, self.Ay = Ax, Ay
        self.A = module2(Ax, Ay)

    def first_space_speed(self, x1, y1):
        self.orbital_velocity = first_space_speed(self.m, self.x0, self.y0, x1, y1)
        self.escape_velocity = sqrt(2) * first_space_speed(self.m, self.x0, self.y0, x1, y1)

    def update_planet(self):
        self.force(self.Fx, self.Fy)
        self.acceleration(self.Fx / self.m, self.Fy / self.m)
        self.velocity(velocity(self.Vx, self.Ax, self.time_interval), velocity(self.Vy, self.Ay, self.time_interval))
        self.coordinates(coordinate(self.x0, self.Vx, self.time_interval), coordinate(self.y0,
                                                                                      self.Vy, self.time_interval))
        if len(self.trajectory) > self.trajectory_depth:
            self.trajectory.popleft()
            self.trajectory.append(self.get_coordinates())
        else:
            self.trajectory.append(self.get_coordinates())

    def velocity_vector_coord(self, v):
        self.Vel_vec_coords = v

    def get_coordinates(self):
        return [self.x0, self.y0]

    def get_velocity_vet(self):
        return [self.Vel_vec_coords[0], self.Vel_vec_coords[1]]
