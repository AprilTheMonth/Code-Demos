import pygame
import math

SCREENX = 1280
SCREENY = 720
NUMLINES = 100
WALLHEIGHT = 100
LINELENGTH = math.pow(SCREENX + SCREENY, 2)

class player:
    def __init__(self):
        # Initilization function, resets player to middle of the screen, facing the boxes
        self.pos = pygame.Vector2(SCREENX / 2, SCREENY / 2)
        self.theta = 180
        self.firstPerson = False
        self.spacePressed = False

    def update(self, dt):
        # Updates the player's position based on keypresses

        # Get keypresses
        keys = pygame.key.get_pressed()

        # Move forward
        if keys[pygame.K_w]:
            if self.firstPerson:
                self.pos.y += 300 * math.sin(self.theta) * dt
                self.pos.x += 300 * math.cos(self.theta) * dt
            else:
                self.pos.y -= 300 * dt

        # Move back
        if keys[pygame.K_s]:
            if self.firstPerson:
                self.pos.y -= 300 * math.sin(self.theta) * dt
                self.pos.x -= 300 * math.cos(self.theta) * dt
            else:
                self.pos.y += 300 * dt

        # Move to the right (or rotate if in first person)
        if keys[pygame.K_a]:
            if self.firstPerson:
                self.theta -= 2 * dt
            else:   
                self.pos.x -= 300 * dt

        # Move to the left (or rotate if in first person)
        if keys[pygame.K_d]:
            if self.firstPerson:
                self.theta += 2 * dt
            else:
                self.pos.x += 300 * dt

        # Rotate if not in first person
        if keys[pygame.K_RIGHT] and not self.firstPerson:
            self.theta += 2 * dt
        if keys[pygame.K_LEFT] and not self.firstPerson:
            self.theta -= 2 * dt

        # Trigger first person / overhead perspective
        if keys[pygame.K_SPACE]:
            # Wait until the space has been released before changing again
            # Prevents flickering back and forth
            if not self.spacePressed:
                self.firstPerson = not self.firstPerson
                self.spacePressed = True
        else:
            self.spacePressed = False

    def getSightLines(self,screen, obstacles):
        lines = []
        for i in range((0 - NUMLINES), NUMLINES):
            # Cast one ray
            line = pygame.Vector2(self.pos.x + math.cos(self.theta+(i/NUMLINES)) * LINELENGTH, self.pos.y + math.sin(self.theta+(i/NUMLINES)) * LINELENGTH)
            lines.append(line)
            hasCollision = False
            closestCollission = pygame.Vector2(0,0)
            # For each obstacles in the list
            # note: This wouldn't scale well in situations with a lot of objects
            # This demo is mostly to show that I understand the principles behind raycasting
            # In a more efficient version, the obstacles would be checked according to their distance to the player
            # and the loop would break as soon as a collision is found
            for obstacle in obstacles:
                # Clipline returns the portion of the line within a box
                collision = obstacle.clipline(self.pos.x, self.pos.y, line.x, line.y)
                # If there is nothing in collision, that means the ray doesn't intersect with the box
                if len(collision) > 0:
                    # Clip the line so only a closer collision will update it
                    line = pygame.Vector2(collision[0])
                    closestCollission = line
                    hasCollision = True
            if not self.firstPerson:
                # only draw sightlines if the game is in topdown view
                pygame.draw.line(screen, "white", self.pos, line)
            else:
                # If the line collided with a box & the game is in first person view
                if hasCollision:
                    # ((i + NUMLINES) / (2 * NUMLINES)) gets the position of the line as a normalized value where 0 = the leftmost line and 1 = the rightmost line
                    # Then, multiply that number by the screen width
                    xpos = ((i + NUMLINES) / (2 * NUMLINES)) * SCREENX
                    dist = self.pos.distance_to(closestCollission)
                    # Scale the height of the box by the distance to the box, so the further it is, the shorter it is
                    height = (WALLHEIGHT / (2 * dist)) * SCREENY
                    # Box always appears in the middle of the screen
                    yTop = (SCREENY / 2) + height
                    yBottom = (SCREENY / 2) - height
                    top = pygame.Vector2(xpos, yTop)
                    bottom = pygame.Vector2(xpos, yBottom)
                    # Scale the color so further boxes appear darker
                    color = int(min(25000/pow(dist,2), 0) * 255)
                    # For each line that sees a box, draw a single vertical line on the screen
                    pygame.draw.line(screen, pygame.Color(color, color, color), top, bottom, width=15)

def main():
    # Set up pygame interface
    pygame.init()
    screen = pygame.display.set_mode((SCREENX, SCREENY))
    clock = pygame.time.Clock()
    running = True
    dt = 0

    # Create boxes
    obstacles = []
    obstacles.append(pygame.Rect(200, 200, 50, 50))
    obstacles.append(pygame.Rect(300, 200, 50, 50))

    # Create players
    chara = player()

    # Main loop
    while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("black")

        # Draw the player (if not in first person)
        if(not chara.firstPerson):
            pygame.draw.circle(screen, "white", chara.pos, 20)

        # Raycast to 
        chara.getSightLines(screen, obstacles)

        chara.update(dt)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # Get time since last frame
        dt = clock.tick(60) / 1000  # limits FPS to 60

if __name__ == "__main__":
    main()
