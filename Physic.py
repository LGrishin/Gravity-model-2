from math import sqrt, cos, sin, atan, pi


G = 6.67408 * (10 ** (-11))


def module1(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def module2(a, b):
    return sqrt(a * a + b * b)


def angle(x1, y1, x2, y2):
    if y1 == y2:
        if x1 > x2:
            return pi
        else:
            return 0
    if x1 == x2:
        if y1 > y2:
            return -pi / 2
        else:
            return pi / 2
    if x1 - x2 != 0:
        f = atan((y1 - y2) / (x1 - x2))

        if x1 <= x2 and y1 <= y2:
            return f
        if x1 > x2 and y1 > y2 or x1 >= x2 and y1 <= y2:
            return pi + f
        if x1 < x2 and y1 > y2:
            return f


def force(m1, m2, x1, y1, x2, y2):  # return F, Fx, Fy
    angle1 = angle(x1, y1, x2, y2)
    f = (G * (m1 * m2) / module1(x1, y1, x2, y2) ** 2)
    return f, f * cos(angle1), f * sin(angle1)


def coordinate(x0, vx, t):
    return x0 + vx * t


def velocity(vx, ax, t):
    return vx + ax * t


def acceleration(F, m):
    return F / m


def law_of_con_moment(m1, m2, v1, v2):
    return (v1 * m1 + v2 * m2) / (m1 + m2)


def perfectly_elastic_collision(m1, m2, v1, v2):
    v1 = (2 * m2 * v2 + v1 * (m1 - m2)) / (m1 + m2)
    v2 = (2 * m1 * v1 + v2 * (m2 - m1)) / (m1 + m2)
    return v1, v2


def first_space_speed(m, x1, y1, x2, y2):
    global G
    h = module1(x1, y1, x2, y2)
    return sqrt(G * (m / h))


