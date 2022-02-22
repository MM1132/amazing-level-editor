import pygame
from Tile import Tile
from glob import glob

# Weather there is a tile at the specifiead coords or not...
def tileInPos(tiles, pos):
    for i in tiles:
        if i.tilePos == pos:
            return True
            break
    return False

class Map:
    # Jah jah jah...
    # Load in the whole map from the provided file
    def __init__(self, file):
        self.file = file

        # If the saveFile already exists, just read it
        if file in glob("./saves/*.map"):
            with open(self.file, "r") as f:
                info = [list(map(int, i.strip().split(" "))) for i in f]
            self.tiles = []
            if info != []:
                self.tiles = [Tile([i[0], i[1]], i[2], i[3]) for i in info]
            del info
        # If the saveFile doesn't exist, create it (:
        else:
            with open(self.file, "w") as f:
                self.tiles = []

        self.size = [28, 20]
        self.offset = [(1920-(self.size[0] * 50))//2, (1080-(self.size[1] * 50))//2 + 25]
        self.centerOffset = list(self.offset)

        self.mouse = [0, 0]

        self.carelessPlace = False

        self.tileFont = pygame.font.SysFont("Consolas", 50)

        levelNameFont = pygame.font.SysFont("Consolas", 60)
        self.renderLevelName = levelNameFont.render(self.file, 1, (0, 0, 0))


        ## LOAD IN THE BACKGROUDN IMAGE
        with open("./resourcepacks/resourcepack.cfg", "r") as f:
            # Get all the settings for the resourcepack from the config file
            settings = [i.strip().split("=") for i in f]
            for i in range(len(settings)):
                if settings[i][0] == "resourcepack":
                    pack = settings[i][1]
        self.background = pygame.image.load("./resourcepacks/" + pack + "/goodback.png").convert()

    # Set the camera to center
    def centerCamera(self):
        self.offset = list(self.centerOffset)

    # Change the offset of the tiles if middle click gets pressed...
    def update(self, middle):
        if middle:
            if pygame.mouse.get_pos()[0] < self.mouse[0]:
                self.offset[0] -= abs(self.mouse[0]-pygame.mouse.get_pos()[0])
            if pygame.mouse.get_pos()[0] >= self.mouse[0]:
                self.offset[0] += abs(self.mouse[0]-pygame.mouse.get_pos()[0])
            if pygame.mouse.get_pos()[1] < self.mouse[1]:
                self.offset[1] -= abs(self.mouse[1]-pygame.mouse.get_pos()[1])
            if pygame.mouse.get_pos()[1] >= self.mouse[1]:
                self.offset[1] += abs(self.mouse[1]-pygame.mouse.get_pos()[1])
        self.mouse = pygame.mouse.get_pos()

    # Render out all the tiles using the render function from the Tile class
    def render(self, window):
        # Render the background image
        window.blit(self.background, (self.offset[0], self.offset[1]))

        for i in self.tiles:
            i.render(window, self.offset)

        if self.carelessPlace:color = (255, 0, 0)
        else: color = (0, 0, 0)
        pygame.draw.rect(window, color, (self.offset[0], self.offset[1], self.size[0]*50, self.size[1]*50), 2)

        window.blit(self.renderLevelName, (self.offset[0], self.offset[1] - 60))

    def renderTileNumbers(self, window):
        for i in self.tiles:
            count = 0
            for j in self.tiles:
                if i.tilePos == j.tilePos: count += 1
            fontRender = self.tileFont.render(str(count), 1, (0, 0, 0))
            window.blit(fontRender, (i.renderPos[0] + self.offset[0] + 11, i.renderPos[1] + self.offset[1] + 2, 50, 50))

    def toggleCarelessPlace(self):
        if self.carelessPlace:
            self.carelessPlace = False
        else:
            self.carelessPlace = True

    # Place down a tile into the fucking map
    def placeTile(self, selection):
        mouse = [(pygame.mouse.get_pos()[0] - self.offset[0]) // 50, (pygame.mouse.get_pos()[1] - self.offset[1]) // 50]
        # If the coords aren't outside of the maps area
        if mouse[0] > -1 and mouse[0] < self.size[0] and mouse[1] > -1 and mouse[1] < self.size[1]:
            if self.carelessPlace:
                self.tiles.append(Tile(mouse, selection[0], selection[1]))
            else:
                if tileInPos(self.tiles, mouse):
                    self.removeTile()
                self.tiles.append(Tile(mouse, selection[0], selection[1]))

    # Remove a tile at mouses coordinates
    def removeTile(self):
        mouse = [(pygame.mouse.get_pos()[0] - self.offset[0]) // 50, (pygame.mouse.get_pos()[1] - self.offset[1]) // 50]

        for i in range(len(self.tiles)):
            if self.tiles[i].tilePos == mouse:
                del self.tiles[i]
                break

    # Save the map into the fuckin' file when it's closed
    def save(self):
        with open(self.file, "w") as f:
            for i in self.tiles:
                f.write(str(i.tilePos[0]) + " " + str(i.tilePos[1]) + " " + str(i.type) + " " + str(i.texture) + "\n")