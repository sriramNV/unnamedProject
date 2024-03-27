import pygame


NEIGHBOUR_OFFSETS = [
    (-1, 0),
    (-1, -1),
    (0, -1),
    (1, -1),
    (1, 0),
    (0, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]

PHYSICS_TILE = {"grass", "stone"}


class Tilemap:
    def __init__(self, game, tileSize=16):
        self.game = game
        self.tileSize = tileSize
        self.tilemap = {}
        self.offgridTiles = []

        for i in range(10):
            self.tilemap[str(3 + i) + ";10"] = {
                "type": "grass",
                "variant": 1,
                "pos": (3 + i, 10),
            }
            self.tilemap["10;" + str(5 + i)] = {
                "type": "stone",
                "variant": 1,
                "pos": (10, 5 + i),
            }

    def tilesAround(self, pos):
        tiles = []
        tileLoc = (int(pos[0] // self.tileSize), int(pos[1] // self.tileSize))

        for offset in NEIGHBOUR_OFFSETS:
            checkLoc = str(tileLoc[0] + offset[0]) + ";" + str(tileLoc[1] + offset[1])
            if checkLoc in self.tilemap:
                tiles.append(self.tilemap[checkLoc])
        return tiles

    def render(self, surface, offset=(0, 0)):
        for x in range(
            offset[0] // self.tileSize,
            (offset[0] + surface.get_width()) // self.tileSize + 1,
        ):
            for y in range(
                offset[1] // self.tileSize,
                (offset[1] + surface.get_height()) // self.tileSize + 1,
            ):
                loc = str(x) + ";" + str(y)
                if loc in self.tilemap:
                    tile = self.tilemap[loc]
                    surface.blit(
                        self.game.assets[tile["type"]][tile["variant"]],
                        (
                            tile["pos"][0] * self.tileSize - offset[0],
                            tile["pos"][1] * self.tileSize - offset[1],
                        ),
                    )

    # for tile in self.offgridTiles:
    # surface.blit(
    #     self.game.assets[tile["type"]][tile["variant"]],
    #     (tile["pos"][0] - offset[0].tile["pos"][1] - offset[1]),
    # )

    # for location in self.tilemap:
    #     tile = self.tilemap[location]
    #     surface.blit(
    #         self.game.assets[tile["type"]][tile["variant"]],
    #         (
    #             tile["pos"][0] * self.tileSize - offset[0],
    #             tile["pos"][1] * self.tileSize - offset[1],
    #         ),
    #     )

    def physicsRectsAround(self, pos):
        rects = []
        for tile in self.tilesAround(pos):
            if tile["type"] in PHYSICS_TILE:
                rects.append(
                    pygame.Rect(
                        tile["pos"][0] * self.tileSize,
                        tile["pos"][1] * self.tileSize,
                        self.tileSize,
                        self.tileSize,
                    )
                )
        return rects
