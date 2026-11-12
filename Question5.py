# Question 5 

from graphics import *
import math
import time


# Ball class
class Ball:
    def __init__(self, win, x, height, color):
        self.height = height
        self.velocity = 0
        self.gravity = 9.8
        self.bounces = 0
        self.x = x
        self.radius = 0.4

        self.circle = Circle(
            Point(x, height + self.radius),
            self.radius
        )
        self.circle.setFill(color)
        self.circle.draw(win)

    def update(self, dt):
        # Apply gravity
        self.velocity -= self.gravity * dt

        # Calculate new height
        self.height += self.velocity * dt

        # Check if ball hits the ground
        if self.height <= 0:
            self.height = 0

            if abs(self.velocity) > 0.1:
                self.velocity = (
                    abs(self.velocity) * math.sqrt(0.60)
                )
                self.bounces += 1
            else:
                self.velocity = 0

        # Move the ball
        new_y = self.height + self.radius
        old_y = self.circle.getCenter().getY()

        self.circle.move(0, new_y - old_y)


# Main function
def main():
    height1 = float(input("Enter height for ball 1: "))
    height2 = float(input("Enter height for ball 2: "))
    height3 = float(input("Enter height for ball 3: "))

    max_height = max(height1, height2, height3)

    win = GraphWin("Three Bouncing Balls", 750, 500)
    win.setCoords(0, 0, (max_height + 3) * 1.5, max_height + 3)
    win.setBackground("white")

    # Draw ground
    ground = Line(Point(0, 0), Point((max_height + 3) * 1.5, 0))
    ground.setWidth(3)
    ground.draw(win)

    # Create three balls
    ball1 = Ball(win, 3, height1, "red")
    ball2 = Ball(win, 7.5, height2, "blue")
    ball3 = Ball(win, 12, height3, "green")

    balls = [ball1, ball2, ball3]

    dt = 0.02

    # Animate the balls
    while True:
        moving = False

        for ball in balls:
            ball.update(dt)

            if ball.height > 0 or ball.velocity != 0:
                moving = True

        if not moving:
            break

        update()
        time.sleep(dt)

    print("\nTotal bounces:")
    print("Ball 1:", ball1.bounces)
    print("Ball 2:", ball2.bounces)
    print("Ball 3:", ball3.bounces)

    win.getMouse()
    win.close()


main()