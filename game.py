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
        self.collisionArea = pygame.Rect(50, 50, 300, 50)

    def run(self):
        while True:
            self.screen.fill((14, 219, 248))

            img_r = pygame.Rect(
                self.cloud_pos[0],
                self.cloud_pos[1],
                self.cloud.get_width(),
                self.cloud.get_height(),
            )

            if img_r.colliderect(self.collisionArea):
                pygame.draw.rect(self.screen, (0, 100, 255), self.collisionArea)
            else:
                pygame.draw.rect(self.screen, (0, 50, 155), self.collisionArea)

            # cloud_r = pygame.Rect(*self.cloud_pos, *self.cloud.get_siz()  )

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
