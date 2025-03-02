import pygame
import sys
import math
import numpy as np

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Bouncing in a Spinning Hexagon")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Physics constants
GRAVITY = 0.3
FRICTION = 0.98
ELASTICITY = 0.8
HEX_ROTATION_SPEED = 0.01  # radians per frame

# Ball properties
ball_radius = 15
ball_pos = np.array([WIDTH/2, HEIGHT/2], dtype=float)
ball_vel = np.array([2.0, 1.0], dtype=float)

# Hexagon properties
hex_center = np.array([WIDTH/2, HEIGHT/2])
hex_radius = 200
hex_angle = 0  # Current rotation angle

def get_hexagon_vertices():
    """Get the current vertices of the hexagon based on rotation."""
    vertices = []
    for i in range(6):
        angle = hex_angle + i * (2 * math.pi / 6)
        x = hex_center[0] + hex_radius * math.cos(angle)
        y = hex_center[1] + hex_radius * math.sin(angle)
        vertices.append((x, y))
    return vertices

def get_hexagon_edges():
    """Get the edges (line segments) of the hexagon."""
    vertices = get_hexagon_vertices()
    edges = []
    for i in range(6):
        edges.append((vertices[i], vertices[(i+1) % 6]))
    return edges

def reflect_velocity(normal):
    """Reflect the ball's velocity based on the normal vector of collision."""
    global ball_vel
    # Normalize the normal vector
    normal = normal / np.linalg.norm(normal)
    
    # Calculate the reflection
    dot_product = np.dot(ball_vel, normal)
    ball_vel = ball_vel - (1 + ELASTICITY) * dot_product * normal
    
    # Apply friction
    ball_vel *= FRICTION

def point_line_distance(point, line_start, line_end):
    """Calculate the distance from a point to a line segment."""
    line_vec = np.array(line_end) - np.array(line_start)
    point_vec = np.array(point) - np.array(line_start)
    line_len = np.linalg.norm(line_vec)
    line_unitvec = line_vec / line_len
    point_vec_scaled = point_vec / line_len
    
    t = np.clip(np.dot(line_unitvec, point_vec_scaled), 0, 1)
    nearest = np.array(line_start) + t * line_vec
    dist = np.linalg.norm(np.array(point) - nearest)
    return dist, nearest

def get_collision_normal(point, nearest):
    """Get the normal vector pointing from the nearest point on the edge to the ball center."""
    normal = np.array(point) - np.array(nearest)
    if np.linalg.norm(normal) > 0:
        normal = normal / np.linalg.norm(normal)
    return normal

def check_ball_hexagon_collision():
    """Check if the ball collides with any of the hexagon edges."""
    edges = get_hexagon_edges()
    
    for edge in edges:
        dist, nearest = point_line_distance(ball_pos, edge[0], edge[1])
        
        if dist <= ball_radius:
            # Collision detected, move the ball outside the edge
            normal = get_collision_normal(ball_pos, nearest)
            ball_pos[0] = nearest[0] + normal[0] * ball_radius
            ball_pos[1] = nearest[1] + normal[1] * ball_radius
            
            # Reflect the velocity
            reflect_velocity(normal)
            
            return True
    
    return False

def update():
    """Update the game state."""
    global ball_pos, ball_vel, hex_angle
    
    # Update the ball position and velocity
    ball_vel[1] += GRAVITY  # Apply gravity
    ball_pos += ball_vel
    
    # Rotate the hexagon
    hex_angle += HEX_ROTATION_SPEED
    
    # Check for collisions
    check_ball_hexagon_collision()

def draw():
    """Draw the game state."""
    screen.fill(BLACK)
    
    # Draw the hexagon
    vertices = get_hexagon_vertices()
    pygame.draw.polygon(screen, WHITE, vertices, 2)
    
    # Draw the ball
    pygame.draw.circle(screen, RED, (int(ball_pos[0]), int(ball_pos[1])), ball_radius)
    
    pygame.display.flip()

def main():
    """Main game loop."""
    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        update()
        draw()
        clock.tick(60)

if __name__ == "__main__":
    main()