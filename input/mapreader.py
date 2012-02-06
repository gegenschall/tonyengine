import os
import sys
import re
import logging
from struct import unpack

class Map:
    width   = -1
    height  = -1
    data    = []
    world   = -1
    level   = -1
    unknown = -1

    def dump_data_ascii(self):
        pass

class MapReader:
    """Reads .map and .are files and wraps them in easier to
    understand datastructures"""
    def __init__(self, filename):
        self.l = logging.getLogger(self.__class__.__name__)
        if not self._is_valid_map_file(filename):
            print('Invalid map file. Exiting...')
            exit(1)
    
    def _is_valid_map_file(self, filename):
        MAP_HEADER_MAGIC    = 'TLE1'
        VALID_WORLDS        = range(1, 3)
        VALID_LEVELS        = range(0, 7)
        MAP_DATA_PATH       = 'data'
        MAP_NAME_PATTERN    = re.compile('w(\d)l(\d)\.map')
    
        match = re.match(MAP_NAME_PATTERN, filename)

        self.world, self.level = (int(match.group(1)), int(match.group(2)))
        if not (self.world in VALID_WORLDS and self.level in VALID_LEVELS):
            print('Invalid world or level.')
            return False
        
        map_file = os.path.join(MAP_DATA_PATH, filename)
        if not os.path.exists(map_file):
            print('Map file %s does not exists' % (map_file, ))
            return False
        else:
            self.map_fh = open(map_file, 'rb')

        # the first 4 bytes must contain the magic bytes
        self.map_fh.seek(0)
        magic = unpack('cccc', self.map_fh.read(4))
        if not "".join(magic) == MAP_HEADER_MAGIC:
            print('Map file does not contain correct header')
            return False

        return True

    def get_map_dimensions(self):
        MAP_WIDTH_OFFSET    = 0x04
        MAP_HEIGHT_OFFSET   = 0x06
        MAP_DIMENSION_TYPE  = '>H'

        # the dimensions are stored at offset
        # 4 (width) and
        # 6 (height)
        # as 16-bit unsigned integers in big-endian
        self.map_fh.seek(MAP_WIDTH_OFFSET)
        width = unpack(MAP_DIMENSION_TYPE, self.map_fh.read(2))[0]
        self.map_fh.seek(MAP_HEIGHT_OFFSET)
        height = unpack(MAP_DIMENSION_TYPE, self.map_fh.read(2))[0]
        
        return (width, height)

    def get_map_unknown(self):
        UNKNOWN_VALUE_OFFSET  = 0x08
        UNKNOWN_VALUE_TYPE   = '>H'

        self.map_fh.seek(UNKNOWN_VALUE_OFFSET)
        value = self.map_fh.read(2)
        return unpack(UNKNOWN_VALUE_TYPE, value)[0]

    def get_map_data(self): 
        MAP_DATA_OFFSET     = 0x0a
        MAP_ELEMENT_LEN     = 2
        MAP_ELEMENT_TYPE    = '>H'

        if not self._is_valid_map_file:
            print('Invalid map file. Does not contain obligatory header')
            exit(1)

        width, height = self.get_map_dimensions()
        self.map_fh.seek(MAP_DATA_OFFSET)
        
        map_data = []

        for x in range(0, width):
            map_row = []
            for y in range(0, height):
                entry = self.map_fh.read(MAP_ELEMENT_LEN)
                map_row.append(unpack(MAP_ELEMENT_TYPE, entry)[0])
            map_data.append(map_row)

        return map_data

    def get_map(self):
        m = Map()
        m.world             = self.world
        m.level             = self.level
        m.width, m.height   = self.get_map_dimensions()
        m.unknown           = self.get_map_unknown()
        m.data              = self.get_map_data()
        return m
