import os
from struct import unpack

TILE_WIDTH      = 16
TILE_HEIGHT     = 16
TILE_SIZE       = 256
    
class Tileset:
    pass

class TilesetReader:
    def __init__(self, filename, palette):
        if not self._is_valid_tileset_file(filename):
            print('Unknown or wrong tileset file format')
            exit(1)
        
        self.palette = palette

    def _is_valid_tileset_file(self, filename):
        TILESET_DATA_PATH = 'data'

        ts_file = os.path.join(TILESET_DATA_PATH, filename)
        if not os.path.exists(ts_file):
            print('The tileset file %s does not exist' % (ts_file,))
            return False

        # Each tileset file is always a multiple of 256 byte:
        size = os.path.getsize(ts_file)

        if size % TILE_SIZE == 0:
            self.fh_ts = open(ts_file, 'rb')
            self.filesize = size
            return True

        return False

    def get_num_tiles(self):
        # Each tile is 16x16 pixel => 256 byte
        return self.filesize / TILE_SIZE

    def extract_tile(self, tilenumber):
        # calculate start position and seek in file
        offset = tilenumber * TILE_SIZE
        self.fh_ts.seek(offset)
        data = unpack(str(TILE_SIZE) + 'B', self.fh_ts.read(TILE_SIZE))

        tile = []
        for i in range(TILE_WIDTH):
            row = []
            for j in range(TILE_HEIGHT):
                # I can tell by the pixels
                row.append(data[i * TILE_WIDTH + j])
            tile.append(row)

        return self.deinterleave(tile)
    
    def deinterleave(self, tile):
        # Images appear to be optimized by interleaving
        # with factor 4
        INTERLEAVING_FACTOR = 4
        
        for i in range(TILE_WIDTH):
            for j in range(0, TILE_WIDTH, INTERLEAVING_FACTOR):


    def apply_palette(self, tiledata):
       pass

    def get_all_tiles(self):
        num_tiles = self.get_num_tiles()
        
        tiles = []
        for i in range(num_tiles):
            tile = self.extract_tile(i)
            tiles.append(tile)

        return tiles

    def get_tileset(self):
        t = Tileset()
        t.data = self.get_all_tiles()
        t.num = self.get_num_tiles()
        return t
