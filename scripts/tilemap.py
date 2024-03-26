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

    def render(self, surface):

        for tile in self.offgridTiles:
            surface.blit(self.game.assets[tile["type"]][tile["variant"]], tile["pos"])

        for location in self.tilemap:
            tile = self.tilemap[location]
            surface.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] * self.tileSize, tile["pos"][1] * self.tileSize),
            )
