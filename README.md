# Asteroid Slingshot

Asteroid Slingshot is a simple simulation game built with Pygame. The game allows players to simulate the gravitational effects on asteroids as they are slung around a planet. Utilizing real-world physics constants, the game attempts to provide an educational yet entertaining experience on gravitational forces and celestial object interactions.

## Features

- Simulate asteroid trajectories influenced by a planet's gravity.
- Different types of asteroids with varying densities and sizes.
- Realistic gravitational physics calculations.
- Visual representation of collisions and asteroid trajectories.
- Customizable constants for more varied simulations.

## Installation

To run Asteroid Slingshot, you'll need Python and Pygame installed on your system.

1. Install Python from [python.org](https://www.python.org/downloads/).
2. Install Pygame using pip:

   ```sh
   pip install pygame
   ```

3. Clone or download this repository to your local machine.

4. Navigate to the project directory and run the script:

   ```sh
   python main.py
   ```

## How to Play

- Click and hold the mouse to create an asteroid at the desired location.
- Drag the mouse to aim and adjust the velocity of the asteroid.
- Release the mouse to launch the asteroid.
- Watch as the asteroid's path is altered by the planet's gravity.
- Try to create interesting orbits or direct hits on the planet.

## Customization

You can customize various constants within the game to experiment with different scenarios:

- `G`: Gravitational constant.
- `PLANET_MASS`: Mass of the planet.
- `MAXIMUM_ASTEROID_SIZE`: Maximum size of the asteroids.
- Display settings like window size and scales for distance and velocity.

## Dependencies

- Python 3.x
- Pygame
