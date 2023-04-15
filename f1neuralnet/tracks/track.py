import abc
from pygame import Surface

class Track(abc.ABC):
    @abc.abstractmethod
    def __init__(self, x: int, y: int, width: int, height: int):
        pass

    @abc.abstractmethod
    def draw(self, screen: Surface):
        pass

    @abc.abstractmethod
    def is_car_within_track_limits(self, car) -> bool:
        pass

    @abc.abstractmethod
    def are_car_front_wheels_touching_start_finish(self, car) -> bool:
        pass

    @abc.abstractmethod
    def compute_points(self) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        pass
