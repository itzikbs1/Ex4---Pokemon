import pygame


# This class represents a gui button

class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self, surface):
        """
        This functions draws the button on the gui interface
        :param surface:  The screen surface
        :return: True if the button was pressed, false if not.
        """
        action = False
        pos = pygame.mouse.get_pos()  # get mouse pos to check where it is located
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False: # if the mouse was pressed set paramters to true
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action
