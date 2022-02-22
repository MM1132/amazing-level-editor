import pygame

# The amazing function for loading in all the tiles
def getTexture(tile, size, alpha, resourcepack):
    image = pygame.image.load("./resourcepacks/" + resourcepack + "/tiles/" + tile[0] + ".png").convert()
    part = []
    for i in range(int(image.get_width() / size)):
        rect = pygame.Rect(i * size, 0, size, size)
        texture = pygame.Surface(rect.size)
        texture.blit(image, (0, 0), rect)
        texture.set_colorkey(alpha)
        part.append(texture)
    return [part, j[1]]

TILES = []
# Lets load all the tiles in and save them into the TILES variable :D
with open("./resourcepacks/resourcepack.cfg", "r") as f:
    # Get all the settings for the resourcepack from the config file
    settings = [i.strip().split("=") for i in f]
    for i in range(len(settings)):
        if settings[i][0] == "resourcepack":
            pack = settings[i][1]

# Open the tiles config file
with open("./resourcepacks/" + pack + "/tiles.cfg") as f:
    tiles = [eval(i) for i in f]

# Set all the TILES
for j in tiles:
    TILES.append(getTexture(j, 50, (0, 38, 255), pack))