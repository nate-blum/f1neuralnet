from math import inf
import gym
from gym import spaces
import pygame
from f1neuralnet.constant import *
from f1neuralnet.f1_graphics import render, draw_actions_debug, draw_stats_debug
from f1neuralnet.models import Car, Timer
from f1neuralnet.tracks import OvalTrack
import numpy as np


class State:
    def __init__(self, flying_lap: bool, touching_start_finish: bool, dnf: bool, lap_length: float, total_length: float, dt: float):
        self.flying_lap, self.touching_start_finish,\
        self.lap_length, self.dnf, self.total_length, self.dt = flying_lap, touching_start_finish,\
        lap_length, dnf, total_length, dt
        self.actions = []


class TrackEnv(gym.Env):
    """Custom Environment that follows gym interface"""
    metadata = {'render_modes': ['human']}

    def __init__(self, render_mode="human"):
        super(TrackEnv, self).__init__()

        self.action_space = spaces.Box(
            low=np.array([
                -1, 0, 0
            ]), #type: ignore
            high=np.array([
                1, 1, 1
            ]), #type: ignore
            dtype=np.float32
        )  # steering input (-1 - 0 - 1) = (left, straight, right), throttle 0 - 1, brakes 0 - 1
        self.observation_space = spaces.Box(
            # x, y, v, d, dist_to_turn, radius, distances 1-5
            low=np.array(
                [0, 0, 0, 0, 
                0, -1280, 
                0, 0, 0, 0, 0],
                ), # type: ignore
            high=np.array(
                [1280, 720, 1000, 360, 
                1280, 1280, 
                1280, 1280, 1280, 1280, 1280]), # type: ignore
            dtype=np.float32
        )
        self.reward_range = (-100, 100)
        self.render_mode = render_mode

        self.track = OvalTrack(TRACK_PADDING[0], TRACK_PADDING[1], WINDOW_WIDTH - (2 * TRACK_PADDING[0]), WINDOW_HEIGHT - (2 * TRACK_PADDING[1]))
        self.player = Car((self.track.grid_slots_pos[0] + GRID_SLOT_PADDING + 8 + (CAR_HEIGHT / 2),
                           self.track.grid_slots_pos[1] + GRID_SLOT_PADDING + (GRID_SLOT_SIZE / 2)), 180, 0)
        self.state = State(False, False, False, 0, 0, 0)
        self.lap_timer = Timer()
        self.episode_timer = Timer()

        self.generation = 1

        self.window = None
        self.clock = None

        self.did_start_lap = []
        self.distances = []

    def lap_time_reward(self):
        x = self.lap_timer.current_lap - IDEAL_LAP_TIME
        square = -(x ** 2) + (60 * x)
        return -(10 / 3) * (np.sqrt(-(x ** 2) + (60 * x)) - 30) if square >= 0 else 0
    
    def delta_to_ideal(self):
        c = OVAL_TRACK_LENGTH / 12
        ideal_distance = c * self.lap_timer.current_lap
        return (self.state.lap_length - ideal_distance) / c
    
    def compute_reward(self, did_start_lap: bool, did_finish_lap: bool, dnf: bool, timed_out: bool):
        reward = 0
        dnf_penalty = 25
        timeout_penalty = 50
        fail_to_start_penalty = 50
        distance_reward_coeff = 2 if did_start_lap else 1
        wrong_direction_penalty = 50

        if did_finish_lap:
            return self.lap_time_reward()
        
        reward -= dnf_penalty * dnf
        reward -= timeout_penalty * timed_out
        reward -= fail_to_start_penalty * (timed_out and not did_start_lap)
        reward -= wrong_direction_penalty * (not did_start_lap and self.player.position[0] > self.player.initial_position[0])
        reward += ((self.state.total_length / OVAL_TRACK_LENGTH) * 50) * distance_reward_coeff

        if reward > 100:
            return 100
        elif reward < -100:
            return -100
        else:
            return reward
        
    def append_stats(self):
        self.did_start_lap.append(self.state.flying_lap)
        self.distances.append(self.state.total_length)

    def step(self, action):
        if not self.track.is_car_within_track_limits(self.player):
            print("dnf")
            self.state.dnf = True
            self.append_stats()
            return self.next_observation(), self.compute_reward(self.state.flying_lap, False, True, False), True, {}
        elif self.episode_timer.current_lap > 5000 and not self.state.flying_lap:
            print("took too long to start a lap", self.state.total_length)
            self.append_stats()
            return self.next_observation(), self.compute_reward(False, False, False, True), True, {}
        elif self.delta_to_ideal() < -6 and self.lap_timer.current_lap > 6000 and self.state.flying_lap:
            print("current lap is soo slow")
            self.append_stats()
            return self.next_observation(), self.compute_reward(True, False, False, True), True, {}

        if not self.state.touching_start_finish and self.track.are_car_front_wheels_touching_start_finish(self.player):
            self.state.touching_start_finish = True
            if self.state.flying_lap and 0.8 * OVAL_TRACK_LENGTH <= self.state.lap_length and self.state.lap_length <= 1.2 * OVAL_TRACK_LENGTH:
                print("finished our flying lap")
                self.append_stats()
                return self.next_observation(), self.compute_reward(True, True, False, False), True, {}
            self.state.flying_lap = not self.state.flying_lap
        elif self.state.touching_start_finish and not self.track.are_car_front_wheels_touching_start_finish(self.player):
            self.state.touching_start_finish = False

        self.state.actions = action
        self.player.handle_actions(action, self.state.dt)

        self._render_frame()
        # return self.next_observation(), self.distance_reward(), True, False, {}
        # print(self.next_observation())
        return self.next_observation(), 20 * self.delta_to_ideal(), False, {}

    def reset(self):
        super().reset()
        self.generation += 1
        self.player.reset()

        if not self.state.flying_lap:
            self.lap_timer.reset()
        elif 0.8 * OVAL_TRACK_LENGTH <= self.state.lap_length and self.state.lap_length <= 1.2 * OVAL_TRACK_LENGTH and not self.state.dnf:
            self.lap_timer.complete()
        else:
            self.lap_timer.dnf()
        self.episode_timer.reset()

        self.state = State(False, False, False, 0, 0, 0)

        # return np.array([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], dtype=np.float32), {}
        self._render_frame()
        # print(self.next_observation())
        return self.next_observation()

    def next_observation(self):
        # x, y, v, d, dist_to_turn, radius, distances 1-5
        return np.array(
            [
                self.player.position[0],
                self.player.position[1],
                self.player.velocity,
                self.player.direction,
                self.track.distance_to_next_turn(self.player), 
                self.track.current_turn_radius(self.player),
                *self.player.get_distances_to_track_limits(self.track)
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

        render(canvas, self.player, self.track, self.lap_timer, self.generation, self.state)
        draw_actions_debug(canvas, self.state.actions)
        draw_stats_debug(canvas, self.did_start_lap, self.distances)
        self.window.blit(canvas, canvas.get_rect())
        pygame.event.pump()
        pygame.display.update()

        self.state.dt = self.clock.tick(60) / 1000  # limits FPS to 60
        self.episode_timer.tick(self.state.dt)
        self.state.total_length += self.player.velocity * self.state.dt

        if self.state.flying_lap:
            self.lap_timer.tick(self.state.dt)
            self.state.lap_length += self.player.velocity * self.state.dt

    def close(self):
        if self.window is not None:
            pygame.display.quit()
            pygame.quit()
