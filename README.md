# TerrainLab

# AxonometricLab.py
## Updated 1/17/26 – Tested iteratively with CentrED#; designed for ClassicUO-compatible tooling

---

## Goal and intent

**AxonometricLab.py** exists to generate a **fully legal, structurally valid Ultima Online–style MUL data set** that contains **no copyrighted content** from the original game.

The purpose is to:

- Run **CentrED# client and server** without relying on original Ultima Online assets  
- Build and edit worlds using **entirely original tiles, statics, metadata, and art**  
- Remain compatible *in spirit and structure* with **ClassicUO / ServUO pipelines**  
- Enable clean import, conversion, or re-encoding into **Godot-native formats** such as `.res`, `.tres`, or custom binary layouts  
- Support axonometric and isometric world building while fully respecting copyright

Every file produced by this script is either **empty** or **structurally correct but zeroed**.  
Nothing proprietary is embedded. All visual assets, names, metadata, and gameplay logic are intended to be authored by the developer.

This is a **foundation tool**, not a content pack.

---

## Compatibility status (important)

- **CentrED#**: Actively tested during development and iteration  
- **ClassicUO**: File structures are based on ClassicUO loader expectations, but **direct runtime testing in ClassicUO has not yet been performed**  
- **ServUO / UO-style servers**: Structurally aligned, but server-specific behavior may vary

The intent is full compatibility, but this project favors **structural correctness and legal cleanliness** over unverified claims.

---

## What this script creates

AxonometricLab.py generates a **minimal but structurally complete MUL layout** that CentrED# and ClassicUO-derived tooling expect to exist.

### Asset metadata and registries

These files allow UO-style editors to boot without missing-file or null-reference errors:

- `art.mul`  
- `artidx.mul`  
- `tiledata.mul`  
- `hues.mul`  
- `radarcol.mul`  

All entries are empty or zeroed. No art, names, or colors are included.

---

### Texture data (land textures)

Required by CentrED# and ClassicUO asset loaders, even when unused:

- `texmaps.mul`  
- `texidx.mul`  

All texture slots are marked as missing. The container is intentionally blank.

---

### Lighting data

Required by ClassicUO-derived loaders:

- `light.mul`  
- `lightidx.mul`  

These files contain no light patterns but are structurally valid to prevent loader crashes.

---

### Multis (houses, boats, large structures)

Required by CentrED# blueprint and multi loaders:

- `multi.mul`  
- `multi.idx`  

All entries are empty. This prevents null-reference errors during multi initialization.

---

### World and facet data

For a chosen facet number and map size:

- `map{facet}.mul`  
- `staidx{facet}.mul`  
- `statics{facet}.mul`  

The map is filled with a developer-chosen **default land tile ID** and **default Z value**, ready to be edited interactively in CentrED#.

Map dimensions must be multiples of **8 × 8**, matching the classic UO block structure.

---

## What this script deliberately does not include

- No original Ultima Online artwork  
- No original tile names  
- No original statics  
- No original color tables  
- No sounds, animations, gumps, or UI assets  

All creative content is expected to be authored by you.

---

## Example commands

Create a **512 × 512** blank world for facet 0, overwriting existing files:

```bash
python AxonometricLab.py --out ClientMin --force --facet 0 --map-width 512 --map-height 512
````

Create a smaller test map with a custom default tile and elevation:

```bash
python AxonometricLab.py \
  --out ClientMin \
  --force \
  --facet 0 \
  --map-width 256 \
  --map-height 256 \
  --default-land 3 \
  --default-z 5
```

Map width and height **must** be multiples of 8.

---

## Intended workflows

### CentrED# client and server

* Point CentrED# client and server at the generated directory
* Load without missing-file or null-reference crashes
* Edit terrain, statics placement, elevations, and multis normally
* Use **UO Fiddler** to inject your own original art and metadata
* Keep all content original and legally clean

---

### ServUO or Classic UO–style servers

* Use the generated MUL files as a base world
* Populate gameplay logic server-side
* Replace or extend asset handling as needed

---

### Godot and modern engines

This script treats MUL files as an **intermediate authoring format**, not a runtime requirement.

A common pattern:

1. Author world layout in CentrED#
2. Export or parse MUL data
3. Convert into:

   * Godot `Resource` files
   * Custom chunked binary formats
   * JSON or MessagePack registries
4. Render using your own meshes, sprites, shaders, lighting, and collision logic

Nothing in this repository requires Godot to read MUL files at runtime.

---

## Why this exists

Classic Ultima Online tooling is mature, fast, and spatially expressive.
The file formats are simple, deterministic, and well understood.

AxonometricLab.py allows developers to **reuse the structure without reusing the content**.

It is intended for:

* Axonometric RPGs
* Isometric sandbox worlds
* World editors for original IP
* Research and tooling experiments
* Education and engine integration

All without copyright risk.

---

## Legal clarity

This project intentionally avoids distributing or embedding any copyrighted Ultima Online assets.

* File formats are structural facts
* Generated data is zeroed or user-defined
* All content added afterward is the responsibility of the developer

This repository is about **format compatibility**, not asset reuse.

---

## Philosophy

Use the past as scaffolding.
Build something new.
Own your art, your worlds, and your future.

If you extend this script, keep it honest, transparent, and clean.

Limitless peace.
