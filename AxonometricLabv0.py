#!/usr/bin/env python3
"""
uo_min_client_muls.py

Creates a structurally valid, non-proprietary minimal set of UO .mul files that
CentrED# and UO Fiddler typically expect to exist.

Creates (in output directory):
  - art.mul            (empty container; no artwork)
  - artidx.mul         (0x14000 index records pointing to "no art")
  - tiledata.mul       (classic layout: 512 land groups + 2048 static groups; all zeroed)
  - hues.mul           (default 375 groups x 8 hues = 3000 hues; all zeroed)
  - radarcol.mul       (0x10000 ushort colors; all zeroed)
  - map{facet}.mul     (classic map format, blank tiles, user-defined size)
  - staidx{facet}.mul  (one record per 8x8 block, all empty)
  - statics{facet}.mul (empty container)

Notes:
  - This generates structurally valid placeholders only.
  - It intentionally contains no copyrighted artwork or original names.
  - You can later add your own original art and metadata using tools like UO Fiddler.
  - Map size must be a multiple of 8 in both dimensions.

Usage examples:
  python uo_min_client_muls.py --out ClientMin --force --facet 0 --map-width 512 --map-height 512
  python uo_min_client_muls.py --out ClientMin --force --facet 0 --map-width 256 --map-height 256 --default-land 2 --default-z 0
"""

from __future__ import annotations
import argparse
import struct
from pathlib import Path


# ----------------------------
# File helpers
# ----------------------------

def write_file(path: Path, data: bytes, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} exists. Use --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)

def write_streamed(path: Path, writer_fn, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"{path} exists. Use --force to overwrite.")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        writer_fn(f)

def require_multiple_of_8(value: int, name: str) -> None:
    if value <= 0:
        raise ValueError(f"{name} must be > 0.")
    if value % 8 != 0:
        raise ValueError(f"{name} must be a multiple of 8. Got {value}.")


# ----------------------------
# art.mul / artidx.mul
# ----------------------------

def make_art_mul(out_dir: Path, force: bool) -> None:
    # Art container has no header. Empty is acceptable when artidx marks "no art".
    write_file(out_dir / "art.mul", b"", force)

def make_artidx_mul(out_dir: Path, force: bool, idx_entries: int = 0x14000) -> None:
    # Index record: 12 bytes [lookup:4][size:4][extra:4]
    # "No art" lookup is 0xFFFFFFFF, size 0, extra 0.
    NO_ART = 0xFFFFFFFF
    record = struct.pack("<III", NO_ART, 0, 0)
    write_file(out_dir / "artidx.mul", record * idx_entries, force)


# ----------------------------
# tiledata.mul (classic groups)
# ----------------------------

LAND_GROUPS = 512
STATIC_GROUPS = 2048
NAME20_ZERO = b"\x00" * 20

def make_tiledata_mul(out_dir: Path, force: bool) -> None:
    # Land groups: 512 * (4 + 32 * 26)
    # Static groups: 2048 * (4 + 32 * 37)
    def writer(f):
        # Land
        for _ in range(LAND_GROUPS):
            f.write(struct.pack("<I", 0))  # group header
            for _ in range(32):
                f.write(struct.pack("<I", 0))  # flags
                f.write(struct.pack("<H", 0))  # texture id
                f.write(NAME20_ZERO)           # name[20]

        # Statics
        for _ in range(STATIC_GROUPS):
            f.write(struct.pack("<I", 0))  # group header
            for _ in range(32):
                f.write(struct.pack("<I", 0))  # flags
                f.write(struct.pack("<B", 0))  # weight
                f.write(struct.pack("<B", 0))  # quality
                f.write(struct.pack("<H", 0))  # unknown
                f.write(struct.pack("<B", 0))  # unknown1
                f.write(struct.pack("<B", 0))  # quantity
                f.write(struct.pack("<H", 0))  # animid
                f.write(struct.pack("<B", 0))  # unknown2
                f.write(struct.pack("<B", 0))  # hue
                f.write(struct.pack("<H", 0))  # unknown3
                f.write(struct.pack("<b", 0))  # height (signed)
                f.write(NAME20_ZERO)           # name[20]

    write_streamed(out_dir / "tiledata.mul", writer, force)


# ----------------------------
# hues.mul (default 3000 hues)
# ----------------------------

def make_hues_mul(out_dir: Path, force: bool, hue_groups: int = 375) -> None:
    # Each group: DWORD header + 8 hue entries
    # Hue entry: 32*WORD colors (64) + WORD start + WORD end + CHAR[20] name = 88 bytes
    def writer(f):
        hue_entry = (
            (b"\x00" * (32 * 2)) +          # 32 WORD colors
            struct.pack("<H", 0) +          # tableStart
            struct.pack("<H", 0) +          # tableEnd
            (b"\x00" * 20)                  # name[20]
        )
        if len(hue_entry) != 88:
            raise RuntimeError("Internal error: hue_entry size is not 88 bytes.")

        for _ in range(hue_groups):
            f.write(struct.pack("<I", 0))   # group header
            for _ in range(8):
                f.write(hue_entry)

    write_streamed(out_dir / "hues.mul", writer, force)


# ----------------------------
# radarcol.mul
# ----------------------------

def make_radarcol_mul(out_dir: Path, force: bool, entries: int = 0x10000) -> None:
    # 0x10000 ushort colors
    write_file(out_dir / "radarcol.mul", b"\x00\x00" * entries, force)


# ----------------------------
# map{facet}.mul / staidx{facet}.mul / statics{facet}.mul
# ----------------------------

def make_map_and_statics(
    out_dir: Path,
    force: bool,
    facet: int,
    width: int,
    height: int,
    default_land: int = 0,
    default_z: int = 0
) -> None:
    require_multiple_of_8(width, "map-width")
    require_multiple_of_8(height, "map-height")
    if facet < 0 or facet > 255:
        raise ValueError("facet must be between 0 and 255.")
    if default_land < 0 or default_land > 0x3FFF:
        raise ValueError("default-land must be between 0 and 16383 (0x3FFF).")
    if default_z < -128 or default_z > 127:
        raise ValueError("default-z must be between -128 and 127.")

    map_path = out_dir / f"map{facet}.mul"
    staidx_path = out_dir / f"staidx{facet}.mul"
    statics_path = out_dir / f"statics{facet}.mul"

    blocks_x = width // 8
    blocks_y = height // 8
    block_count = blocks_x * blocks_y

    # Classic map block:
    #   int32 header
    #   64 tiles, each tile:
    #     uint16 landTileId
    #     int8   z
    # Total = 4 + 64*3 = 196 bytes
    tile_bytes = struct.pack("<Hb", default_land, default_z)  # 3 bytes
    block_header = struct.pack("<i", 0)
    one_block = block_header + (tile_bytes * 64)

    if len(one_block) != 196:
        raise RuntimeError("Internal error: map block is not 196 bytes.")

    def write_map(f):
        for _ in range(block_count):
            f.write(one_block)

    # Staidx entry (classic):
    #   int32 lookup
    #   int32 length
    #   int32 extra
    # For empty statics: lookup = -1, length = 0, extra = 0
    empty_staidx = struct.pack("<iii", -1, 0, 0)

    def write_staidx(f):
        f.write(empty_staidx * block_count)

    # Statics container empty
    write_streamed(map_path, write_map, force)
    write_streamed(staidx_path, write_staidx, force)
    write_file(statics_path, b"", force)


# ----------------------------
# Main
# ----------------------------

def main() -> int:
    p = argparse.ArgumentParser(description="Generate minimal, structurally valid UO .mul files (no proprietary content).")
    p.add_argument("--out", default="ClientMin", help="Output directory")
    p.add_argument("--force", action="store_true", help="Overwrite existing files")

    p.add_argument("--facet", type=int, default=0, help="Facet number (default 0 -> map0.mul, staidx0.mul, statics0.mul)")
    p.add_argument("--map-width", type=int, default=256, help="Map width in tiles (must be multiple of 8). Default 256.")
    p.add_argument("--map-height", type=int, default=256, help="Map height in tiles (must be multiple of 8). Default 256.")
    p.add_argument("--default-land", type=int, default=0, help="Default land tile ID to fill the map with (default 0).")
    p.add_argument("--default-z", type=int, default=0, help="Default Z altitude to fill the map with (default 0).")

    p.add_argument("--artidx-entries", type=lambda x: int(x, 0), default=0x14000,
                   help="Number of artidx records (default 0x14000). Accepts hex like 0x14000.")
    p.add_argument("--hue-groups", type=int, default=375, help="Number of hue groups (default 375 -> 3000 hues)")

    args = p.parse_args()

    out_dir = Path(args.out)

    make_art_mul(out_dir, args.force)
    make_artidx_mul(out_dir, args.force, idx_entries=args.artidx_entries)
    make_tiledata_mul(out_dir, args.force)
    make_hues_mul(out_dir, args.force, hue_groups=args.hue_groups)
    make_radarcol_mul(out_dir, args.force)

    make_map_and_statics(
        out_dir=out_dir,
        force=args.force,
        facet=args.facet,
        width=args.map_width,
        height=args.map_height,
        default_land=args.default_land,
        default_z=args.default_z
    )

    def sz(name: str) -> int:
        return (out_dir / name).stat().st_size

    map_name = f"map{args.facet}.mul"
    staidx_name = f"staidx{args.facet}.mul"
    statics_name = f"statics{args.facet}.mul"

    print("Wrote minimal MUL set to:", out_dir.resolve())
    print("Sizes:")
    print("  art.mul          =", sz("art.mul"), "bytes")
    print("  artidx.mul       =", sz("artidx.mul"), "bytes")
    print("  tiledata.mul     =", sz("tiledata.mul"), "bytes")
    print("  hues.mul         =", sz("hues.mul"), "bytes")
    print("  radarcol.mul     =", sz("radarcol.mul"), "bytes")
    print(f"  {map_name:<14} =", sz(map_name), "bytes")
    print(f"  {staidx_name:<14} =", sz(staidx_name), "bytes")
    print(f"  {statics_name:<14} =", sz(statics_name), "bytes")

    blocks_x = args.map_width // 8
    blocks_y = args.map_height // 8
    block_count = blocks_x * blocks_y

    print("Map info:")
    print(f"  facet           = {args.facet}")
    print(f"  size            = {args.map_width} x {args.map_height} tiles")
    print(f"  blocks          = {blocks_x} x {blocks_y} (8x8), total {block_count} blocks")
    print(f"  default land id = {args.default_land}")
    print(f"  default z       = {args.default_z}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
