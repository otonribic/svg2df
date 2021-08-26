'''Convert SVG to Dark Forces' .LEV geometry, with some extra parameters
#
SECTOR 24
 NAME
 AMBIENT          25
 FLOOR TEXTURE    13  0.00  0.00 2
 FLOOR ALTITUDE   24.00
 CEILING TEXTURE  46  0.00  0.00 2
 CEILING ALTITUDE 16.00
 SECOND ALTITUDE   0.00
 FLAGS            2 0 0
 LAYER            0
 VERTICES 4
  X: 280.00 Z: 362.00 #  0
  X: 272.00 Z: 362.00 #  1
  X: 272.00 Z: 364.00 #  2
  X: 280.00 Z: 364.00 #  3
 WALLS 4
  WALL LEFT:  0 RIGHT:  1 MID:  41  0.00  0.00 0 TOP:  22  0.00  0.00 0 BOT:  22  0.00  0.00 0 SIGN: -1 0.00 0.00 ADJOIN: 23 MIRROR: 2 WALK: 23 FLAGS: 0 0 0 LIGHT: 0
  WALL LEFT:  1 RIGHT:  2 MID:  54  0.00  0.00 0 TOP:  22  0.00  0.00 0 BOT:  22  0.00  0.00 0 SIGN: -1 0.00 0.00 ADJOIN: -1 MIRROR: -1 WALK: -1 FLAGS: 0 0 0 LIGHT: 0
  WALL LEFT:  2 RIGHT:  3 MID:  41  0.00  0.00 0 TOP:  22  0.00  0.00 0 BOT:  22  0.00  0.00 0 SIGN: -1 0.00 0.00 ADJOIN: 25 MIRROR: 0 WALK: 25 FLAGS: 0 0 0 LIGHT: 0
  WALL LEFT:  3 RIGHT:  0 MID:  54  0.00  0.00 0 TOP:  22  0.00  0.00 0 BOT:  22  0.00  0.00 0 SIGN: -1 0.00 0.00 ADJOIN: -1 MIRROR: -1 WALK: -1 FLAGS: 0 0 0 LIGHT: 0
'''

INPUTFILE = 'res\\arena.svg'
OUTFILE = 'dfsvg.lev'

SECTOROFFSET = 775  # Begin with this sector ID number (instead of 0)
GEOSCALE = 0.1  # Multiplier of all coordinates (zoom/scale)

VERTEXRANDOMRANGE = 0  # To be added at the end (random range) unless used in more than 1 sector
NAMEPREFIX = 'zzz'

# Randomly picked from sets:
LIGHTNESS = [25]
FLOOR = [-178, -177, -176, -175]
CEILING = [-168, -167, -166, -165]

# Metadata for sector(s)
FLAGS = '0 0 0'
LAYER = '2'
TEMPLATE = '''#
SECTOR {0}
 NAME     {1}
 AMBIENT          {2}
 FLOOR TEXTURE    1  0.00  0.00 2
 FLOOR ALTITUDE   {3}.00
 CEILING TEXTURE  1  0.00  0.00 2
 CEILING ALTITUDE {4}.00
 SECOND ALTITUDE   0.00
 FLAGS            {5}
 LAYER            {6}'''

# ==================================================================================

import re
import random


def getrandname():
    cands = 'abcdefghijklmnopqrstuvwxyz'
    return NAMEPREFIX + ''.join([random.choice(cands) for b in range(8)])


# Open file
inf = open(INPUTFILE, 'r')
indat = inf.read()
inf.close()
# Parse to get points
polygons = re.findall('<polygon.*?/>', indat)
# Clean up to get REALLY clean points
polygons = [e.partition('points="')[2].partition('"')[0] for e in polygons]
# Get actual numbers
polygons = [e.split(' ') for e in polygons]
polygons = [[[float(y) for y in k.split(',')] for k in c if k] for c in polygons]

allvertices = []  # Collector
# Count all and group
for poly in polygons:
    for x, y in poly:
        allvertices.append((x, y))
print('Polygons: ', len(polygons))
print('Vertices: ', len(allvertices))

# Loaded all, now process to sectors
output = []  # Collector of one- or multi-row strings to be concatenated at the end

# Iterate over all polygons
for id, polygon in enumerate(polygons):
    print('Polygon V: ', len(polygon))
    # Generate header
    header = TEMPLATE.format(SECTOROFFSET + id,  # ID
                             getrandname(),  # name
                             random.choice(LIGHTNESS),  # light
                             -random.choice(FLOOR),  # floor
                             -random.choice(CEILING),  # ceiling
                             FLAGS,  # flags
                             LAYER,  # layer
                             )
    output.append(header)

    # Now onto geometry
    output.append(' VERTICES {0}'.format(len(polygon)))
    # Export vertices
    for vid, elem in enumerate(polygon):
        usage = allvertices.count(tuple(elem))
        elem[0] *= GEOSCALE
        elem[1] *= GEOSCALE
        # Randomize coordinates if needed
        if VERTEXRANDOMRANGE:
            if usage == 1:
                elem[0] += random.random() * VERTEXRANDOMRANGE - VERTEXRANDOMRANGE / 2
                elem[1] += random.random() * VERTEXRANDOMRANGE - VERTEXRANDOMRANGE / 2
        # DF uses 2 decimals precision
        elem[0] = round(elem[0], 2)
        elem[1] = round(elem[1], 2)
        output.append('  X: {0} Z: {1} # {2}'.format(elem[0], elem[1], vid))
        # Add walls
    output.append(' WALLS {0}'.format(len(polygon)))
    for wall in range(len(polygon)):
        wallstring = '  WALL LEFT:  {0} RIGHT:  {1} MID:  54  0.00  0.00 0 TOP:  22  0.00  0.00 0 BOT:  22  0.00  0.00 0 SIGN: -1 0.00 0.00 ADJOIN: -1 MIRROR: -1 WALK: -1 FLAGS: 0 0 0 LIGHT: 0'
        wallstring = wallstring.format(wall, (wall + 1) % len(polygon))
        output.append(wallstring)

# Collected all, export
outf = open(OUTFILE, 'w', encoding='ascii')
outf.write('\n'.join(output))
outf.close()
print('All done')