import math
from constant import GREY, TRACK_WIDTH, WHITE


def circular_arc(center: tuple[float, float], start_angle: float,
                 finish_angle: float, steps: int,
                 radius: float, width: float):
    inner_points = []
    outer_points = []

    delta_theta = finish_angle - start_angle
    theta = start_angle

    outer_radius = int(radius + (width / 2))
    inner_radius = int(radius - (width / 2))

    for i in range(0, steps + 1):
        outer_points.append((
            int(center[0] + (outer_radius * math.cos(math.radians(theta)))),
            int(center[1] - (outer_radius * math.sin(math.radians(theta))))
        ))

        theta += delta_theta / steps

    theta = start_angle

    for i in range(0, steps + 1):
        inner_points.append((
            int(center[0] + (inner_radius * math.cos(math.radians(theta)))),
            int(center[1] - (inner_radius * math.sin(math.radians(theta))))
        ))

        theta += delta_theta / steps

    return (outer_points, inner_points)


def rect_points(x, y, width, height):
    return [(x, y), (x, y + height), (x + width, y + height), (x + width, y)]


def checkerboard_pattern(x, y, width, height, box_size):
    assert (width % box_size == 0) and (height % box_size == 0)

    boxes = []
    for i in range(0, int(width / box_size)):
        for j in range(0, int(height / box_size)):
            boxes.append([GREY if (i + j) % 2 == 0 else WHITE,
                         *rect_points(x + (i * box_size), y + (j * box_size),
                         box_size, box_size)])
    return boxes


def grid_slots(x: float, y: float, slot_size: int,
               slot_padding: int, n: int) -> list[list[tuple[float, float]]]:
    assert (slot_size * 2) + (slot_padding * 3) == TRACK_WIDTH

    slots = []
    for i in range(0, n):
        x_offset = (slot_padding + slot_size) * i
        y_offset = (slot_padding + slot_size) * (i % 2)
        slots.append([
            (x + slot_padding + slot_size + x_offset,
             y + slot_padding + y_offset),
            (x + slot_padding + x_offset,
             y + slot_padding + y_offset),
            (x + slot_padding + x_offset,
             y + slot_padding + slot_size + y_offset),
            (x + slot_padding + slot_size + x_offset,
             y + slot_padding + slot_size + y_offset)
        ])

    return slots


# class Bspline(object):
#     def __init__(self, P, t, k = None):
#         """
#         construct Bspline object
#         uses Cox-DeBoor

#         P == vector of two-dimensional control points
#         t == vector of non-decreasing real numbers
#         k == degree of curve

#         identities:
#         P = (P[0], ... P[n]); n = len(P) - 1
#         t = (t[0], ... t[m]); m = len(t) - 1
#         k = m - n - 1
#         m = n + k + 1
#         n = m - k - 1
#         """
#         m, n = len(t) - 1, len(P) - 1
#         if not k: k = m - n - 1
#         else: assert m == n + k + 1
#         self.k, self.t = k, t
#         (self.X, self.Y) = P # points in X, Y components
#         self._deboor() # evaluate

#     def __call__(self, t_):
#         """
#         S(t) = sum(b[i][k](t) * P[i] for i in xrange(0, n))
#         domain: t in [t[k - 1], t[n + 1]]

#         returns point on Bspline at t_
#         """
#         k, t = self.k, self.t
#         m = len(t) - 1
#         n = m - k - 1
#         assert t[k - 1] <= t_ <= t[n + 1] # t in [t[k - 1], t[n + 1]]
#         X, Y, b = self.X, self.Y, self.b
#         x, y, _n = 0, 0, range(n + 1) # initial return values,
# iterator over P
#         for i in _n:
#             b_i = b[i][k](t_)
#             x += X[i] * b_i
#             y += Y[i] * b_i
#         return x, y

#     def _deboor(self):
#         # de Boor recursive algorithm
#         # S(t) = sum(b[i][k](t) * P[i] for i in xrange(0, n))
#         #
#         # b[i][k] = {
#         #     if k == 0:
#         #         t[i] <= t_ < t[i+1]
#         #     else:
#         #         a[i][k](t)*b[i][k-1](t)+(1-a[i+1][k](t))*b[i+1][k-1](t)
#         # }
#         #
#         # a[i][k] = {
#         #     if t[i] == t[i+k]:
#         #         0
#         #     else:
#         #         (t_-t[i])/(t[i+k]-t[i])
#         # }
#         #
#         # NOTE: for b[i][k](t), must iterate to t[:-1];
#         # the number of [i, i + 1) spans in t
#         k, t = self.k, self.t
#         m = len(t) - 1 # iterate to t[:-1]
#         a, b, _k_, _m_ = [], [], range(k + 1), range(m)
#         for i in _m_:
#             a.append([]); b.append([]) # a[i]; b[i]
#             for k in _k_:
#                 a[i].append(None) # a[i][k]
#                 # if k == 0: b[i][k](t) is a step
#                   function in [t[i], t[i + 1])
#                 if k == 0: b[i].append(lambda t_, i=i: t[i] <= t_ < t[i + 1])
#                 # if m < i + k: b[i][k](t) undefined
#                 elif m < i + k: b[i].append(lambda t_: False)
#                 # else: calculate b[i][k](t)
#                 else:
#                     # if t[i] == t[i + k]: a[i][k] undefined
#                     if t[i] == t[i + k]: a[i][k] = lambda t_: False
#                     # else: calculate a[i][k](t)
#                     else:
#                         # a[i][k](t) = (t_ - t[i]) / (t[i + k] - t[i])
#                         a[i][k] = lambda t_, i=i, k=k: ((t_ - t[i]) /
#                                                         (t[i + k] - t[i]))
#                     # b[i][k](t) = a[i][k](t) * b[i][k - 1](t) +
#                     #              (1 - a[i + 1][k](t)) * b[i + 1][k - 1](t)
#                     b[i].append(lambda t_, i=i, k=k:
#                                 a[i][k](t_) * b[i][k - 1](t_) +
#                                 (1 - a[i + 1][k](t_)) * b[i + 1][k - 1](t_))
#         self.b = b

#     def insert(self, t_):
#         """
#         Q[i] = (1 - a[i][k]) * P[i] + a[i][k] * P[i]
#         domain: t in (t[0], t[m])

#         insert new control point at t_
#         """
#         t = self.t
#         assert t[0] < t_ < t[-1] # t_ in (t[0], t[m])
#         X, Y, k = self.X, self.Y, self.k
#         m = len(t) - 1
#         _t_ = range(m + 1)
#         # find the span containing t_
#         for i in _t_:
#             if t[i] <= t_ < t[i + 1]: break
#         assert not i < k + 1 and not i > m - k + 1 # i not in clamp
#         Q_x, Q_y = [], [] # new control points
#         # iterate over replaced control points
#         # set new control points
#         for j in range(i - k + 1, i + 1):
#             a_j = (t_ - t[j]) / (t[j + k] - t[j])
#             Q_x.append((1 - a_j) * X[j - 1] + a_j * X[j])
#             Q_y.append((1 - a_j) * Y[j - 1] + a_j * Y[j])
#         Q_x, Q_y = tuple(Q_x), tuple(Q_y)
#         self.t = t[:i + 1] + [t_] + t[i + 1:]
#         self.X = X[:i - k + 1] + Q_x + X[i:]
#         self.Y = Y[:i - k + 1] + Q_y + Y[i:]
#         self._deboor() # re-evaluate
