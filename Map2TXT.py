#!/usr/bin/env python3
# ---------------------------------------------------------------------------
# Map2TXT.py — export .mul-style terrain maps into human-readable text
#
# This tool reads a binary map#.mul file (commonly used by tile-based
# 2D world editors) and converts it into a block-by-block text layout.
# Each 8×8 cell block is unpacked into its 2-byte tile ID and 1-byte
# altitude values, producing a grid that’s easy to study or visualize.
#
# It’s useful for:
#   • Studying or analyzing 2D pixel-grid terrain data
#   • Inspecting map structure without relying on a graphical editor
#   • Converting or preparing maps for import into custom engines (e.g., Godot)
#   • Examining totally unique maps created in open tools such as CentrED#
#
# Supported features:
#   – Automatic detection of common map sizes
#   – Optional full-map output with --all-blocks
#   – Clear tile:altitude text formatting
#
# Typical usage:
#     python Map2TXT.py map0.mul --all-blocks
#
# This will produce map0_all_blocks.txt in the same directory, showing
# each 8×8 block as a section of tile IDs and elevation values.
#
# Notes:
#   – The script is read-only and non-destructive.
#   – It’s designed for studying and documenting original map data,
#     including blank or custom worlds created in open editors.
#   – All terminology refers generically to legacy .mul-style formats.
# ---------------------------------------------------------------------------

import argparse, struct, math
from pathlib import Path

BLOCK_SIZE_BYTES = 4 + 64 * 3           # 4-byte header + 64 cells * 3 bytes
CELL_STRUCT = struct.Struct("<Hb")      # uint16 tile_id (LE) + int8 altitude

KNOWN_BLOCK_DIMS = {
    (768, 512): "Classic rectangular (map0/map1 style)",
    (896, 512): "Large rectangular (variant)",
    (288, 200): "Medium rectangular (map2-like)",
    (256, 256): "Square (map3-like)",
    (181, 181): "Small square (map4-like)",
    (512, 512): "Square test/dev",
}

def autodetect_block_dims(file_size: int):
    if file_size % BLOCK_SIZE_BYTES != 0:
        raise SystemExit(
            f"File size {file_size} is not a multiple of block size {BLOCK_SIZE_BYTES}; "
            "this does not look like a valid map#.mul."
        )
    total_blocks = file_size // BLOCK_SIZE_BYTES
    for (ax, ay), label in KNOWN_BLOCK_DIMS.items():
        if ax * ay == total_blocks:
            return ax, ay, label, total_blocks
    # fallback heuristic
    return int(math.sqrt(total_blocks)), int(math.sqrt(total_blocks)), "Heuristic", total_blocks

def block_offset(bx: int, by: int, blocks_down: int) -> int:
    return ((bx * blocks_down) + by) * BLOCK_SIZE_BYTES

def read_block(f, bx: int, by: int, blocks_down: int):
    f.seek(block_offset(bx, by, blocks_down))
    header = f.read(4)
    if len(header) != 4: raise SystemExit("Unexpected EOF in block header.")
    cells = []
    for y in range(8):
        row = []
        for x in range(8):
            data = f.read(CELL_STRUCT.size)
            if len(data) != CELL_STRUCT.size:
                raise SystemExit("Unexpected EOF in block data.")
            tile, alt = CELL_STRUCT.unpack(data)
            row.append((tile, alt))
        cells.append(row)
    return header, cells

def dump_block_pretty(cells, bx: int, by: int) -> str:
    lines = [f"# Block ({bx},{by}) — 8x8 cells, format tile:alt"]
    for y in range(8):
        lines.append(" ".join(f"{tile:04d}:{alt:+d}" for (tile, alt) in cells[y]))
    return "\n".join(lines) + "\n\n"

def main():
    ap = argparse.ArgumentParser(description="Dump .mul-style terrain map into block-by-block text.")
    ap.add_argument("input", type=Path, help="map#.mul file")
    ap.add_argument("-o", "--output", type=Path, help="Output .txt file (default auto-named)")
    ap.add_argument("--all-blocks", action="store_true", help="Dump every block in the map")
    args = ap.parse_args()

    file_size = args.input.stat().st_size
    blocks_across, blocks_down, label, total_blocks = autodetect_block_dims(file_size)
    print("# map2txt summary")
    print(f"file: {args.input}")
    print(f"size: {file_size} bytes")
    print(f"total blocks: {blocks_across} x {blocks_down} ({total_blocks}) ({label})")
    print(f"cells: {blocks_across*8} x {blocks_down*8}\n")

    out_path = args.output or args.input.with_name(f"{args.input.stem}_all_blocks.txt")

    with args.input.open("rb") as f, out_path.open("w", encoding="utf-8") as out_fp:
        if args.all_blocks:
            for bx in range(blocks_across):
                for by in range(blocks_down):
                    _, cells = read_block(f, bx, by, blocks_down)
                    out_fp.write(dump_block_pretty(cells, bx, by))
        else:
            # default: just block (0,0)
            _, cells = read_block(f, 0, 0, blocks_down)
            out_fp.write(dump_block_pretty(cells, 0, 0))

    print(f"Wrote {out_path}")

if __name__ == "__main__":
    main()
