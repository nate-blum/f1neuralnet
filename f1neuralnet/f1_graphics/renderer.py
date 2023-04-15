import pygame
from f1neuralnet.constant import WHITE
from f1neuralnet.f1_graphics import draw_debug_info
from f1neuralnet.models import Car, Timer
from f1neuralnet.tracks import OvalTrack


def render(screen: pygame.Surface, player: Car, track: OvalTrack, timer: Timer, generation: float, state):
    screen.fill(WHITE)

    track.draw(screen)
    player.draw(screen)
    
    draw_debug_info(screen, player, track, timer, generation, state)
    # draw_debug_graphics(screen)
    # vec_coords = (math.cos(math.radians(player_car.direction)) * player_car.velocity, math.sin(math.radians(player_car.direction)) * player_car.velocity)
    # pygame.draw.line(screen, "green", player_car.position, (player_car.position[0] + vec_coords[0], player_car.position[1] - vec_coords[1]))

    # pygame.draw.polygon(screen, "red", car_points(*player_car.position, player_car.width, player_car.height, player_car.direction))
    # for p in points:
    #     gfxdraw.pixel(screen, int(p[0]), int(p[1]), pygame.Color(255, 255, 255))
