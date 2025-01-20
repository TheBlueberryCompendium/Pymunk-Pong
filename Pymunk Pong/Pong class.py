import pygame
import pymunk
from sys import exit

pygame.init()

display = pygame.display.set_mode((1000, 600))
clock = pygame.time.Clock()
space = pymunk.Space()
FPS = 50

left = 50
right = 950
top = 25
bottom = 575
middle_x = 500
middle_y = 300


class Ball:
    def __init__(self):
        self.body = pymunk.Body()
        self.body.position = middle_x, middle_y
        self.body.velocity = 400, -300
        self.shape = pymunk.Circle(self.body, 8)
        self.shape.density = 1
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self):
        x, y = self.body.position
        pygame.draw.circle(display, (255, 255, 255), (int(x), int(y)), 8)

    def reset(self):
        self.body.position = middle_x, middle_y
        self.body.velocity = 400, -300


class Wall:
    def __init__(self, p1, p2):
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shape = pymunk.Segment(self.body, p1, p2, 10)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self):
        pygame.draw.line(display, (255, 255, 255), self.shape.a, self.shape.b, 10)


class Player:
    def __init__(self, x):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, middle_y
        self.shape = pymunk.Segment(self.body, [0, -30], [0, 30], 10)
        self.shape.elasticity = 1
        space.add(self.body, self.shape)

    def draw(self):
        p1 = self.body.local_to_world(self.shape.a)
        p2 = self.body.local_to_world(self.shape.b)
        pygame.draw.line(display, (255, 255, 255), p1, p2, 10)

    def move_up(self):
        self.body.velocity = (0, -600)

    def move_down(self):
        self.body.velocity = (0, 600)

    def stop(self):
        self.body.velocity = pymunk.Vec2d(0, 0)


def game():
    ball = Ball()
    wall_left = Wall([left, top], [left, bottom])
    wall_right = Wall([right, top], [right, bottom])
    wall_top = Wall([left, top], [right, top])
    wall_bottom = Wall([left, bottom], [right, bottom])
    player1 = Player(left + 15)
    player2 = Player(right - 15)

    def ball_scored(arbiter, space, data):
        """Reset the ball when it scores on either side."""
        ball.reset()
        return True

    # Add collision handler for scoring
    collision_handler = space.add_collision_handler(1, 2)
    collision_handler.begin = ball_scored

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        keys = pygame.key.get_pressed()
        # Player 2
        if keys[pygame.K_UP] and player2.body.position.y > top+55:
            player2.move_up()
        elif keys[pygame.K_DOWN] and player2.body.position.y < bottom-55:
            player2.move_down()
        else:
            player2.stop()
        # Player 1
        if keys[pygame.K_w] and player1.body.position.y > top+55:
            player1.move_up()
        elif keys[pygame.K_s] and player1.body.position.y < bottom-55:
            player1.move_down()
        else:
            player1.stop()

        display.fill((0, 0, 0))
        ball.draw()
        wall_left.draw()
        wall_right.draw()
        wall_bottom.draw()
        wall_top.draw()
        player1.draw()
        player2.draw()

        pygame.display.update()
        clock.tick(FPS)
        space.step(1 / FPS)


game()
