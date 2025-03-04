import pygame
import time
from OpenGL.GL import *
from OpenGL.GLU import gluPerspective
import numpy as np

# Initialize pygame
pygame.init()

# Set up display
display = (800, 600)
pygame.display.set_mode(display, pygame.DOUBLEBUF | pygame.OPENGL)
gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

# Cube vertices
vertices = np.array([
    [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
    [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
], dtype=float)

# Cube edges
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# PID Controller Class
class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = np.array([0.0, 0.0, 0.0])
        self.integral = np.array([0.0, 0.0, 0.0])

    def compute(self, target, current, dt):
        error = target - current
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        self.prev_error = error
        return self.kp * error + self.ki * self.integral + self.kd * derivative

# Initialize PID controller for movement control
pid = PIDController(kp=0.1, ki=0.01, kd=0.05)

# Target position for the cube
target_position = np.array([0.0, 0.0, 0.0])
cube_position = np.array([0.0, 0.0, -5.0])

# Function to draw cube
def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex] + cube_position)
    glEnd()

# Game loop
clock = pygame.time.Clock()
running = True
last_time = time.time()

while running:
    dt = time.time() - last_time
    last_time = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Control cube with PID towards target position
    movement = pid.compute(target_position, cube_position, dt)
    cube_position += movement * dt

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    draw_cube()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
