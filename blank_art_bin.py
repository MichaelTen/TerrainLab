#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# make_art_bin.py — create clean placeholder art.mul and artidx.mul files
#
# This script generates empty .mul-format art files for compatibility with
# map editors that expect them to exist. It creates:
#   • art.mul      – an empty art container (no images)
#   • artidx.mul   – an index filled with 0xFFFFFFFF entries (no art present)
#
# Use this if you already have a valid tiledata.mul created separately and
# just need minimal art files for editors such as CentrED# or UO Fiddler
# to open your map directory cleanly.
#
# All data is blank, non-proprietary, and safe to redistribute.
#
# Typical usage:
#     python make_art_stubs.py
#
# Notes:
#   – Creates 65,536 (0x10000) “no art” entries by default.
#   – Files are zero-content; meant only to satisfy format expectations.
# ---------------------------------------------------------------------------

import struct

def make_art_stubs(art_path="art.mul", artidx_path="artidx.mul", idx_entries=0x10000):
    # Create an empty art.mul container
    open(art_path, "wb").close()

    # Each artidx entry: [offset:4][length:4][extra:4]
    # Offset set to 0xFFFFFFFF to mark “no art”
    NO_ART = 0xFFFFFFFF
    with open(artidx_path, "wb") as idx:
        for _ in range(idx_entries):
            idx.write(struct.pack("<III", NO_ART, 0, 0))

    print(f"Created {art_path} and {artidx_path} with {idx_entries} empty index entries.")

if __name__ == "__main__":
    make_art_stubs()
