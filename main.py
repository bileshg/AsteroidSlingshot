from enum import Enum

import pygame
import math
import random

# Constants for calculations
G = 6.67428e-11  # Gravitational constant

PLANET_MASS = 6 * 10 ** 24  # kg
MAXIMUM_ASTEROID_SIZE = 10  # km

# Constants for display
WIDTH, HEIGHT = 800, 800

DISTANCE_SCALE = 100_000
TIME_STEP = 60 * 30  # 30 minutes
VELOCITY_SCALE = TIME_STEP / DISTANCE_SCALE

MIN_ASTEROID_RADIUS = 3  # pixels
MAX_ASTEROID_RADIUS = 5  # pixels
PLANET_RADIUS = 50  # pixels

CLOCK_TICK = 60
COLLISION_COOLDOWN = 3000

COLLISION_SIZE = 3  # pixels


class Color(Enum):
    WHITE = (255, 255, 255)
    SILVER = (192, 192, 192)
    GRAY = (128, 128, 128)
    SANDY_BROWN = (244, 164, 96)
    RED = (255, 0, 0)


# Constants for the asteroid
ASTEROID_TYPES = [
    ("C-Type", 1.38 * 10 ** 12, Color.GRAY),  # Density in kg/km^3
    ("S-Type", 2.70 * 10 ** 12, Color.SANDY_BROWN),
    ("M-Type", 5.32 * 10 ** 12, Color.SILVER)
]


class CelestialObject:
    def __init__(self, x, y, radius, actual_mass):
        # Position of the object in the window
        self.x = x
        self.y = y

        # Radius of the object in pixels
        self.radius = radius

        # Mass of the object in kg
        self.actual_mass = actual_mass

    def set_position(self, x, y):
        self.x = x
        self.y = y

    def get_position(self):
        return self.x, self.y


class Planet(CelestialObject):
    def __init__(self, x, y, radius, actual_mass, image_path):
        super().__init__(x, y, radius, actual_mass)

        self.appearance = pygame.transform.scale(
            pygame.image.load(image_path),
            (radius * 2, radius * 2)
        )

    def draw(self, win, font):
        # Position of the planet's top-left corner
        pos = (self.x - self.radius, self.y - self.radius)
        win.blit(self.appearance, pos)


class Asteroid(CelestialObject):
    def __init__(self, x, y, radius, actual_mass, asteroid_type, actual_size, color, vel_x, vel_y):
        super().__init__(x, y, radius, actual_mass)

        self.asteroid_type = asteroid_type
        self.actual_size = actual_size
        self.color = color

        self.vel_x = vel_x
        self.vel_y = vel_y

    def move(self, planet=None):
        if planet is not None:
            x, y = self.get_position()
            x, y = x * DISTANCE_SCALE, y * DISTANCE_SCALE
            m = self.actual_mass

            px, py = planet.get_position()
            px, py = px * DISTANCE_SCALE, py * DISTANCE_SCALE
            pm = planet.actual_mass

            distance = math.sqrt((x - px) ** 2 + (y - py) ** 2)
            force = (G * m * pm) / distance ** 2

            acceleration = force / m
            angle = math.atan2(py - y, px - x)

            acceleration_x = acceleration * math.cos(angle)
            acceleration_y = acceleration * math.sin(angle)

            self.vel_x += acceleration_x * VELOCITY_SCALE
            self.vel_y += acceleration_y * VELOCITY_SCALE

        self.x += self.vel_x
        self.y += self.vel_y

    def draw(self, win, font):
        x, y = int(self.x), int(self.y)
        pygame.draw.circle(win, self.color.value, (x, y), self.radius)

        # Display Type & Size
        txt_asteroid_type = font.render(
            f"{self.asteroid_type}({round(self.actual_size)} km)",
            True,
            Color.WHITE.value
        )
        win.blit(txt_asteroid_type, (x, y + self.radius))


def create_asteroid():
    type_probability = random.randint(0, 100)

    if type_probability < 75:
        asteroid_type, density, color = ASTEROID_TYPES[0]
    elif type_probability < 92:
        asteroid_type, density, color = ASTEROID_TYPES[1]
    else:
        asteroid_type, density, color = ASTEROID_TYPES[2]

    radius = random.randint(0, MAXIMUM_ASTEROID_SIZE) + 1
    volume = (4 / 3) * math.pi * radius ** 3
    mass = density * volume

    return asteroid_type, radius, mass, color


def throw_asteroid(location, mouse):
    asteroid_type, radius, mass, color = create_asteroid()

    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) * VELOCITY_SCALE
    vel_y = (m_y - t_y) * VELOCITY_SCALE

    asteroid_size = MIN_ASTEROID_RADIUS + (radius / MAXIMUM_ASTEROID_SIZE) * (MAX_ASTEROID_RADIUS - MIN_ASTEROID_RADIUS)

    return Asteroid(t_x, t_y, asteroid_size, mass, asteroid_type, radius, color, vel_x, vel_y)


def _process_collisions(win, collisions):
    for collision in collisions:
        ast, time = collision
        if time + COLLISION_COOLDOWN >= pygame.time.get_ticks():
            pygame.draw.circle(win, Color.RED.value, ast.get_position(), COLLISION_SIZE)
        else:
            collisions.remove(collision)


def _process_asteroids(win, font, planet, asteroids):
    new_collisions = []
    for ast in asteroids[:]:
        ast.draw(win, font)
        ast.move(planet)

        off_screen = ast.x < 0 or ast.x > WIDTH or ast.y < 0 or ast.y > HEIGHT
        if off_screen:
            asteroids.remove(ast)

        collided = math.sqrt((ast.x - planet.x) ** 2 + (ast.y - planet.y) ** 2) <= PLANET_RADIUS
        if collided:
            now = pygame.time.get_ticks()
            new_collisions.append((ast, now))
            asteroids.remove(ast)

    return new_collisions


def run_simulation(win, clock, font):
    bg = pygame.transform.scale(pygame.image.load("stars.jpg"), (WIDTH, HEIGHT))

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_RADIUS, PLANET_MASS, "earth.png")
    asteroids = []
    collisions = []
    new_asteroid_position = None

    run = True
    while run:
        clock.tick(CLOCK_TICK)

        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if new_asteroid_position:
                    asteroid = throw_asteroid(new_asteroid_position, mouse_pos)
                    asteroids.append(asteroid)
                    new_asteroid_position = None
                else:
                    new_asteroid_position = mouse_pos

        win.blit(bg, (0, 0))

        if new_asteroid_position:
            pygame.draw.line(win, Color.WHITE.value, new_asteroid_position, mouse_pos, 2)
            pygame.draw.circle(win, Color.RED.value, new_asteroid_position, MAX_ASTEROID_RADIUS)

        new_collisions = _process_asteroids(win, font, planet, asteroids)
        collisions.extend(new_collisions)

        planet.draw(win, font)

        _process_collisions(win, collisions)

        pygame.display.update()

    pygame.quit()


def main():
    pygame.init()

    win = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(pygame.font.get_fonts()[0], 14)

    pygame.display.set_caption("Asteroid Slingshot")

    run_simulation(win, clock, font)


if __name__ == "__main__":
    main()
