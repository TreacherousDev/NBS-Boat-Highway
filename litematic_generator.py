import csv
from collections import defaultdict
from litemapy import Region, BlockState

INSTRUMENT_BLOCKS = {
    0: "minecraft:air",            # Piano (requires air block)
    1: "minecraft:oak_wood",       # Double Bass
    2: "minecraft:stone",          # Bass Drum
    3: "minecraft:sand",           # Snare Drum
    4: "minecraft:glass",          # Click
    5: "minecraft:wool",           # Guitar
    6: "minecraft:clay",           # Flute
    7: "minecraft:gold_block",     # Bell
    8: "minecraft:packed_ice",     # Chime
    9: "minecraft:bone_block",     # Xylophone
    10: "minecraft:iron_block",    # Iron Xylophone
    11: "minecraft:soul_sand",     # Cow Bell
    12: "minecraft:pumpkin",       # Didgeridoo
    13: "minecraft:emerald_block", # Bit
    14: "minecraft:hay_block",     # Banjo
    15: "minecraft:glowstone",     # Pling
}
INSTRUMENT_SOUNDS = {
    0: "piano",
    1: "bass",
    2: "basedrum",          
    3: "snare",
    4: "hat",        
    5: "guitar",
    6: "flute",
    7: "bell",
    8: "chime",
    9: "xylophone",
    10: "iron_xylophone",    
    11: "cow_bell",     
    12: "didgeridoo",      
    13: "bit",
    14: "banjo",    
    15: "pling",     
}

# Read CSV
notes = []
with open("output.csv", newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        tick = int(row["tick"])
        instrument = int(row["instrument"])
        key = int(row["key"])
        notes.append((tick, instrument, key))

# Group notes by tick
tick_map = defaultdict(list)
for note in notes:
    tick_map[note[0]].append(note)

# Determine schematic size
max_tick = max(tick_map.keys())
width = (max_tick + 2) * 16
height = 2
depth = 5

# Create schematic
reg = Region(0, 0, 0, width, height, depth)
schem = reg.as_schematic(name="Boat Song", author="TreacherousDev", description="Made with litemapy")

offsets = [
    (-1, -1),     # 1st note
    (-1, 1),    # 2nd note
    (1, -1),     # 3rd note
    (1, 1),     # 4th note
    (2, 0),     # 5th note
    (-2, 0),     # 6th note
    (0, 2),     # 7th note
    (0, -2),     # 8th note
]

# Place blocks
for tick, notes_on_tick in tick_map.items():
    base_x = tick * 16 + 2
    base_z = 2  # Center z, to allow space left and right
    for i, (t, instrument, key) in enumerate(notes_on_tick):
        dx, dz = offsets[i] if i < len(offsets) else (i + 3, 0)  # Extend if more than 8 ?? 
        x = base_x + dx
        z = base_z + dz
        y = 0

        instr_block_id = INSTRUMENT_BLOCKS.get(instrument, "minecraft:air")
        reg[x, y, z] = BlockState(instr_block_id)

        reg[x, y + 1, z] = BlockState(
            "minecraft:note_block",
            note=str(max(0, min(key, 24))),
            instrument=INSTRUMENT_SOUNDS.get(instrument, "piano")
        )

# Save schematic
schem.save("output.litematic")
print("Litematic file saved as output.litematic")
