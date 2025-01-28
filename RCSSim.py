import pygame
import sys
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

# Define vertices and edges of the cube
vertices = [
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, 1],
    [1, -1, 1],
    [-1, -1, 1],
    [-1, 1, 1]
]

edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7)
]

# Function to draw the cube
def draw_cube():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Main function
def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
    glTranslatef(0.0, 0.0, -5)

    x_move, y_move, z_move = 0, 0, 0

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_move = -0.1
                if event.key == pygame.K_RIGHT:
                    x_move = 0.1
                if event.key == pygame.K_UP:
                    y_move = 0.1
                if event.key == pygame.K_DOWN:
                    y_move = -0.1
                if event.key == pygame.K_w:
                    z_move = 0.1
                if event.key == pygame.K_s:
                    z_move = -0.1

            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    x_move = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    y_move = 0
                if event.key in [pygame.K_w, pygame.K_s]:
                    z_move = 0

        glTranslatef(x_move, y_move, z_move)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        draw_cube()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
