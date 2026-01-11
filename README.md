# TerrainLab


# AxonometricLab.py
## 1/11/26 - THIS HAS NOT BEEN TESTED YET... FOR LEARNING AND IDEA SHARING PURPOSES ONLY ATM... 

## Goal and intent

AxonometricLab.py exists to generate a **fully legal, structurally valid Ultima Online–style MUL data set** that contains **no copyrighted content** from the original game.

The purpose is to:

• Run **CentrED# client and server** without relying on original Ultima Online assets  
• Build and edit worlds using **entirely original tiles, statics, metadata, and art**  
• Remain compatible in spirit and structure with **Classic UO / ServUO pipelines**  
• Enable clean import, conversion, or re-encoding into **Godot-native formats** such as `.res`, `.tres`, or custom binary layouts  
• Support axonometric and isometric world building while respecting copyright fully

Every file produced by this script is either empty or structurally correct but zeroed. Nothing proprietary is embedded. All visual assets, names, metadata, and gameplay logic are intended to be authored by the developer.

This is a foundation tool, not a content pack.

---

## What this script creates

AxonometricLab.py generates a minimal but structurally complete MUL layout that ClassicUO-derived tools expect.

### Asset metadata and registries

• `art.mul`  
• `artidx.mul`  
• `tiledata.mul`  
• `hues.mul`  
• `radarcol.mul`

These files allow CentrED# and UO Fiddler to boot and operate normally while remaining empty and legally clean.

### World and facet data

For a chosen facet number and map size:

• `map{facet}.mul`  
• `staidx{facet}.mul`  
• `statics{facet}.mul`

The map is filled with a developer-chosen default land tile ID and Z value, ready to be edited interactively in CentrED#.

---

## What this script deliberately does not include

• No original Ultima Online artwork  
• No original tile names  
• No original statics  
• No original color tables  
• No sounds, animations, gumps, or UI assets  

All creative content is expected to be authored by you.

---

## Example command

Create a 512 x 512 blank world for facet 0, overwriting existing files:

```bash
python AxonometricLab.py --out ClientMin --force --facet 0 --map-width 512 --map-height 512
````

Create a smaller test map with a custom default tile and elevation:

```bash
python AxonometricLab.py --out ClientMin --force --facet 0 --map-width 256 --map-height 256 --default-land 3 --default-z 5
```

Map width and height must be multiples of 8. This matches the classic 8 x 8 block structure used by UO editors.

---

## Intended workflows

### CentrED# client and server

• Point CentrED# client and server at the generated directory
• Edit terrain, statics placement, and elevations normally
• Use UO Fiddler to inject your own art into `art.mul` and `artidx.mul`
• Keep all content original and legally clean

### ServUO or Classic UO–style servers

• Use the generated MUL files as a base world
• Populate gameplay logic server-side
• Replace or extend asset handling as needed

### Godot and modern engines

This script treats MUL files as an **intermediate authoring format**, not a runtime requirement.

A common pattern is:

1. Author world layout in CentrED#
2. Export or parse MUL data
3. Convert into:
   • Godot `Resource` files
   • Custom chunked binary formats
   • JSON or MessagePack registries for tooling
4. Render using your own meshes, sprites, shaders, and collision logic

Nothing in this repository requires Godot to read MUL files at runtime.

---

## Why this exists

Classic Ultima Online tooling is mature, fast, and spatially expressive. The file formats are simple, deterministic, and well understood.

AxonometricLab.py allows developers to **reuse the structure without reusing the content**.

It is intended for:

• Axonometric RPGs
• Isometric sandbox worlds
• World editors for original IP
• Research and tooling experiments
• Education and engine integration

All without copyright risk.

---

## Legal clarity

This project intentionally avoids distributing or embedding any copyrighted Ultima Online assets.

• File formats are structural facts
• Generated data is zeroed or user-defined
• All content added afterward is the responsibility of the developer

This repository is about **format compatibility**, not asset reuse.

---

## Philosophy

Use the past as scaffolding.
Build something new.
Own your art, your worlds, and your future.

If you extend this script, keep it honest, transparent, and clean.

Limitless peace.

