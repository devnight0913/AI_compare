import pygame
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
BALL_RADIUS = 10
GRAVITY = 0.2
FRICTION = 0.99
HEXAGON_RADIUS = 200
ROTATION_SPEED = 1  # Degrees per frame

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Ball properties
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_vx, ball_vy = 2, -5

# Hexagon rotation angle
angle = 0

# Function to get hexagon vertices
def get_hexagon_vertices(cx, cy, radius, angle):
    vertices = []
    for i in range(6):
        theta = math.radians(i * 60 + angle)
        x = cx + radius * math.cos(theta)
        y = cy + radius * math.sin(theta)
        vertices.append((x, y))
    return vertices

# Function to reflect velocity off a wall
def reflect(velocity, normal):
    dot_product = velocity[0] * normal[0] + velocity[1] * normal[1]
    reflection = (velocity[0] - 2 * dot_product * normal[0],
                  velocity[1] - 2 * dot_product * normal[1])
    return reflection

# Game loop
running = True
while running:
    screen.fill(BLACK)
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    angle += ROTATION_SPEED
    hexagon = get_hexagon_vertices(WIDTH // 2, HEIGHT // 2, HEXAGON_RADIUS, angle)
    
    # Update ball physics
    ball_vy += GRAVITY  # Apply gravity
    ball_vx *= FRICTION  # Apply friction
    ball_vy *= FRICTION
    ball_x += ball_vx
    ball_y += ball_vy
    
    # Check for collisions with hexagon walls
    for i in range(6):
        p1, p2 = hexagon[i], hexagon[(i + 1) % 6]
        edge_vector = (p2[0] - p1[0], p2[1] - p1[1])
        edge_length = math.sqrt(edge_vector[0]**2 + edge_vector[1]**2)
        edge_normal = (-edge_vector[1] / edge_length, edge_vector[0] / edge_length)
        
        # Ball to edge vector
        ball_to_edge = (ball_x - p1[0], ball_y - p1[1])
        projection = ball_to_edge[0] * edge_normal[0] + ball_to_edge[1] * edge_normal[1]
        
        # Check if the ball is colliding with the edge
        if abs(projection) < BALL_RADIUS:
            ball_vx, ball_vy = reflect((ball_vx, ball_vy), edge_normal)
            ball_x += edge_normal[0] * (BALL_RADIUS - projection)
            ball_y += edge_normal[1] * (BALL_RADIUS - projection)
    
    # Draw hexagon
    pygame.draw.polygon(screen, WHITE, hexagon, 2)
    
    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_x), int(ball_y)), BALL_RADIUS)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
