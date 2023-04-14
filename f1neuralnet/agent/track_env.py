from math import inf
import gym
from gym import spaces
import pygame
from constant import *
from graphics.renderer import render
from models.car import Car
from models.timer import Timer
from tracks.oval_track import OvalTrack
import numpy as np
from collections import OrderedDict


class State:
    def __init__(self, flying_lap: bool, touching_start_finish: bool, dnf: bool, lap_length: float, dt: float):
        self.flying_lap, self.touching_start_finish, self.dnf, self.lap_length, self.dt = flying_lap, touching_start_finish, dnf, lap_length, dt


class TrackEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render_modes': ['human'], 'render_fps': 60}

    def __init__(self, render_mode="human"):
        super(TrackEnv, self).__init__()

        self.action_space = spaces.MultiDiscrete([3, 2, 2])  # steering input (0, 1, 2) = (left, straight, right), throttle on/off, brakes on/off
        self.observation_space = spaces.Box(
            # x, y, v, d, dist_to_turn, radius, distances 1-5
            low=np.array([0, 0, 0, 0, 0, -1280, 0, 0, 0, 0, 0]),
            high=np.array([1280, 720, 1000, 360, 1280, 1280, 1280, 1280, 1280, 1280, 1280])
        )
        self.reward_range = (-100, 100)
        self.render_mode = render_mode

        self.track = OvalTrack(TRACK_PADDING[0], TRACK_PADDING[1], WINDOW_WIDTH - (2 * TRACK_PADDING[0]), WINDOW_HEIGHT - (2 * TRACK_PADDING[1]))
        self.player = Car((self.track.grid_slots_pos[0] + GRID_SLOT_PADDING + 8 + (CAR_HEIGHT / 2),
                           self.track.grid_slots_pos[1] + GRID_SLOT_PADDING + (GRID_SLOT_SIZE / 2)), 180, 0)
        self.state = State(False, False, False, 0, 0)
        self.timer = Timer()

        self.window = None
        self.clock = None

    def lap_time_reward(self):
        x = self.timer.current_lap - IDEAL_LAP_TIME
        return -(10 / 3) * (np.sqrt(-(x ** 2) + (60 * x)) - 30)

    def distance_reward(self):
        c = 2710 / 12
        ideal_distance = c * self.timer.current_lap
        return (20 / c) * (self.state.lap_length - ideal_distance)

    def step(self, action):
        if not self.track.is_car_within_track_limits(self.player):
            self.state.dnf = True
            return {}, -100, False, True, {}
        elif self.timer.current_lap > 30:
            return {}, -50, False, True, {}

        if not self.state.touching_start_finish and self.track.are_car_front_wheels_touching_start_finish(self.player):
            self.state.touching_start_finish = True
            if self.state.flying_lap:
                return {}, self.lap_time_reward(), True
            self.state.flying_lap = not self.state.flying_lap
        elif self.state.touching_start_finish and not self.track.are_car_front_wheels_touching_start_finish(self.player):
            self.state.touching_start_finish = False

        self.player.handle_actions(action, self.state.dt)

        self._render_frame()
        return self.next_observation(), self.distance_reward(), False, False, {}

    def reset(self):
        super().reset()
        self.player.reset()

        if 0.8 * OVAL_TRACK_LENGTH <= self.state.lap_length and self.state.lap_length <= 1.2 * OVAL_TRACK_LENGTH and not self.state.dnf:
            self.timer.complete()
        elif self.state.dnf:
            self.timer.dnf()

        self.state = State(False, False, False, 0, 0)

        # return np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float32), {}
        self._render_frame()
        return self.next_observation(), {}

    def next_observation(self):
        # x, y, v, d, dist_to_turn, radius, distances 1-5
        return np.array([
            self.player.position[0],
            self.player.position[1],
            self.player.velocity,
            self.player.direction,
            0, 0,
            0, 0, 0, 0, 0
        ], dtype=np.float32)

    # {
    #         'position': spaces.Box(low=np.array([0, 0]), high=np.array([1280, 720])),
    #         'velocity': spaces.Box(low=0, high=inf),
    #         'direction': spaces.Box(low=0, high=360),
    #         'distance_to_turn': spaces.Box(low=0, high=inf),
    #         'radius_of_current_turn': spaces.Box(low=-inf, high=inf),
    #         'distances': spaces.Box(low=np.array([0, 0, 0, 0, 0]), high=np.array([inf, inf, inf, inf, inf]))
    #     }

    # def

    def render(self):
        pass

    def _render_frame(self):
        if self.window is None:
            pygame.init()
            pygame.display.init()
            self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        if self.clock is None:
            self.clock = pygame.time.Clock()

        canvas = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))

        render(canvas, self.player, self.track, self.timer)
        self.window.blit(canvas, canvas.get_rect())
        pygame.event.pump()
        pygame.display.update()

        self.state.dt = self.clock.tick(self.metadata["render_fps"]) / 1000  # limits FPS to 60
        if self.state.flying_lap:
            self.timer.tick(self.state.dt)
            self.state.lap_length += self.player.velocity * self.state.dt

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
