import pygame
from constant import RED, WINDOW_HEIGHT, WINDOW_WIDTH
from models.car import Car
from models.timer import Timer
from tracks.track import Track


def draw_debug_graphics(screen):
    pygame.draw.line(screen, RED, (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT))
    pygame.draw.line(screen, RED, (0, WINDOW_HEIGHT / 2), (WINDOW_WIDTH, WINDOW_HEIGHT / 2))


def draw_debug_info(screen: pygame.Surface, player: Car, track: Track, timer: Timer):
    font = pygame.font.Font('freesansbold.ttf', 24)
    pos = font.render(f'position: {str(player.position)}', True, "black")
    screen.blit(pos, (300, 200))
    vel = font.render(f'velocity: {player.velocity}', True, "black")
    screen.blit(vel, (300, 230))
    dir = font.render(f'direction: {player.direction}', True, "black")
    screen.blit(dir, (300, 260))
    in_bounds = font.render(f'is on track: {track.is_car_within_track_limits(player)}', True, "black")
    screen.blit(in_bounds, (300, 290))
    in_bounds = font.render(f'front wheels touching start finish: {track.are_car_front_wheels_touching_start_finish(player)}', True, "black")
    screen.blit(in_bounds, (300, 320))
    time = font.render(f'time: {timer.format(timer.current_lap)}', True, "black")
    screen.blit(time, (300, 350))
    laps = [
        font.render(f'lap {i + 1}: {"DNF" if lap == -1 else timer.format(lap)}', True, "black")
        for i, lap in enumerate(timer.laps[-5:])
    ]
    for i in range(0, len(laps)):
        screen.blit(laps[i], (300, 380 + (30 * i)))


def draw_car_debug(car):
    pass
