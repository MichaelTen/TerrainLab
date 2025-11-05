#!/usr/bin/env python3

#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# emptyX.py — generate blank staidx0.mul and statics0.mul files
#
# This utility creates the static index pair required by map editors that use
# .mul-style formats. It produces:
#   • staidx0.mul   — index file with correctly sized empty entries
#   • statics0.mul  — corresponding empty data file
#
# These files define static object placement data, but here they are initialized
# with no content (all lookups set to -1). They are used when starting a new
# custom map so editors such as CentrED# or compatible tools can save and load
# correctly without depending on existing assets.
#
# Each map block represents an 8×8 tile area. The user enters the number of
# blocks horizontally (X) and vertically (Y), and the script calculates the
# correct number of index entries automatically.
#
# Typical usage:
#     python emptyX.py
#     # then follow prompts for Blocks X and Blocks Y
#
# Output:
#   - staidx0.mul  → properly sized, all -1 lookup entries (12 bytes each)
#   - statics0.mul → empty placeholder file
#
# Notes:
#   – Safe for blank or custom worlds; contains no proprietary data.
#   – Only needed to initialize new projects or test editors’ map loading.
#   – You can rerun it anytime to resize for different map dimensions.
# ---------------------------------------------------------------------------

"""
emptyX.py — create an empty staidx0.mul (and empty statics0.mul)
for a custom map in CentrED# of BlocksX × BlocksY (each block = 8×8 tiles).

Usage:
  python emptyX.py
  # then follow prompts for BlocksX and BlocksY
"""

import struct
import pathlib
import sys

def prompt_int(prompt):
    while True:
        try:
            s = input(prompt).strip()
            if s == "":
                print("Please enter a positive integer.")
                continue
            v = int(s, 10)
            if v <= 0:
                print("Please enter a positive integer.")
                continue
            return v
        except ValueError:
            print("Not a valid integer. Try again.")

def main():
    print("== Create empty staidx0.mul/statics0.mul ==")
    print("Each block is 8×8 tiles. You will enter block counts, not tiles.\n")

    blocks_x = prompt_int("Blocks X (e.g., 16): ")
    blocks_y = prompt_int("Blocks Y (e.g., 16): ")

    entries = blocks_x * blocks_y
    total_bytes = entries * 12  # each entry is 12 bytes: 3× int32

    out_dir = pathlib.Path(".")
    staidx_path = out_dir / "staidx0.mul"
    statics_path = out_dir / "statics0.mul"

    # Write staidx0.mul with empty entries:
    #   lookup = -1 (0xFFFFFFFF), length = 0, extra = 0
    with staidx_path.open("wb") as f:
        empty_entry = struct.pack("<iii", -1, 0, 0)
        f.write(empty_entry * entries)

    # Ensure an empty statics0.mul exists
    statics_path.write_bytes(b"")

    print("\nDone.")
    print(f"Blocks: {blocks_x} × {blocks_y} (tiles: {blocks_x*8} × {blocks_y*8})")
    print(f"Entries written: {entries}")
    print(f"staidx0.mul size: {total_bytes} bytes")
    print(f"Wrote: {staidx_path.resolve()}")
    print(f"Wrote: {statics_path.resolve()}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nCanceled by user.")
