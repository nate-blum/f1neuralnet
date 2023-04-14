import math
import pygame
from constant import CAR_HEIGHT, CAR_WIDTH, RED, TRANSPARENT

# https://asawicki.info/Mirror/Car%20Physics%20for%20Games/Car%20Physics%20for%20Games.html
class Car:
    def __init__(self, position, direction, velocity):
        self.position = position
        self.initial_position = position
        self.direction = direction
        self.initial_direction = direction
        self.velocity = velocity
        self.initial_velocity = velocity
        self.surface = pygame.Surface((CAR_WIDTH, CAR_HEIGHT))
        self.surface.set_colorkey(TRANSPARENT)

    def get_rect_coords(self):
        coords = []
        r = math.sqrt(725)
        theta = 21.801
        for i in range(0, 2):
            for j in range(0, 2):
                coords.append((
                    self.rect.centerx + 
                        self.negate(r * math.cos(math.radians(self.direction + self.negate(theta, j))), i),
                    self.rect.centery + 
                        self.negate(r * math.sin(math.radians(self.direction + self.negate(theta, j))), i + 1)
                ))
        return coords
    
    def get_front_wheels(self):
        return self.get_rect_coords()[:2]

    def negate(self, value: int, exp: int):
        return value * ((-1) ** exp)
    
    def reset(self):
        self.position = self.initial_position
        self.direction = self.initial_direction
        self.velocity = self.initial_velocity

    def draw(self, screen):
        image = pygame.transform.rotate(self.surface, self.direction + 90)
        rect = image.get_rect()
        rect.center = self.position
        self.rect = rect
        self.surface.fill(RED)
        screen.blit(image, rect)
        pygame.draw.line(screen, "green", self.position, (self.position[0] + (50 * math.cos(math.radians(self.direction))), self.position[1] - (50 * math.sin(math.radians(self.direction)))))

    def handle_actions(self, dt):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.accelerate(dt)
        if key[pygame.K_s]:
            self.accelerate(dt, True)
        if key[pygame.K_a]:
            self.turn(dt)
        if key[pygame.K_d]:
            self.turn(dt, True)

        self.move(dt)

    # simple simulation:
    def accelerate(self, dt, neg=False): 
        coeff = 30
        accel = (((-1) ** int(neg)) * coeff) * dt
        
        if self.velocity + accel < 0:
            self.velocity = 0
        else:
            self.velocity += accel

    def move(self, dt):
        new_x = self.position[0] + ((self.velocity * math.cos(math.radians(self.direction))) * dt)
        new_y = self.position[1] - ((self.velocity * math.sin(math.radians(self.direction))) * dt)
        self.position = (new_x, new_y)

    def turn(self, dt, right=False):
        ang_vel = 50
        self.direction += (((-1) ** int(right)) * ang_vel) * dt
        self.direction %= 360

    # def top_left_corner(self):
    #     return (self.position[0] - (self.width / 2), self.position[1] - (self.height / 2))



    #     self.mass = 752 # listed mass of Mercedes W12
    #     self.mu_fric = 1.7 # coefficient of friction for f1 cars is roughly 1.7
    #     self.c_

    # '''
    # follows sigmoid function 1 / 1+e^-(5x/3 - 4)
    # derivative (5e^((-5x+12) / 3) / 3(1 + e^((-5x+12) / 3))^2)

    # assume 1:1 pixel to meter so maximum velocity of 93.47 m/s
    # '''
    # def accelerate(self, neg=False): 
    #     exp = ((-5 * self.velocity) + 12) / 3
    #     accel = (5 * (math.e ** exp)) / (3 * ((1 + (math.e ** exp) ** 2)))
    #     v_coefficient = 93.47
    #     self.velocity += (-1 ** int(neg)) * accel * v_coefficient

    # '''
    # assume perfectly balanced front/rear downforce car
    # perfect slide when grip threshold is passed

    # assume downforce properties of Mercedes W12 F1 car
    # following paper gives rough estimates of downforce produced at high-, mid-, and low-speeds
    # 93.47 m/s (336 km/h) equivalent to 93.47 pixels/second

    # https://commons.erau.edu/cgi/viewcontent.cgi?article=1003&context=aiaar2sc
    # '''
    # def rotate(self, right=False):


    # # bounding box - track limits
    # # think about implementing oversteer curve
    # # starting grid box - tire warmup lap ?
    # # tire friction coefficient
    # # reward - timed lap
    
    # # vertical load = downforce + force of gravity
    # # downforce follows roughly quadratic relationship with velocity (df ~= v^2 / 7.5)
    # def vertical_load(self):
    #     downforce = (self.velocity ** 2) / 7.5
    #     return downforce + (self.mass * 9.81)
    
    # # drag also follows roughly quadratic relationship with velocity (df ~= v^2 / 8.5)
    # def drag(self):
    #     return (self.velocity ** 2) / 8.5
    

    
    # def isAdhering(self, angular_v, radius):
    #     centripetal = self.mu_fric * self.vertical_load()
    #     centrifugal = self.mass * (angular_v ** 2) * radius
    #     return centripetal >= centrifugal
    
    # tractive force - force delivered by engine to rear wheels
    # drag
    # force of rolling resistance
    # longitudinal force (parallel to motion) = traction - (drag + rr)


