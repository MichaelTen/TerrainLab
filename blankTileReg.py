# make_tiledata_mul_full.py
# Spec-correct classic tiledata.mul:
#  - 512 land groups  (32 entries each)
#  - 2048 static groups (32 entries each)
# All fields zeroed (safe for Godot; just for editors to load cleanly).
#
# ---------------------------------------------------------------------------
# This script generates a blank TileData file that matches the structural
# format used by legacy .mul-based world editors and map-building tools.
# It defines the correct byte layout for both land and static tile sections
# but contains no proprietary data, names, or artwork.
#
# Each group begins with a 4-byte header followed by 32 fixed-length entries:
#   • Land entry  : 26 bytes (flags, texture ID, and 20-character name)
#   • Static entry: 37 bytes (flags, stats, height, and 20-character name)
#
# The resulting file (~2.9 MB) adheres to the traditional format so that
# compatible open-source editors can read and display tile groups correctly.
# All numeric values and names are zeroed, producing a legally clean base for:
#   – testing map editor functionality
#   – building entirely new worlds from scratch
#   – later filling in your own custom tile definitions
#
# For integration with Godot:
#   – Do NOT add gameplay flags here; keep all values at zero.
#   – This file exists only to satisfy external map editors.
#   – Your actual game logic and tile metadata will live in your own
#     .res/.tres/.json registries within Godot.
# ---------------------------------------------------------------------------


import struct

LAND_GROUPS      = 512
LAND_ENTRY_SIZE  = 26  # Flags(DWORD)=4, TextureID(WORD)=2, Name[20]
STATIC_GROUPS    = 2048
STATIC_ENTRY_SIZE= 37  # Classic static entry layout (37 bytes)
NAME20_ZERO      = b"\x00" * 20

def write_land_group(f):
    # Group header DWORD (unused)
    f.write(struct.pack("<I", 0))
    for _ in range(32):
        f.write(struct.pack("<I", 0))   # Flags
        f.write(struct.pack("<H", 0))   # TextureID
        f.write(NAME20_ZERO)            # Name[20]

def write_static_group(f):
    f.write(struct.pack("<I", 0))       # Group header
    for _ in range(32):
        # Flags(DWORD), Weight(B), Quality(B), Unknown(WORD),
        # Unknown1(B), Quantity(B), AnimID(WORD), Unknown2(B),
        # Hue(B), Unknown3(WORD), Height(B), Name[20]
        f.write(struct.pack("<I", 0))   # Flags
        f.write(struct.pack("<B", 0))   # Weight
        f.write(struct.pack("<B", 0))   # Quality
        f.write(struct.pack("<H", 0))   # Unknown
        f.write(struct.pack("<B", 0))   # Unknown1
        f.write(struct.pack("<B", 0))   # Quantity
        f.write(struct.pack("<H", 0))   # AnimID
        f.write(struct.pack("<B", 0))   # Unknown2
        f.write(struct.pack("<B", 0))   # Hue
        f.write(struct.pack("<H", 0))   # Unknown3
        f.write(struct.pack("<b", 0))   # Height (signed)
        f.write(NAME20_ZERO)            # Name[20]

if __name__ == "__main__":
    with open("tiledata.mul", "wb") as f:
        for _ in range(LAND_GROUPS):
            write_land_group(f)
        for _ in range(STATIC_GROUPS):
            write_static_group(f)

    land_bytes   = LAND_GROUPS   * (4 + 32*LAND_ENTRY_SIZE)
    static_bytes = STATIC_GROUPS * (4 + 32*STATIC_ENTRY_SIZE)
    total = land_bytes + static_bytes
    print(f"tiledata.mul written: land={land_bytes} bytes, "
          f"static={static_bytes} bytes, total={total} bytes")
