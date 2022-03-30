import pygame
from app import App

app = App()

while app.isRunning:

    app.update()

    app.draw()

    # --- Limit to 60 frames per second
    app.clock.tick(60)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
