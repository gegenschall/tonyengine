import os
from struct import unpack

PALETTE_START_OFFSET    = -0x300 # 768
PALETTE_LENGTH          = 0x300

class Palette:
    def dump_data(self):
        print self.data

class PaletteReader:
    def __init__(self, filename):
        if not self._is_valid_palette_file(filename):
            print('Error opening palette')
            exit(1)

    def _is_valid_palette_file(self, filename):
        PALETTE_START_VALUE     = '\x0c'
        PALETTE_DATA_PATH       = 'data'
            
        pal_file = os.path.join(PALETTE_DATA_PATH, filename)
        if not os.path.exists(pal_file):
            print('Palette file %s does not exist' % (pal_file,))
            return False
        
        self.pal_fh = open(pal_file, 'rb')

        # Check for existence of magic byte before palette start
        self.pal_fh.seek(PALETTE_START_OFFSET - 1, 2)
        magic = self.pal_fh.read(1)
        if magic != PALETTE_START_VALUE:
            print('File does not seem to be a palette')
            return False

        return True

    def get_palette_data(self):
        self.pal_fh.seek(PALETTE_START_OFFSET, 2)
        palb = self.pal_fh.read()
        palb = unpack(str(PALETTE_LENGTH) + 'B', palb)
        
        pal = []
        for i in range(0, PALETTE_LENGTH / 3):
            pal.append( (palb[i*3], palb[i*3 + 1], palb[i*3 + 2]))
        return pal

    def get_palette(self):
        p = Palette()
        p.data      = self.get_palette_data() 
        p.length    = len(p.data)

        return p
