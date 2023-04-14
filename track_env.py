from math import inf
from gym import Env, spaces
import pygame
from constant import *
from graphics.renderer import render
from models.car import Car
from models.timer import Timer
from tracks.oval_track import OvalTrack
from numpy import array


class TrackEnv(Env):
    """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self):
    super(TrackEnv, self).__init__()
    
    self.action_space = spaces.MultiDiscrete([3, 2, 2]) #steering input (0, 1, 2) = (left, straight, right), throttle on/off, brakes on/off
    self.observation_space = spaces.Dict({
        'position': spaces.Box(low=array([0,0]), high=array([1280,720])),
        'velocity': spaces.Box(low=0,high=inf),
        'direction': spaces.Box(low=0, high=360),
        'distance_to_turn': spaces.Box(low=0, high=inf),
        'radius_of_current_turn': spaces.Box(low=-inf, high=inf),
        'distances': spaces.Box(low=array([0, 0, 0, 0, 0]),high=array([inf, inf, inf, inf, inf]))
    })

    pygame.init()
    
    self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    self.clock = pygame.time.Clock()
    self.running = True

    self.track = OvalTrack(TRACK_PADDING[0], TRACK_PADDING[1], WINDOW_WIDTH - (2 * TRACK_PADDING[0]), WINDOW_HEIGHT - (2 * TRACK_PADDING[1]))
    self.player = Car((self.track.grid_slots_pos[0] + GRID_SLOT_PADDING + 8 + (CAR_HEIGHT / 2), self.track.grid_slots_pos[1] + GRID_SLOT_PADDING + (GRID_SLOT_SIZE / 2)), 180, 0)
    self.flying_lap = False
    self.timer = Timer()

    self.touching_start_finish = False
    self.lap_length = 0

#   def step(self, action):
    # if not touching_start_finish and track.are_car_front_wheels_touching_start_finish(player):
    #     touching_start_finish = True
    #     if flying_lap:
    #         player.reset()
    #         lap_length = 0
    #     flying_lap = not flying_lap
    # elif touching_start_finish and not track.are_car_front_wheels_touching_start_finish(player):
    #     touching_start_finish = False

    # if track.is_car_within_track_limits(player):
    #     player.handle_actions(dt)
    # else:
    #     player.reset()
    #     timer.dnf()
    #     flying_lap = False
    #     lap_length = 0

    # dt = clock.tick(60) / 1000 # limits FPS to 60
    # if flying_lap:
    #     timer.tick(dt)
    #     lap_length += player.velocity * dt

  def reset(self):
    self.player.reset()
    if 0.8 * OVAL_TRACK_LENGTH <= self.lap_length and self.lap_length <= 1.2 * OVAL_TRACK_LENGTH:
        self.timer.complete()
    else:
        self.timer.dnf()
    self.flying_lap = False
    self.lap_length = 0

    # return self._next_observation()

    # def

  def render(self, mode='human', close=False):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            self.running = False

    render(self.screen, self.player, self.track, self.timer)
    pygame.display.flip()
