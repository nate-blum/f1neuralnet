import numpy as np
from pygame import gfxdraw
from f1neuralnet.models import Car
from f1neuralnet.constant import *
from f1neuralnet.f1_graphics import checkerboard_pattern, circular_arc, grid_slots
from f1neuralnet.tracks import Track
from shapely import Polygon, Point


class OvalTrack(Track):
    def __init__(self, x, y, width, height):
        self.x, self.y, self.width, self.height = x, y, width, height

        self.straight_left = int(self.x + (self.width / 4))
        self.straight_right = int(self.x + ((self.width * 3) / 4))
        self.turn_radius = int((self.height / 2) - (TRACK_WIDTH / 2))

        self.points = self.compute_points()
        self.polygon = Polygon(self.points[0], (self.points[1],))

        self.start_finish = checkerboard_pattern(
            (self.x + (self.width / 2)) - (START_FINISH_WIDTH / 2),
            (self.y + self.height) - TRACK_WIDTH,
            START_FINISH_WIDTH, TRACK_WIDTH, 10)
            
        self.start_finish_rect = pygame.Rect(((self.x + (self.width / 2)) - (START_FINISH_WIDTH / 2),
                                              (self.y + self.height) - TRACK_WIDTH), (START_FINISH_WIDTH, TRACK_WIDTH))

        self.grid_slots_pos = ((self.x + (self.width / 2) + (START_FINISH_WIDTH / 2)),
                               self.y + (self.height - TRACK_WIDTH))

        self.grid_slots = grid_slots(
            *self.grid_slots_pos,
            GRID_SLOT_SIZE, GRID_SLOT_PADDING, 4
        )

    def distance_to_next_turn(self, car: Car):
        if car.position[0] <= self.straight_left or self.straight_right <= car.position[0]:
            return 0
        else:
            return self.straight_right - car.position[0] if car.position[1] < (WINDOW_HEIGHT / 2) else car.position[0] - self.straight_left

    def current_turn_radius(self, car: Car):
        if car.position[0] <= self.straight_left:
            return self.turn_radius
        elif car.position[0] >= self.straight_right:
            return -self.turn_radius
        else:
            return 0

    def is_car_within_track_limits(self, car: Car):
        return any([self.polygon.contains(Point(p)) for p in car.get_rect_coords()])

    def are_car_front_wheels_touching_start_finish(self, car: Car):
        return any([self.start_finish_rect.collidepoint(*p) for p in car.get_front_wheels()])

    def draw(self, screen):
        gfxdraw.aapolygon(screen, self.points[0] + self.points[1], ASPHALT)
        gfxdraw.filled_polygon(screen, self.points[0] + self.points[1], ASPHALT)

        for box in self.start_finish:
            gfxdraw.filled_polygon(screen, box[1:], box[0])

        for slot in self.grid_slots:
            pygame.draw.lines(screen, WHITE, False, slot, width=5)

    def compute_points(self):
        turn_y = self.y + int(self.height / 2)

        (outer_left_turn, inner_left_turn) = circular_arc((self.straight_left, turn_y), 90, 270, 50, self.turn_radius, TRACK_WIDTH)  # left side 180-degree turn
        (outer_right_turn, inner_right_turn) = circular_arc((self.straight_right, turn_y), -90, 90, 50, self.turn_radius, TRACK_WIDTH)  # right side 180-degree turn

        return outer_left_turn + outer_right_turn + [outer_left_turn[0]], inner_left_turn + inner_right_turn + [inner_left_turn[0]]
