import pygame
from Button import Button
from FileBrowser import FileBrowser
from TextBox import TextBox
class Menu:
    def __init__(self):
        # The current state and the background of the menu
        self.state = 0

        # Get and set background
        with open("./resourcepacks/resourcepack.cfg", "r") as f:
            # Get all the settings for the resourcepack from the config file
            settings = [i.strip().split("=") for i in f]
            for i in range(len(settings)):
                if settings[i][0] == "resourcepack":
                    pack = settings[i][1]
        self.background = pygame.image.load("./resourcepacks/" + pack + "/forest.png").convert()

        # Configure manu's elements (buttons, file browers, etc..)
        self.elements = {
            0: [Button("Create new", 2, ["centered", 300]), Button("Load level", 1, ["centered", 400]), Button("Exit", "quit", ["centered", 500])],
            1: [FileBrowser("./saves/", ".map", ["centered", 200]), Button("Back", 0, ["centered", 800])],
            2: [TextBox(60, ["centered", 300]), Button("Create", "createNew", ["centered", 750]), Button("Back", 0, ["centered", 800])]
        }

    # Render all of menu
    def render(self, window):
        window.blit(self.background, (0, 0))
        for i in self.elements[self.state]:
            i.render(window)

    # Get input from the user and do stuff according to it
    def getInput(self):
        for event in pygame.event.get():
            # ALL OF QUITTING CODE
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.KEYDOWN:
                # If we have a textbox in our current state, update it
                for i in self.elements[self.state]:
                    if type(i) == TextBox:
                        i.update(event)

                # Quit the manu if escape is pressed
                if event.key == pygame.K_ESCAPE:
                    return "quit"

            # HANDLE PRESSES OF THE BUTTONS
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for i in self.elements[self.state]:
                        if type(i) == Button:
                            if i.hover:
                                if type(i.returnValue) == int:
                                    self.state = i.returnValue
                                elif type(i.returnValue) == str:
                                    if i.returnValue == "createNew":
                                        for i in self.elements[self.state]:
                                            if type(i) == TextBox:
                                                # Clear the textBox from text
                                                saveFile = i.text; i.text = ""
                                                return "./saves/" + saveFile + ".map"
                                    return i.returnValue
                        elif type(i) == FileBrowser:
                            for j in i.elements:
                                if j.hover:
                                    if type(j) == Button:
                                        return j.returnValue