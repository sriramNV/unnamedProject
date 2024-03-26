import pygame


class PhysicsEntity:
    def __init__(self, game, eType, pos, size):
        self.game = game
        self.type = eType
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collision = {"up": False, "down": False, "right": False, "left": False}

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):
        self.collision = {"up": False, "down": False, "right": False, "left": False}

        frameMovement = (movement[0] + self.velocity[0], movement[1] + self.velocity[1])

        self.pos[0] += frameMovement[0]
        entityRect = self.rect()
        for rect in tilemap.physicsRectsAround(self.pos):
            if entityRect.colliderect(rect):
                if frameMovement[0] > 0:
                    entityRect.right = rect.left
                    self.collision["right"] = True
                if frameMovement[0] < 0:
                    entityRect.left = rect.right
                    self.collision["left"] = True
                self.pos[0] = entityRect.x

        self.pos[1] += frameMovement[1]
        entityRect = self.rect()
        for rect in tilemap.physicsRectsAround(self.pos):
            if entityRect.colliderect(rect):
                if frameMovement[1] > 0:
                    entityRect.bottom = rect.top
                    self.collision["bottom"] = True
                if frameMovement[1] < 0:
                    entityRect.top = rect.bottom
                    self.collision["top"] = True
                self.pos[1] = entityRect.y

        self.velocity[1] = min(5, self.velocity[1] + 0.1)

        if self.collision["down"] or self.collision["up"]:
            self.velocity[1] = 0

    def render(self, surface, offset=(0, 0)):
        surface.blit(
            self.game.assets["player"],
            (self.pos[0] - offset[0], self.pos[1] - offset[1]),
        )
