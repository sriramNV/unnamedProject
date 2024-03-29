import json
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

AUTOTILE_MAP = {
    tuple(sorted([(1, 0), (0, 1)])): 0,
    tuple(sorted([(1, 0), (0, 1), (-1, 0)])): 1,
    tuple(sorted([(-1, 0), (0, 1)])): 2,
    tuple(sorted([(-1, 0), (0, -1), (0, 1)])): 3,
    tuple(sorted([(-1, 0), (0, -1)])): 4,
    tuple(sorted([(-1, 0), (0, -1), (1, 0)])): 5,
    tuple(sorted([(1, 0), (0, -1)])): 6,
    tuple(sorted([(1, 0), (0, -1), (0, 1)])): 7,
    tuple(sorted([(1, 0), (-1, 0), (0, 1), (0, -1)])): 8,
}

AUTOTILE_TYPES = {"grass", "stone"}


class Tilemap:
    def __init__(self, game, tileSize=16):
        self.game = game
        self.tileSize = tileSize
        self.tilemap = {}
        self.offgridTiles = []

    def tilesAround(self, pos):
        tiles = []
        tileLoc = (int(pos[0] // self.tileSize), int(pos[1] // self.tileSize))

        for offset in NEIGHBOUR_OFFSETS:
            checkLoc = str(tileLoc[0] + offset[0]) + ";" + str(tileLoc[1] + offset[1])
            if checkLoc in self.tilemap:
                tiles.append(self.tilemap[checkLoc])
        return tiles

    def render(self, surface, offset=(0, 0)):
        for tile in self.offgridTiles:
            surface.blit(
                self.game.assets[tile["type"]][tile["variant"]],
                (tile["pos"][0] - offset[0], tile["pos"][1] - offset[1]),
            )

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

    # not needed anymore
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

    def save(self, path):
        f = open(path, "w")
        json.dump(
            {
                "tilemap": self.tilemap,
                "tile_size": self.tileSize,
                "offgrid": self.offgridTiles,
            },
            f,
        )
        f.close()

    def load(self, path):
        f = open(path, "r")
        map_data = json.load(f)
        f.close()

        self.tilemap = map_data["tilemap"]
        self.tileSize = map_data["tile_size"]
        self.offgridTiles = map_data["offgrid"]

    def autotile(self):
        for loc in self.tilemap:
            tile = self.tilemap[loc]
            neighbors = set()
            for shift in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
                check_loc = (
                    str(tile["pos"][0] + shift[0])
                    + ";"
                    + str(tile["pos"][1] + shift[1])
                )
                if check_loc in self.tilemap:
                    if self.tilemap[check_loc]["type"] == tile["type"]:
                        neighbors.add(shift)
            neighbors = tuple(sorted(neighbors))
            if (tile["type"] in AUTOTILE_TYPES) and (neighbors in AUTOTILE_MAP):
                tile["variant"] = AUTOTILE_MAP[neighbors]
