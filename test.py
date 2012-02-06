from input.mapreader import MapReader
from input.palettereader import PaletteReader
from input.tilesetreader import TilesetReader

mr = MapReader('w1l0.map')
m = mr.get_map()
#m.dump_data_ascii()

pr = PaletteReader('w1.pcc')
p = pr.get_palette()
p.dump_data()

tr = TilesetReader('w1.ico', p)
t = tr.get_tileset()
print t.data[44]
