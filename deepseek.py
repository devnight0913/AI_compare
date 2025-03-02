import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bouncing Ball in Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Clock
clock = pygame.time.Clock()

# Hexagon properties
hexagon_radius = 200
hexagon_center = (WIDTH // 2, HEIGHT // 2)
hexagon_angle = 0  # Rotation angle
hexagon_angular_speed = 0.01  # Rotation speed

# Ball properties
ball_radius = 20
ball_pos = [hexagon_center[0], hexagon_center[1] - hexagon_radius + ball_radius]
ball_velocity = [2, 0]  # Initial velocity
gravity = 0.1
friction = 0.99

# Function to calculate hexagon vertices
def calculate_hexagon_vertices(center, radius, angle):
    vertices = []
    for i in range(6):
        x = center[0] + radius * math.cos(math.radians(60 * i) + angle)
        y = center[1] + radius * math.sin(math.radians(60 * i) + angle)
        vertices.append((x, y))
    return vertices

# Function to check collision between ball and hexagon walls
def check_collision(ball_pos, ball_radius, hexagon_vertices):
    for i in range(len(hexagon_vertices)):
        p1 = hexagon_vertices[i]
        p2 = hexagon_vertices[(i + 1) % len(hexagon_vertices)]
        
        # Vector from p1 to p2
        wall_vector = (p2[0] - p1[0], p2[1] - p1[1])
        # Vector from p1 to ball
        ball_vector = (ball_pos[0] - p1[0], ball_pos[1] - p1[1])
        
        # Project ball_vector onto wall_vector
        dot_product = (ball_vector[0] * wall_vector[0] + ball_vector[1] * wall_vector[1])
        wall_length_squared = wall_vector[0]**2 + wall_vector[1]**2
        projection = (dot_product / wall_length_squared)
        
        # Closest point on the wall to the ball
        closest_point = (
            p1[0] + projection * wall_vector[0],
            p1[1] + projection * wall_vector[1]
        )
        
        # Distance from ball to closest point
        distance = math.sqrt((ball_pos[0] - closest_point[0])**2 + (ball_pos[1] - closest_point[1])**2)
        
        if distance <= ball_radius:
            # Calculate normal vector of the wall
            normal = (-wall_vector[1], wall_vector[0])
            normal_length = math.sqrt(normal[0]**2 + normal[1]**2)
            normal = (normal[0] / normal_length, normal[1] / normal_length)
            
            # Reflect ball velocity
            dot = ball_velocity[0] * normal[0] + ball_velocity[1] * normal[1]
            ball_velocity[0] -= 2 * dot * normal[0]
            ball_velocity[1] -= 2 * dot * normal[1]
            
            # Move ball outside the wall to avoid sticking
            overlap = ball_radius - distance
            ball_pos[0] += overlap * normal[0]
            ball_pos[1] += overlap * normal[1]
            
            return True
    return False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update hexagon rotation
    hexagon_angle += hexagon_angular_speed
    hexagon_vertices = calculate_hexagon_vertices(hexagon_center, hexagon_radius, hexagon_angle)

    # Update ball position and velocity
    ball_velocity[1] += gravity  # Apply gravity
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]
    
    # Apply friction
    ball_velocity[0] *= friction
    ball_velocity[1] *= friction

    # Check for collisions with hexagon walls
    if check_collision(ball_pos, ball_radius, hexagon_vertices):
        pass  # Collision handling is done inside the function

    # Clear screen
    screen.fill(WHITE)

    # Draw hexagon
    pygame.draw.polygon(screen, BLACK, hexagon_vertices, 2)

    # Draw ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()