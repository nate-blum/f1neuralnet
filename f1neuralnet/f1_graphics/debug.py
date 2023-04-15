import pygame
from f1neuralnet.constant import RED, WINDOW_HEIGHT, WINDOW_WIDTH
from f1neuralnet.models import Car, Timer, lap_time_format
from f1neuralnet.tracks import OvalTrack

def draw_debug_graphics(screen):
    pygame.draw.line(screen, RED, (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT))
    pygame.draw.line(screen, RED, (0, WINDOW_HEIGHT / 2), (WINDOW_WIDTH, WINDOW_HEIGHT / 2))

def draw_stats_debug(screen: pygame.Surface, did_start_lap: list[bool], distances: list[float]):
    font = pygame.font.Font(None, 24)
    if len(did_start_lap) == 0 or len(distances) == 0:
        return
    
    started_percent = sum(did_start_lap[-20:] if len(did_start_lap) > 20 else did_start_lap) / (20 if len(did_start_lap) > 20 else len(did_start_lap))
    distance_average = sum(distances[-20:] if len(distances) > 20 else distances) / (20 if len(distances) > 20 else len(distances))
    laps_started = font.render(
        f'lap_started_%: {"{:.3f}".format(started_percent)}, avg_distance: {"{:.3f}".format(distance_average)}', True, "black")
    screen.blit(laps_started, (600, 500))

def draw_debug_info(screen: pygame.Surface, player: Car, track: OvalTrack, timer: Timer, generation: float, state):
    font = pygame.font.Font(None, 24)
    pos = font.render(f'position: {str(player.position)}', True, "black")
    screen.blit(pos, (300, 200))
    vel = font.render(f'velocity: {player.velocity}', True, "black")
    screen.blit(vel, (300, 230))
    direction = font.render(f'direction: {player.direction}', True, "black")
    screen.blit(direction, (300, 260))
    time = font.render(f'time: {lap_time_format(timer.current_lap)}', True, "black")
    screen.blit(time, (300, 320))
    lower_bound = len(timer.laps) - 5
    laps = [
        font.render(f'lap {i + 1}: {"DNF" if timer.laps[i] == -1 else lap_time_format(timer.laps[i])}', True, "black")
        for i in range(lower_bound if lower_bound >= 0 else 0, len(timer.laps))
    ]
    for i in range(0, len(laps)):
        screen.blit(laps[i], (300, 350 + (30 * i)))
    gen = font.render(f'generation: {generation}', True, "black")
    screen.blit(gen, (600, 350))
    fly_lap = font.render(f'flying_lap: {state.flying_lap}', True, "black")
    screen.blit(fly_lap, (600, 380))
    dist_to_turn = font.render(f'distance_to_turn: {track.distance_to_next_turn(player)}', True, "black")
    screen.blit(dist_to_turn, (600, 410))
    radius = font.render(f'radius_of_curr_turn: {track.current_turn_radius(player)}', True, "black")
    screen.blit(radius, (600, 440))
    distances = font.render(
        f'distances: [{", ".join(map(lambda f: "{:.2f}".format(f), player.get_distances_to_track_limits(track)))}]',
        True, "black")
    screen.blit(distances, (600, 470))


def draw_actions_debug(screen, actions):
    if len(actions) == 0:
        return
    
    font = pygame.font.Font(None, 24)
    
    turn = font.render(f'turn: ', True, "black")
    screen.blit(turn, (300, 290))
    pygame.draw.rect(screen, pygame.Color(100, 0, 0), pygame.Rect(340, 290, 100, 25))
    left = 390 - (abs(actions[0]) * 50) if actions[0] < 0 else 390
    pygame.draw.rect(screen, pygame.Color(255, 0, 0), pygame.Rect(left, 290, abs(actions[0]) * 50, 25))

    throttle = font.render(f'acc: ', True, "black")
    screen.blit(throttle, (450, 290))
    pygame.draw.rect(screen, pygame.Color(0, 100, 0), pygame.Rect(490, 290, 100, 25))
    pygame.draw.rect(screen, pygame.Color(0, 255, 0), pygame.Rect(490, 290, actions[1] * 100, 25))

    brake = font.render(f'stop: ', True, "black")
    screen.blit(brake, (600, 290))
    pygame.draw.rect(screen, pygame.Color(0, 0, 100), pygame.Rect(640, 290, 100, 25))
    pygame.draw.rect(screen, pygame.Color(0, 0, 255), pygame.Rect(640, 290, actions[2] * 100, 25))
