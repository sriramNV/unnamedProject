import pygame
import sys


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption("UNNAMED PROJECT")
        self.screen = pygame.display.set_mode((640, 480))

        self.clock = pygame.time.Clock()

        self.cloud = pygame.image.load("./data/images/clouds/cloud_1.png")
        self.cloud.set_colorkey((0, 0, 0))
        self.cloud_pos = [160, 260]
        self.movement = [False, False]

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))

            self.cloud_pos[1] += (self.movement[1] - self.movement[0]) * 5
            self.screen.blit(self.cloud, self.cloud_pos)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.movement[0] = True
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.movement[0] = False
                    if event.key == pygame.K_DOWN:
                        self.movement[1] = False

            pygame.display.update()
            self.clock.tick(60)


Game().run()
