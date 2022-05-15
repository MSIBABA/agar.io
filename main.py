import pygame, random, math

# Dimension Definitions
SCREEN_WIDTH, SCREEN_HEIGHT = (800, 800)
PLATFORM_WIDTH, PLATFORM_HEIGHT = (800, 800)

# Other Definitions
NAME = "agario"
VERSION = ''

# Pygame initialization
pygame.init()
pygame.display.set_caption("{} {}".format(NAME, VERSION))
clock = pygame.time.Clock()
try:
    font = pygame.font.Font("Ubuntu-B.ttf", 20)
    big_font = pygame.font.Font("Ubuntu-B.ttf", 24)
except:
    print("Font file not found: Ubuntu-B.ttf")
    font = pygame.font.SysFont('Ubuntu', 20, True)
    big_font = pygame.font.SysFont('Ubuntu', 24, True)

# Surface Definitions
MAIN_SURFACE = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
SCOREBOARD_SURFACE = pygame.Surface((95, 25), pygame.SRCALPHA)
LEADERBOARD_SURFACE = pygame.Surface((155, 250), pygame.SRCALPHA)
SCOREBOARD_SURFACE.fill((30, 50, 50, 50))
LEADERBOARD_SURFACE.fill((30, 50, 50, 50))


# Auxiliary Functions
def drawText(message, pos, color=(255, 255, 255)):
    """Blits text to main (global) screen.
    """
    MAIN_SURFACE.blit(font.render(message, 1, color), pos)


def getDistance(a, b):
    """Calculates Euclidean distance between given points.
    """
    diffX = math.fabs(a[0] - b[0])
    diffY = math.fabs(a[1] - b[1])
    return ((diffX ** 2) + (diffY ** 2)) ** (0.5)


# Auxiliary Classes
class Painter:


    def __init__(self):
        self.paintings = []

    def add(self, drawable):
        self.paintings.append(drawable)

    def paint(self):
        for drawing in self.paintings:
            drawing.draw()


class Camera:
    """Used to represent the concept of POV.
    """

    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = SCREEN_WIDTH
        self.height = SCREEN_HEIGHT
        self.zoom = 0.5

    def centre(self, blobOrPos):
        """Makes sure that the given object will be at the center of player's view.
        Zoom is taken into account as well.
        """
        if isinstance(blobOrPos, Player):
            x, y = blobOrPos.x, blobOrPos.y
            self.x = (x - (x * self.zoom)) - x + (SCREEN_WIDTH / 2)
            self.y = (y - (y * self.zoom)) - y + (SCREEN_HEIGHT / 2)
        elif type(blobOrPos) == tuple:
            self.x, self.y = blobOrPos

    def update(self, target):
        self.zoom = 70 / (target.mass) + 0.2
        self.centre(blob)


class Drawable:
    """Used as an abstract base-class for every drawable element.
    """

    def __init__(self, surface, camera):
        self.surface = surface
        self.camera = camera

    def draw(self):
        pass


class Grid(Drawable):
    """Used to represent the backgroun grid.
    """

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.color = (230, 240, 240)

    def draw(self):
        # A grid is a set of horizontal and prependicular lines
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        for i in range(0, 2001, 25):
            pygame.draw.line(self.surface, self.color, (x, i * zoom + y), (2001 * zoom + x, i * zoom + y), 3)
            pygame.draw.line(self.surface, self.color, (i * zoom + x, y), (i * zoom + x, 2001 * zoom + y), 3)


class HUD(Drawable):
    """Used to represent all necessary Head-Up Display information on screen.
    """

    def __init__(self, surface, camera):
        super().__init__(surface, camera)



class Player(Drawable):

    COLOR_LIST = [
        (255, 50, 255),]

    FONT_COLOR = (50, 50, 50)

    def __init__(self, surface, camera, name=""):
        super().__init__(surface, camera)
        self.x = random.randint(100, 400)
        self.y = random.randint(100, 400)
        self.mass = 20
        self.speed = 4
        self.color = col = random.choice(Player.COLOR_LIST)
        self.outlineColor = (
            int(col[0] - col[0] / 3),
            int(col[1] - col[1] / 3),
            int(col[2] - col[2] / 3))
        if name:
            self.name = name
        else:
            self.name = "Anonymous"
        self.pieces = []

    def collisionDetection(self, edibles):

        for edible in edibles:
            if (getDistance((edible.x, edible.y), (self.x, self.y)) <= self.mass / 2):
                self.mass += 0.5
                edibles.remove(edible)

    def move(self):

        dX, dY = pygame.mouse.get_pos()
        # Find the angle from the center of the screen to the mouse in radians [-Pi, Pi]
        rotation = math.atan2(dY - float(SCREEN_HEIGHT) / 2, dX - float(SCREEN_WIDTH) / 2)
        # Convert radians to degrees [-180, 180]
        rotation *= 100 / math.pi
        # Normalize to [-1, 1]
        # First project the point from unit circle to X-axis
        # Then map resulting interval to [-1, 1]
        normalized = (50 - math.fabs(rotation)) / 50
        vx = self.speed * normalized
        vy = 0
        if rotation < 0:
            vy = -self.speed + math.fabs(vx)
        else:
            vy = self.speed - math.fabs(vx)
        tmpX = self.x + vx
        tmpY = self.y + vy
        self.x = tmpX
        self.y = tmpY

    def draw(self):
        """Draws the player as an outlined circle.
        """
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))

        # Draw the ouline of the player as a darker, bigger circle
        pygame.draw.circle(self.surface, self.outlineColor, center, int((self.mass / 2 ) * zoom))
        # Draw the actual player as a circle
        pygame.draw.circle(self.surface, self.color, center, int(self.mass / 2 * zoom))
        # Draw player's name
        fw, fh = font.size(self.name)
        drawText(self.name, (self.x * zoom + x - int(fw / 2), self.y * zoom + y - int(fh / 2)),
                 Player.FONT_COLOR)


class Cell(Drawable):  # Semantically, this is a parent class of player

    CELL_COLORS = [
        (80, 252, 54),
        (36, 244, 255),
        (243, 31, 46),
        (4, 39, 243),]

    def __init__(self, surface, camera):
        super().__init__(surface, camera)
        self.x = random.randint(20, 1980)
        self.y = random.randint(20, 1980)
        self.mass = 2
        self.color = random.choice(Cell.CELL_COLORS)

    def draw(self):
        """Draws a cell as a simple circle.
        """
        zoom = self.camera.zoom
        x, y = self.camera.x, self.camera.y
        center = (int(self.x * zoom + x), int(self.y * zoom + y))
        pygame.draw.circle(self.surface, self.color, center, int(self.mass * zoom))


class CellList(Drawable):

    def __init__(self, surface, camera, numOfCells):
        super().__init__(surface, camera)
        self.count = numOfCells
        self.list = []
        for i in range(self.count): self.list.append(Cell(self.surface, self.camera))

    def draw(self):
        for cell in self.list:
            cell.draw()


# Initialize essential entities
cam = Camera()

grid = Grid(MAIN_SURFACE, cam)
cells = CellList(MAIN_SURFACE, cam, 1500)
blob = Player(MAIN_SURFACE, cam, "DP-SM")
hud = HUD(MAIN_SURFACE, cam)

painter = Painter()
painter.add(grid)
painter.add(cells)
painter.add(blob)
painter.add(hud)

# Game main loop
while (True):

    clock.tick(30)

    for e in pygame.event.get():
        if (e.type == pygame.KEYDOWN):
            if (e.key == pygame.K_ESCAPE):
                pygame.quit()
                quit()
            if (e.key == pygame.K_SPACE):
                del (cam)
                blob.split()
            if (e.key == pygame.K_w):
                blob.feed()
        if (e.type == pygame.QUIT):
            pygame.quit()
            quit()

    blob.move()
    blob.collisionDetection(cells.list)
    cam.update(blob)
    MAIN_SURFACE.fill((242, 251, 255))
    # Uncomment next line to get dark-theme
    # surface.fill((0,0,0))
    painter.paint()
    # Start calculating next frame
    pygame.display.flip()
